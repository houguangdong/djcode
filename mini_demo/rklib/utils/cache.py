#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 10:49
from rklib.core import app
from rklib.client.mcache import MemcacheClient
from rklib.client.redis_cli import RedisClient

memcache_config = app.cache_config.memcache

cache = MemcacheClient(memcache_config["servers"], memcache_config["default_timeout"])


redis_cache = None



