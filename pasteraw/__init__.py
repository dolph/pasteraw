import flask


app = flask.Flask(__name__, instance_relative_config=True)

# start with a default configuration
app.config.from_object('pasteraw.config')

# override defaults with instance-specific configuration
app.config.from_pyfile('pasteraw_config.py', silent=True)

raven_url = app.config.get('RAVEN_URL', None)
if raven_url is not None:
    import raven
    app = raven.middleware.Sentry(app, client=raven.Client(raven_url))


import pasteraw.views  # flake8: noqa
