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

    def __init__(self, get_response=None):
        super(RKAuthMiddleware, self).__init__(get_response)
        self.rk_user = None     # type: User
        self.data = {}
        self.result = {}

    def process_request(self, request):
        """用户认证中间件"""
        request_context = request._request_context

        if request_context.path.startswith('/test'):
            return

        if request_context.path.startswith('/payment'):
            return

        if request_context.path.startswith('/agg_payment'):
            return

        if request_context.path.startswith('/manage'):
            return

        if request_context.path.startswith('/account'):
            return

        if request_context.path.startswith('/server_mba_api'):
            return

        if request_context.path.startswith('/admin'):
            return

        status, rk_user = User._install(request_context)

        if status in [-1010, -1011, -1012, -1020, -1021, -1022, -1301]:
            return HttpResponse(json.dumps({'r': status, 'msg': 'user is None'}))

        if status is None:
            return HttpResponse(json.dumps({'r': -1030, 'msg': 'user is None'}))

        if not isinstance(rk_user, User):
            return HttpResponse(json.dumps({'r': -1001, 'msg': 'user is None'}))

        pass

        request_context.rk_user = rk_user
        return

    def get_parameter(self, name, default=None):
        return ""