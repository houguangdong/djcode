#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/14 18:29

from rklib.client.redis_cli import parse_setting
from rklib.client.redis_queue_cli import RedisQueue

try:
    import cPickle as pickle
except ImportError:
    import pickle
from rklib.model.engine import StorageEngine


class RedisQueuesEngine(StorageEngine):

    def __init__(self):
        self.servers = None
        self.default_timeout = 0
        self.max_connections = 0
        self.client = None
        self.debug = False
        self.redis_queue = None

    def configure(self, cfg_value):
        '''
        需要重新设计配置
        :param cfg_value:
        :return:
        '''
        # StorageEngine.configure(self, cfg_value)
        # self.servers = '%s:%s:%s' % (cfg_value['default_ip'], cfg_value['default_port'], cfg_value['db']) \
        #         if not cfg_value['override']['flag'] else '%s:%s:%s' % \
        #     (cfg_value['override']['default_ip'], cfg_value['override']['default_ip'], cfg_value['db'])
        # # self.servers = cfg_value.get("servers")
        # self.default_timeout = cfg_value.get("default_timeout", 5)
        # self.max_connections = cfg_value.get("default_max_connections", 100)
        # redis_kwargs = parse_setting(self.servers)
        # password = cfg_value['default_password'] if not cfg_value['override']['flag'] else cfg_value['override']['password']
        # redis_kwargs.update({"password": password})
        # self.redis_queue = RedisQueue('info', 'info', self.max_connections, self.default_timeout, **redis_kwargs)
        # self.debug = cfg_value.get("debug", False)

    def put_data(self, model_cls, pkey, data, create_new):
        cache_key = model_cls.generate_cache_key(pkey)
        # val = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        flag = self.redis_queue.put(cache_key)
        if self.debug:
            import sys
            print >> sys.stderr, "[DEBUG]", "queuescache_key: %s" % cache_key
        return flag

    def put_list(self, list_key, add_value):
        """
        往list中添加数据
        :param list_key: list名字
        :param add_value:  添加的数据
        """
        pass

    def update_redis_db(self, db):
        redis_obj = self.redis_queue.get_conn()
        redis_obj.connection_pool.connection_kwargs['db'] = db
        redis_obj.connection_pool.connection_class.description_format % redis_obj.connection_pool.connection_kwargs
        return

    def get_conn(self):
        return self.redis_queue.get_conn()