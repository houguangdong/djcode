#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 10:08

from django.http import HttpResponse


def get_response(content='', mimetype=None, status=None, content_type=None):
    return HttpResponse(content, mimetype, status, content_type)