# -*- coding:utf-8 -*-
import arrow


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
        return arrow.get(str(times)).to("Asia/Shanghai").format('YYYY-MM-DD HH:mm:ss')
    return ""