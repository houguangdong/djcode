#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/31 11:02
import redis

from rklib.utils.hash_ring import HashRing


def parse_setting(setting):
    '''
    解析配置
    :param setting:
    :return:
    '''
    host, port, db = setting.split(':')
    host = str(host)
    port = int(port)
    db = int(db)
    return dict(host=host, port=port, db=db)


class RedisClient(object):

    def __init__(self, max_connections, default_timeout, **kwargs):
        kwargs['connection_pool'] = redis.BlockingConnectionPool(max_connections, default_timeout, **kwargs)
        self.connection_settings = kwargs

    def get_redis(self):
        return redis.StrictRedis(**self.connection_settings)

    def update(self, d):
        self.connection_settings.update(d)


class RedisManager(object):

    def __init__(self):
        self.connection_settings = None
        self.connections = {}
        self.hash_ring = None

    def connection_setup(self, connection_settings, max_connections, default_timeout):
        """
        连接安装
        :param connection_settings: 配置
        :param max_connections: 最大连接数
        :param default_timeout: 默认超时时间
        :return:
        """
        self.hash_ring = HashRing(connection_settings)
        for setting in connection_settings:
            setting_dict = parse_setting(setting)
            client = RedisClient(max_connections, default_timeout, **setting_dict)
            self.connections[setting] = client
        self.connection_settings = connection_settings

    def get_connection(self, key):
        node = self.hash_ring.get_node(key)
        if node and node in self.connections.keys():
            client = self.connections[node]
            return client.get_redis()
        return None

    def flushall(self, key):
        connection = self.get_connection(key)
        if connection:
            connection.flushall()


redis_manager = RedisManager()