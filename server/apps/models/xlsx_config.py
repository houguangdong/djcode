#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 13:50

from rklib.model import BaseModel


class XLSXConfig(BaseModel):
    """游戏配置信息

    Attributes:
        config_name: 配置名称 str
        config_value: 配置信息 dict
    """
    def __init__(self, config_name=None):
        """初始化游戏配置信息

        Args:
            config_name: 配置名称
        """
        BaseModel.__init__(self)

        self.config_name = config_name
        self.config_value = {}