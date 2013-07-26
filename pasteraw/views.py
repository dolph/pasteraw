import os

import flask

from pasteraw import app
from pasteraw import decorators
from pasteraw import forms


@app.route('/')
@decorators.templated()
def index():
    pass


@app.route('/login', methods=['POST', 'GET'])
@decorators.templated()
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flask.session['username'] = flask.request.form['username']
        flask.flash(
            'Welcome, %s' % flask.escape(flask.session['username']))
        return flask.redirect(flask.url_for('index'))

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return dict(form=form)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    flask.session.pop('username', None)
    flask.flash('You were logged out')
    return flask.redirect(flask.url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return flask.render_template('not_found.html'), 404


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')
