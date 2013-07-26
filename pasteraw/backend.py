import zlib

import redis

from pasteraw import base36


DB = redis.StrictRedis(host='localhost', port=6379, db=0)


def save(content):
    compressed = zlib.compress(content)
    key = base36.unique()
    DB.set(key, compressed)
    return key


def load(key):
    compressed = DB.get(key)
    if compressed is None:
        return None
    content = zlib.decompress(compressed)
    return content
