#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/29 11:33


class StorageEngine(object):

    def configure(self, cfg_value):
        # 该存储方式是否可以给GET方法提供数据. 例如只存key不存value的tt就不能为GET提供数据
        self.support_get = cfg_value.get("support_get", True)

    def get_data(self, model_cls, pkey):
        """
        model_cls:  model类
        pkey:       model对象主键
        """
        raise NotImplementedError

    def put_data(self, model_cls, pkey, data, create_new):
        """
        model_cls:  model类
        pkey:       model对象主键
        data:       model对象dump之后的结果(dict类型)
        create_new: 是否创建新记录(INSERT or UPDATE)
        """
        raise NotImplementedError

    def reset(self):
        """重置存储相关状态（比如关闭数据库链接，关闭memcached链接）
        """
        pass

    def delete_data(self, model_cls, pkey):
        """
        model_cls:  model类
        pkey:       model对象主键
        """
        raise NotImplementedError