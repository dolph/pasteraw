import os

import flask


app = flask.Flask(__name__, instance_relative_config=True)

# start with a default configuration
app.config.from_object('pasteraw.config')

# override defaults with custom configuration
app.config.from_pyfile('/etc/pasteraw.conf.py', silent=True)

# enable logging in production
if not app.debug:
    import logging
    file_handler = logging.FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


import pasteraw.views  # flake8: noqa
