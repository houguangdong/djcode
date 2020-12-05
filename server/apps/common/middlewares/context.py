#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/14 20:42

from django.utils.deprecation import MiddlewareMixin
from rklib.model import storage_context
from rklib.web.logic.django import DjangoRequestContext


class RKContextMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request._request_context = DjangoRequestContext(request)    # 初始化web框架无关的request_context实例
        storage_context.clear()                                     # 重置storage_context

    def process_response(self, request, response):
        storage_context.save()                                      # 统一保存storage_context中的数据对象

        return response