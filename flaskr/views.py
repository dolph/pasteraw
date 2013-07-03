import flask


app = flask.Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return flask.render_template('hello.html')


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


if __name__ == '__main__':
    app.run()
