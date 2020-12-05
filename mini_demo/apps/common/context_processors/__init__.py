#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 22:58

from django.conf import settings as _settings


def settings(request):
    return {'settings': _settings}