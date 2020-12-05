#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 12:12
from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from apps.logics.utils.time_handler import get_current_time
from apps.common.project_const import const
from apps.models.user import User
from rklib.utils import rkjson as json


class RKAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """用户认证中间件"""
        request_context = request._request_context

        if request_context.path.startswith('/admin'):
            return

        rk_user = User._install(request_context)

        if not isinstance(rk_user, User):
            if request_context.path == 'api':
                pass
            else:
                return HttpResponse('user is None')

        request_context.rk_user = rk_user