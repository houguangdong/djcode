#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 20:44

import hashlib
import re

# from rklib.utils.trie_tree import


def str_change_md5(str_key):
    """
    根据参数算出md5值
    :param str_key: 转md5字符串
    :return: md5值
    """
    md5_obj = hashlib.md5()
    md5_obj.update(str_key)
    md5_val = md5_obj.hexdigest()
    return md5_val