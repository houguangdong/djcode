#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 20:36


def get_addr(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip