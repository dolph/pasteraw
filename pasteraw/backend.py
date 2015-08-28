import hashlib
import os
import tempfile

import flask

from pasteraw import app
from pasteraw import base36
from pasteraw import cdn


class InvalidKey(ValueError):
    pass


class NotFound(Exception):
    pass


def _validate_key(key):
    """Keys must be base36 encoded."""
    if not base36.validate(key):
        raise InvalidKey(key)
    return True


def _local_path(key):
    _validate_key(key)
    return os.path.expanduser('%s/%s' % (app.config['PASTE_DIR'], key))


def local_url(key):
    _validate_key(key)
    return flask.url_for('show_paste', paste_id=key)


def remote_url(key):
    _validate_key(key)
    return '%s/%s' % (app.config['CDN_ENDPOINT'], key)


def read(key):
    """Read the content from the local system.

    If the file is not local (for example, it was uploaded to a CDN), this will
    raise NotFound.

    """
    path = _local_path(key)
    if not os.path.isfile(path):
        raise NotFound('Not a local file: %s' % path)
    with open(path, 'r') as f:
        return f.read()


def write(content):
    """Write the content to a backend, and get a URL for it."""
    content = content.encode('utf-8')
    hex_key = hashlib.sha1(content).hexdigest()
    key = base36.re_encode(hex_key, starting_base=16)

    if cdn.upload(key, content):
        app.logger.info('Uploaded paste to CDN: %s' % key)
        return remote_url(key)

    # ensure the PASTE_DIR exists
    if app.config['PASTE_DIR'] is None:
        app.config['PASTE_DIR'] = tempfile.mkdtemp(prefix='pasteraw-')
        app.logger.info('PASTE_DIR not set; created temporary dir: %s' %
                        app.config['PASTE_DIR'])
    elif not os.path.isdir(app.config['PASTE_DIR']):
        msg = 'Directory does not exist: %s' % app.config['PASTE_DIR']
        app.logger.info(msg)
        raise IOError(msg)

    # CDN failed for whatever reason; write to a local file instead.
    path = _local_path(key)
    with open(path, 'w') as f:
        f.write(content)
    app.logger.info('Wrote paste to local filesystem: %s' % key)
    return local_url(key)
