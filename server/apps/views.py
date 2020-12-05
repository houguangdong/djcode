# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rklib.utils import rkjson as json
from rklib.web.logic import gateway
from django.http import HttpResponse

# Create your views here.

def api(request):
    request_context = request._request_context
    result = gateway.process(request_context)
    return HttpResponse(result if isinstance(result, str) else json.dumps(result), content_type='application/json')


def login(request):
    rk_user = request._request_context.rk_user      # type:User
    isnew = 0 if rk_user.username is None else 1

    response = HttpResponse(json.dumps({'r': 0, 'isnew': isnew, 'msg': 'ok'}), content_type='application/json')
    return response