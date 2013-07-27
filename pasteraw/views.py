import os

import flask

from pasteraw import app
from pasteraw import backend
from pasteraw import decorators
from pasteraw import forms


@app.route('/', methods=['POST', 'GET'])
@decorators.templated()
def index():
    form = forms.PasteForm()
    if form.validate_on_submit():
        paste_id = backend.save(flask.request.form['content'])
        return flask.redirect(flask.url_for('show_paste', paste_id=paste_id))
    return dict(form=form)


@app.route('/<paste_id>')
def show_paste(paste_id):
    content = backend.load(paste_id)
    if content is None:
        flask.abort(404)
    return content, 200, {'Content-Type': 'text/plain'}


@app.errorhandler(404)
def not_found(error):
    return flask.render_template('not_found.html'), 404


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/x-icon')
