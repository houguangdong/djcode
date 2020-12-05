#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 15:02
from rklib.model.engine import StorageEngine

dummy_storage = {}


class DummyEngine(StorageEngine):

    def configure(self, cfg_value):
        StorageEngine.configure(self, cfg_value)

    def get_data(self, model_cls, pkey):
        cache_key = model_cls.generate_cache_key(pkey)
        return dummy_storage.get(cache_key, None)

    def put_data(self, model_cls, pkey, data, create_new):
        cache_key = model_cls.generate_cache_key(pkey)
        dummy_storage[cache_key] = data

    def delete_data(self, model_cls, pkey):
        cache_key = model_cls.generate_cache_key(pkey)
        try:
            del dummy_storage[cache_key]
        except:
            pass