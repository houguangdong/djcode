#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/28 18:06


def import_by_name(name):
    tmp = name.split(".")
    module_name = ".".join(tmp[0:-1])
    obj_name = tmp[-1]
    module = __import__(module_name, globals(), locals(), [obj_name])
    return getattr(module, obj_name)