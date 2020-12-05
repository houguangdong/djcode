#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 11:10

try:
    import cPickle as pickle
except ImportError:
    import pickle

import binascii
from rklib.client.mcache import MemcacheClient
from rklib.model.engine import StorageEngine
import sys


class MemcacheEngine(StorageEngine):

    def __init__(self):
        self.servers = None
        self.default_timeout = 0
        self.client = None
        self.debug = False

    def configure(self, cfg_value):
        StorageEngine.configure(self, cfg_value)
        self.servers = cfg_value.get("servers")
        self.default_timeout = cfg_value.get("default_timeout", 0)
        self.client = MemcacheClient(self.servers, self.default_timeout)

        self.debug = cfg_value.get("debug", False)

    def get_data(self, model_cls, pkey):
        """
        :param model_cls: model类对象
        :param pkey: model对象主键
        :return:
        """
        cache_key = model_cls.generate_cache_key(pkey)
        val = self.client.get(cache_key)
        if val is None:
            return None
        data = pickle.loads(binascii.unhexlify(val))
        if self.debug:
            print >> sys.stderr, "[DEBUG GET]", "cache key:", cache_key
            print >> sys.stderr, "[DEBUG GET]", "cache value", repr(data)

        return data

    def put_data(self, model_cls, pkey, data, create_new):
        cache_key = model_cls.generate_cache_key(pkey)
        val = binascii.hexlify(pickle.dumps(data, pickle.HIGHEST_PROTOCOL))
        if create_new:
            flag = self.client.add(cache_key, val, self.default_timeout)
            if not flag:
                raise Exception('memcache client add failure, cache key: %s' % cache_key)
            if self.debug:
                print >> sys.stderr, "[DEBUG ADD]", "cache key:", cache_key
                print >> sys.stderr, "[DEBUG ADD]", "cache value", repr(data)
        else:
            flag = self.client.set(cache_key, val, self.default_timeout)
            if not flag:
                raise Exception('memcache client set failure, cache key: %s' % cache_key)
            if self.debug:
                print >> sys.stderr, "[DEBUG SET]", "cache key:", cache_key
                print >> sys.stderr, "[DEBUG SET]", "cache value", repr(data)

    def reset(self):
        self.client.close()

    def delete_data(self, model_cls, pkey):
        cache_key = model_cls.generate_cache_key(pkey)
        flag = self.client.delete(cache_key)
        if flag == 0:
            raise Exception('memcache client delete failure, cache key: %s' % cache_key)

        if self.debug:
            print >> sys.stderr, "[DEBUG DEL]", "cache key:", cache_key