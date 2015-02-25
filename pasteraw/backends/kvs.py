import hashlib
import zlib

import redis

import pasteraw
from pasteraw import base36


REDIS = redis.StrictRedis(
    host=pasteraw.app.config['REDIS_HOST'],
    port=pasteraw.app.config['REDIS_PORT'],
    db=pasteraw.app.config['REDIS_DB'])


def save(content):
    content = content.encode('utf-8')
    hex_key = hashlib.sha1(content).hexdigest()
    key = base36.re_encode(hex_key, starting_base=16)
    if load(key) is not None:
        return key
    else:
        compressed = zlib.compress(content)
        REDIS.set(key, compressed)
        return key


def load(key):
    compressed = REDIS.get(key)
    if compressed is None:
        return None
    content = zlib.decompress(compressed)
    content = content.decode('utf-8')
    return content
