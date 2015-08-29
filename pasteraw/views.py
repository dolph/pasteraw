import os

import flask

from pasteraw import app
from pasteraw import backend
from pasteraw import decorators
from pasteraw import forms

import time


RATE_LIMIT_BY_IP = {}
MAX_THROTTLES = 3


def check_rate_limit(request):
    if app.config['TESTING']:
        # ignore rate limiting in debug mode
        return True

    # this is the actual remote address passed through nginx
    ip = request.headers['X-Real-IP']

    rate = 3.0  # unit: messages
    per = 60.0  # unit: seconds

    RATE_LIMIT_BY_IP.setdefault(ip, (rate, time.time(), 0))
    allowance, last_check, throttle_count = RATE_LIMIT_BY_IP[ip]

    current = time.time()
    time_passed = current - last_check
    last_check = current
    allowance += time_passed * (rate / per)

    if allowance > rate:
        # A lot of time has passed since we last saw this IP, reset their
        # throttle.
        allowance = rate

    if allowance < 1.0:
        RATE_LIMIT_BY_IP[ip] = (allowance, last_check, throttle_count + 1)
        retry_after = (1.0 - allowance) * (per / rate)
        app.logger.warning(
            'Throttling %s (allowance=%s, last_check=%s, throttle_count=%s, '
            'retry_after=%s)' % (
                ip, allowance, last_check, throttle_count, retry_after))
        if throttle_count <= MAX_THROTTLES:
            raise RateLimitExceeded(
                'Rate limit exceeded. Retry after %s seconds.' % retry_after)
        else:
            raise RateLimitExceeded('Rate limit exceeded.')
    else:
        RATE_LIMIT_BY_IP[ip] = (allowance - 1, last_check, throttle_count)
        return True


class ApiException(Exception):
    status_code = None

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv


class BadRequest(ApiException):
    status_code = 400


class RateLimitExceeded(ApiException):
    status_code = 429


@app.route('/', methods=['POST', 'GET'])
@decorators.templated()
def index():
    form = forms.PasteForm(csrf_enabled=False)
    if form.validate_on_submit():
        check_rate_limit(flask.request)
        url = backend.write(flask.request.form['content'])
        return flask.redirect(url)
    return dict(form=form)


@app.route('/api/v1/pastes', methods=['POST'])
def create_paste():
    form = forms.PasteForm(csrf_enabled=False)
    if form.validate_on_submit():
        check_rate_limit(flask.request)
        url = backend.create(flask.request.form['content'])
        return flask.redirect(url)
    raise BadRequest('Missing paste content')


@app.route('/<paste_id>')
def show_paste(paste_id):
    """Either returns a locally-stored paste or redirects to CDN.

    Redirecting to the CDN handles both legacy paste URLs and pastes that used
    to be stored locally, but have since been moved to the CDN.

    """
    try:
        content = backend.read(paste_id)
        return content, 200, {'Content-Type': 'text/plain; charset="utf-8"'}
    except backend.InvalidKey:
        flask.abort(404)
    except backend.NotFound:
        # The file is not here, but maybe it's on the CDN?
        url = backend.remote_url(paste_id)
        return flask.redirect(url, 301)


@app.errorhandler(404)
def handle_not_found(error):
    return flask.render_template('not_found.html'), 404


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(RateLimitExceeded)
def handle_rate_limit_exceeded(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/x-icon')
