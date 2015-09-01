import json

from pasteraw import app


def _format(message, **kwargs):
    if not kwargs:
        return message

    encoded = [
        '%s=%s' % (k, json.dumps(v))
        for k, v in kwargs.iteritems()]
    return '%s (%s)' % (message, ', '.join(encoded))


def debug(message, **kwargs):
    app.logger.debug(_format(message, **kwargs))


def info(message, **kwargs):
    app.logger.info(_format(message, **kwargs))


def warning(message, **kwargs):
    app.logger.warning(_format(message, **kwargs))


def error(message, **kwargs):
    app.logger.error(_format(message, **kwargs))


def critical(message, **kwargs):
    app.logger.critical(_format(message, **kwargs))


def exception(message, **kwargs):
    app.logger.exception(_format(message, **kwargs))
