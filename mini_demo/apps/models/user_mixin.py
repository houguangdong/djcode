#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/17 14:23

"""
UserMixin.py
"""

class UserMixin(object):
    """
        Attributes:
            _game_info: 用户游戏信息
    """

    def __init__(self):
        self.uid = None
        self._game_info = None
        pass