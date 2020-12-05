#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/31 11:01

try:
    import cPickle as pickle
except ImportError:
    import pickle

import sys

from rklib.client.redis_cli import RedisClient, parse_setting
from rklib.model.engine import StorageEngine


class RedisEngine(StorageEngine):

    def __init__(self):
        self.servers = None
        self.default_timeout = 0
        self.max_connections = 0
        self.client = None
        self.debug = False

    def configure(self, cfg_value):
        StorageEngine.configure(self, cfg_value)
        self.servers = cfg_value.get("servers")
        self.default_timeout = cfg_value.get("default_timeout", 120)
        self.max_connections = cfg_value.get("max_connections", 100)
        setting_dict = parse_setting(self.servers)
        setting_dict.update({'password': cfg_value.get('password', None)})
        self.client = RedisClient(max_connections=self.max_connections, default_timeout=self.default_timeout, **setting_dict)
        # redis_manager.connection_setup(self.servers, self.max_connections, self.default_timeout)
        self.debug = cfg_value.get("debug", False)

    def __get_client(self, db=None):
        # def __get_client(self, pkey):
        """根据key取得redis client
        @param pkey:
        @return:
        """
        # client = redis_manager.get_connection(pkey)
        if db is not None and self.client.connection_settings['db'] != db:
            self.client.connection_settings['db'] = db
        client = self.client.get_redis()
        return client

    def get_data(self, model_cls, pkey):
        '''
        model_cls:  model类对象
        pkey:       model对象主键
        :param model_cls:
        :param pkey:
        :return:
        '''
        # client = self.__get_client(pkey)
        client = self.__get_client()
        cache_key = model_cls.generate_cache_key(pkey)
        val = client.get(cache_key)
        if val is None:
            return None
        data = pickle.loads(val)
        if self.debug:
            print >> sys.stderr, "[DEBUG]", "key: %s, cache_key: %s" % (pkey, cache_key)
            print >> sys.stderr, "[DEBUG]", "value: %s" % data
        return data

    def get_multi_data(self, model_cls, *pkeys):
        '''
        :param model_cls:
        :param pkeys:
        :return:
        '''
        client = self.__get_client()
        cache_keys = [model_cls.generate_cache_key(pkey) for pkey in pkeys]
        if not cache_keys:
            return []
        return [pickle.loads(val) if val else None for val in client.mget(cache_keys)]

    def put_data(self, model_cls, pkey, data, create_new):
        '''
        :param model_cls:
        :param pkey:
        :param data:
        :param create_new:
        :return:
        '''
        client = self.__get_client()
        cache_key = model_cls.generate_cache_key(pkey)
        val = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        flag = client.set(cache_key, val)
        return flag

    def reset(self):
        # self.client.close()
        pass

    def delete_data(self, model_cls, pkey):
        '''
        """删除数据,redis更新状态为MMODE_STATE_DEL
        :param model_cls:
        :param pkey:
        :return:
        '''
        client = self.__get_client()
        cache_key = model_cls.generate_cache_key(pkey)
        flag = client.delete(cache_key)
        return flag

    def put_expire_date(self, model_cls, pkey, data, expire_time, create_new):
        """
        :param model_cls:
        :param pkey:
        :param data:
        :param expire_time:
        :param create_new:
        :return:
        """
        client = self.__get_client()
        cache_key = model_cls.generate_cache_key(pkey)
        val = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        client.set(cache_key, val)
        flag = client.expire(cache_key, expire_time)
        return flag