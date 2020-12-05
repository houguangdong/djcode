#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/17 00:47

import uuid


def get_uuid():
    return uuid.uuid1().get_hex()