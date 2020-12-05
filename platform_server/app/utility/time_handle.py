# -*- coding:utf-8 -*-

import arrow


def get_current_time():
    """
    获取当前时间
    """
    return int(arrow.utcnow().to("Asia/Shanghai").timestamp)