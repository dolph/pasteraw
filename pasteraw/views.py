import os

import flask

from pasteraw import app
from pasteraw import backend
from pasteraw import decorators
from pasteraw import exceptions
from pasteraw import forms
from pasteraw import rate_limit


@app.route('/', methods=['POST', 'GET'])
@decorators.templated()
def index():
    form = forms.PasteForm(csrf_enabled=False)
    if form.validate_on_submit():
        rate_limit.throttle(flask.request)
        url = backend.write(flask.request.form['content'])
        return flask.redirect(url)
    return dict(form=form)


@app.route('/api/v1/pastes', methods=['POST'])
def create_paste():
    form = forms.PasteForm(csrf_enabled=False)
    if form.validate_on_submit():
        rate_limit.throttle(flask.request)
        url = backend.write(flask.request.form['content'])
        return flask.redirect(url)
    raise exceptions.BadRequest('Missing paste content')


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


@app.errorhandler(exceptions.BadRequest)
def handle_bad_request(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(exceptions.RateLimitExceeded)
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
