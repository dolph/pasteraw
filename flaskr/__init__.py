import flask


app = flask.Flask(__name__)
app.secret_key = __name__


import flaskr.views  # flake8: noqa
