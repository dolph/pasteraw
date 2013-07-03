import flask


app = flask.Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    app.run()
