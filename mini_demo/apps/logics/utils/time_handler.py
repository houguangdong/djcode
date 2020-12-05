#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/17 14:28

from datetime import datetime
import arrow

zone_tz = "Asia/Shanghai"


def get_day_end_time(times=None):
    """
    根据times获取当天结束时间，如果为None则为今天的结束时间
    """
    if times is None:
        return int(arrow.utcnow().to(zone_tz).ceil("day").timestamp)
    else:
        return int(arrow.get(times).to(zone_tz).ceil("day").timestamp)


def get_day_start_time(times=None):
    """
    根据times获取当天开始时间，如果为None则为今天的开始时间
    """
    if times is None:
        return int(arrow.utcnow().to(zone_tz).floor("day").timestamp)
    else:
        return int(arrow.get(times).to(zone_tz).floor("day").timestamp)


def check_same_day(times):
    """
    根据时间戳判断是否为同一天
    :param times: 时间戳
    """
    if get_day_end_time(times) != get_day_end_time():
        return False
    return True


def get_current_time(is_float=False):
    """
    获取当前的时间
    :param is_float: 是否是浮点型
    :return:
    """
    if is_float:
        return arrow.utcnow().to(zone_tz).float_timestamp
    return int(arrow.utcnow().to(zone_tz).timestamp)