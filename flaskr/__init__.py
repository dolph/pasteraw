import flask


app = flask.Flask(__name__, instance_relative_config=True)

# start with a default configuration
app.config.from_object('flaskr.config')

# override defaults with instance-specific configuration
app.config.from_pyfile('flaskr_config.py', silent=True)


import flaskr.views  # flake8: noqa
