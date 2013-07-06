import flask

from flaskr import app
from flaskr import forms


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flask.session['username'] = flask.request.form['username']
        flask.flash(
            'Welcome, %s' % flask.escape(flask.session['username']))
        return flask.redirect(flask.url_for('index'))

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return flask.render_template('login.html', form=form)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    flask.session.pop('username', None)
    flask.flash('You were logged out')
    return flask.redirect(flask.url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return flask.render_template('not_found.html'), 404
