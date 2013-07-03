import flask


app = flask.Flask(__name__)
app.debug = True
app.secret_key = __name__


@app.route('/')
def index():
    if 'username' in flask.session:
        return 'Logged in as %s' % flask.escape(flask.session['username'])
    return 'You are not logged in'


@app.route('/hello')
def hello():
    return flask.render_template('hello.html')


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if flask.request.method == 'POST':
        if flask.request.form['username']:
            flask.session['username'] = flask.request.form['username']
            login_url = flask.url_for(
                'show_user_profile',
                username=flask.request.form['username'])
            flask.flash(
                'Welcome, %s' % flask.escape(flask.session['username']))
            return flask.redirect(login_url)
        else:
            app.logger.warning('Invalid login')
            error = 'Invalid username'

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return flask.render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    flask.session.pop('username', None)
    return flask.redirect(flask.url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return flask.render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run()
