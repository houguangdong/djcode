#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 12:30
import time
from django.conf import settings
from rklib.auth import build_rkauth_signature


def get_rkauth_signature(rk_uid, openid, openkey, timestamp):
    """生成rkauth签名"""
    rkauth_fields = {}
    rkauth_fields['rk_uid'] = rk_uid
    rkauth_fields['openid'] = openid
    rkauth_fields['openkey'] = openkey
    rkauth_fields['ts'] = timestamp
    # rkauth_fields['APP_ID'] = settings.APP_ID
    rkauth_fields['SECRET_KEY'] = settings.SECRET_KEY

    return build_rkauth_signature(rkauth_fields)


def get_user_from_cookie(cookies):
    """验证rkauth签名，并且返回验证后的用户ID"""
    rkauth_signature = cookies.get('rkauth_token')

    rkauth_fields = {}
    rkauth_fields['rk_uid'] = cookies.get('rk_uid')
    rkauth_fields['openid'] = cookies.get('openid')
    rkauth_fields['openkey'] = cookies.get('openkey')
    rkauth_fields['ts'] = cookies.get('ts')
    # rkauth_fields['APP_ID'] = settings.APP_ID
    rkauth_fields['SECRET_KEY'] = settings.SECRET_KEY

    built_signature = build_rkauth_signature(rkauth_fields)

    if rkauth_signature == built_signature:
        return {'rk_uid': rkauth_fields['rk_uid'], 'openid': rkauth_fields['openid'], 'openkey': rkauth_fields['openkey'], 'ts': rkauth_fields['ts']}
    else:
        return None


def auth_cookie(request_context):
    """基于cookie的用户认证
    pass
    :param request_context:
    :return:
    """
    pass
    is_login = False
    # user_cookie = get_user_from_cookie(request_context.cookies)
    # print request_context.path
    # if request_context.path == '/':
    #     openid = request_context.params.get('openid')
    #     openkey = request_context.params.get('openkey')
    #
    #     if openid is None or openkey is None:
    #         return None
    #
    #     # cookie中的时间戳超过一个小时，强制重新认证
    #     if isinstance(user_cookie, dict) and ((int(time.time()) - int(user_cookie['ts'])) > 3600):
    #         user_cookie = None
    #
    #     if isinstance(user_cookie, dict) and openid == user_cookie['openid'] and openkey == user_cookie['openkey']:
    #         return user_cookie
    #     else:
    #         rk_uid = AccountMapping.get_user_id(openid)
    #         print rk_uid
    #         return {'rk_uid': rk_uid, 'openid': openid, 'openkey': openkey}
    # else:
    #     return user_cookie