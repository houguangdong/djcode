#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/13 19:41

import arrow

zone_tz = "Asia/Shanghai"


def get_current_time():
    """
    获取当前时间
    """
    return int(arrow.utcnow().to("Asia/Shanghai").timestamp)


def int_format_time(times):
    """
    时间戳格式化
    :param times: 时间戳
    """
    import arrow
    if times is not None and times != "":
        return arrow.get(str(times)).to(zone_tz).format('YYYY-MM-DD HH:mm:ss')
    return ""


def time_open_time(curr_time, bday):
    """
    两个日期相差几天
    :param curr_time: 时间戳
    :return: :type int
    """
    import datetime
    days_num = arrow.get(curr_time).to(zone_tz) - arrow.get(bday).to(zone_tz)
    days_num = days_num + datetime.timedelta(hours=8)
    return days_num.days


def str_change_timestamp(str_time, is_float=False):
    """
    字符串转时间戳
    :return: int
    """
    if is_float:
        return arrow.get(str_time).to(zone_tz).float_timestamp
    return arrow.get(str_time).to(zone_tz).timestamp