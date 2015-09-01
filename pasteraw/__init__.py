import logging
import logging.handlers
import os

import flask


app = flask.Flask(__name__, instance_relative_config=True)

# start with a default configuration
app.config.from_object('pasteraw.config')

# override defaults with custom configuration
app.config.from_pyfile('/etc/pasteraw.conf.py', silent=True)

formatter = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)03d] pid=%(process)d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

if app.debug:
    for handler in app.logger.handlers:
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
else:
    # enable logging to file in production
    file_handler = logging.handlers.RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=1000000,
        backupCount=3)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


import pasteraw.views  # flake8: noqa
