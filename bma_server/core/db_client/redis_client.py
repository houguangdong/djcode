# -*- coding:utf-8 -*-
import redis


class RedisClient(object):
    def __init__(self, host="127.0.0.1", port=6379, password="", db=0):
        self.host = host
        self.port = port
        self.password = password
        self.redis = redis.StrictRedis(host=self.host, port=self.port, password=self.password, db=db)

    @property
    def get_redis_conn(self):
        return self.redis

    def modify_redis_db(self, new_db=0):
        """
        修改链接的redis库
        :param new_db: 新库的地址
        """
        self.redis = redis.StrictRedis(host=self.host, port=self.port, password=self.password, db=int(new_db))
        return self.redis