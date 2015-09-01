from __future__ import unicode_literals

import fcntl
import json
import time

try:
    import anydbm as dbm
except ImportError:
    import dbm

from pasteraw import app
from pasteraw import exceptions


MAX_THROTTLES = 3


class DBMContext(object):
    """A context manager to access a file in a concurrent-safe manner."""
    __slots__ = ('filename', 'mode', 'readonly', 'lockfile', 'db')

    def __init__(self, filename, readonly=False, mode=0o644):
        self.filename = filename
        self.mode = mode
        self.readonly = readonly
        self.lockfile = open(filename + '.lock', 'w+b')

    def __enter__(self):
        fcntl.lockf(
            self.lockfile.fileno(),
            fcntl.LOCK_SH if self.readonly else fcntl.LOCK_EX)
        self.db = dbm.open(self.filename, flag='c', mode=self.mode)
        return self.db

    def __exit__(self, exval, extype, tb):
        self.db.close()
        fcntl.lockf(self.lockfile.fileno(), fcntl.LOCK_UN)
        self.lockfile.close()


def _serialize(t):
    """Converts a tuple to a string."""
    return json.dumps(t, separators=(',', ':'))


def _deserialize(s):
    """Converts a string to a tuple."""
    return tuple(json.loads(s))


def throttle(request):
    if app.config['TESTING']:
        # ignore rate limiting in debug mode
        return True

    # try the actual remote address passed through by nginx first
    ip = str(request.headers.get('X-Real-IP', request.remote_addr))

    rate = 3.0  # unit: messages
    per = 60.0  # unit: seconds

    with DBMContext(app.config['RATE_LIMIT_DBM_FILE']) as db:
        db.setdefault(ip, _serialize((rate, time.time(), 0)))
        allowance, last_check, throttle_count = _deserialize(db[ip])

        if throttle_count > MAX_THROTTLES:
            app.logger.warning('Blocking %s' % ip)
            raise exceptions.RateLimitExceeded('Rate limit exceeded.')

        current = time.time()
        time_passed = current - last_check
        last_check = current
        allowance += time_passed * (rate / per)

        if allowance > rate:
            # A lot of time has passed since we last saw this IP, reset their
            # throttle.
            allowance = rate

        if allowance < 1.0:
            throttle_count += 1
            db[ip] = _serialize((allowance, last_check, throttle_count))

            retry_after = (1.0 - allowance) * (per / rate)
            app.logger.warning(
                'Throttling %s (allowance=%s, last_check=%s, '
                'throttle_count=%s, retry_after=%s)' % (
                    ip, allowance, last_check, throttle_count, retry_after))
            raise exceptions.RateLimitExceeded(
                'Rate limit exceeded. Retry after %s seconds.' % retry_after)

        allowance -= 1
        db[ip] = _serialize((allowance, last_check, throttle_count))

        app.logger.warning(
            'Allowing %s (allowance=%s, last_check=%s, throttle_count=%s)' % (
                ip, allowance, last_check, throttle_count))

        return True
