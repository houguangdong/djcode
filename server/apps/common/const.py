#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 10:05

from __future__ import print_function
import sys


class _Const:

    def __init__(self):
        pass

    class ConstError(TypeError):

        def __init__(self, message):
            print(message)

def __setattr__(self, key, value):
    """
    @param self:
    @type self: _Const
    @param key:
    @param value:
    @return:
    """
    if self.__dict__.get(key):
        raise self.ConstError("constant reassignment error!")
    self.__dict__[key] = value


def __getattr__(self, key):
    if not self.__dict__.get(key):
        raise self.ConstError("constant get error!")
    return self.key


sys.modules[__name__] = _Const()