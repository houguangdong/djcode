# -*- coding:utf-8 -*-
from config import data_config
from core.db_client.redis_client import RedisClient

REDIS_HOST = data_config.redis_conn_info["host"]
REDIS_PORT = data_config.redis_conn_info["port"]
REDIS_PASSWORD = data_config.redis_conn_info["password"]

gift_redis = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD,
                         data_config.redis_app_conn_info["gift_redis"]["db"]).redis
