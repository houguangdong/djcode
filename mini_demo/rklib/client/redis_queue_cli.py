#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/14 18:30
try:
    import cPickle as pickle
except ImportError:
    import pickle
from rklib.client.redis_cli import RedisClient


class RedisQueue(object):

    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace, max_connections, default_timeout, **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        redis_client = RedisClient(max_connections, default_timeout, **redis_kwargs)
        self.__db = redis_client.get_redis()
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        # item = pickle.dumps(item, pickle.HIGHEST_PROTOCOL)
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

    def clear_queue(self):
        """
        clear queue
        :return:
        """
        while self.qsize() > 0:
            self.get()

    def get_conn(self):
        return self.__db