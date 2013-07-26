import zlib

import redis

import pasteraw
from pasteraw import base36


def make_redis(app):
    return redis.StrictRedis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'])


REDIS = make_redis(pasteraw.app)


def save(content):
    compressed = zlib.compress(content)
    key = base36.unique()
    REDIS.set(key, compressed)
    return key


def load(key):
    compressed = REDIS.get(key)
    if compressed is None:
        return None
    content = zlib.decompress(compressed)
    return content
