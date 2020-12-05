# -*- coding:utf-8 -*-
from core.utils.redis_connet import gift_redis


class RedisHash(object):
    def __init__(self, hash_name=""):
        self._name = hash_name
        self.redis_conn = gift_redis.get_redis_conn

    @property
    def name(self):
        return self._name + "%s" if self._name else "%s"

    def hset(self, name, key, value):
        return self.redis_conn.hset(self.name % name, key, value)

    def hget(self, name, key):
        return self.redis_conn.hget(self.name % name, key)

    def hgetall(self, name):
        return self.redis_conn.hgetall(self.name % name)

    def hmset(self, name, mapping):
        return self.redis_conn.hmset(self.name % name, mapping)

    def hmget(self, name, keys, *args):
        return self.redis_conn.hmget(self.name % name, keys, *args)

    def hdel(self, name, *key):
        return self.redis_conn.hdel(self.name % name, *key)

    def hincyby(self, name, key, amount=1):
        return self.redis_conn.hincrby(self.name % name, key, amount)