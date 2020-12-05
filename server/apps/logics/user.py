#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 13:46

from apps.models.user import User


def login(context):
    context.result["test"] += " login"
    context.result["r"] = 0
    context.result["msg"] = "ok"


def get(context):
    uid = context.get_parameter("uid")
    u = User.get(uid)
    context.result["r"] = 0
    context.result["msg"] = "ok"
    context.result["uid"] = uid
    context.result["username"] = u.username


def get_config(context):
    id = context.get_parameter('id')
    from apps.models.xlsx_config import XLSXConfig

    config = XLSXConfig.get('item')
    print config.__dict__

    print id

    # context.result["store_config"] = game_config.item_data.get(str(id))