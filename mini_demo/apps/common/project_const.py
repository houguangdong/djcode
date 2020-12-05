#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 10:14

from apps.common import const

# new_user_key
const.NEWUSERKEY = "new_user_id"
const.NEWUSERIDSTART = 99999

const.PLAY_AGE_STAGE = [18, 16, 8, 0, -1]           # 玩家年龄阶段
const.PLAY_TIME = 90 * 60                           # 小于18岁 每日不能超过90分钟
const.PLAY_LIMIT = [22 * 3600, 8 * 3600]            # 每日22:00-8:00不得登陆游戏
const.RECHARGE_LIMIT = {                            # 未成年充值限制
    18: [-1, -1],
    16: [100, 400],
    8: [50, 200],
    0: [0, 0],
    -1: [0, 0]
}