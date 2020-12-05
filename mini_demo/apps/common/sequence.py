#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 09:56

from rklib.core import app
from apps.common.project_const import const
from rklib.utils.cache import redis_cache
from django.conf import settings


def generate():
    new_user_id = redis_cache.incr(const.NEWUSERKEY)
    return "s%s.%s" % (settings.SERVER_NUMBER, new_user_id)
    # return "%s" % new_user_id


# def generate():
#     engine = app.get_engine("mysql")
#     lastrowid = engine.master_execute("UPDATE sequence SET id=LAST_INSERT_ID(id+1)")
#     return str(int(lastrowid))