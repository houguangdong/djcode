#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/13 17:08

from config.login_conf import login_limit
from core.views import AccView
from app.models import Account
import json


class LoginCheck(AccView):
    '''
    登录验证        平台(1-to-m) > server (1-to-m) > channel(user身上)
    '''

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        response_dic = {
            'status': 'success',
            'code': '0',
        }

        parameter_info = self.parameters

        open_id = parameter_info['open_id']
        acc_info = Account.search_open_id(open_id)
        if not acc_info:
            acc_info = Account.install(
                open_id, parameter_info['platformId'], parameter_info["channelId"],
                parameter_info["serverId"], parameter_info.get('uid', ''), parameter_info['os_type'],
                parameter_info['app_version'], parameter_info['build_version'], parameter_info['res_version'],
                parameter_info['age'], parameter_info['istourist'], 0
            )
            return self.HttpResponse(json.dumps(response_dic))

        # 游客登录
        if int(acc_info['istourist']) == 1:
            if int(acc_info['online_time']):                            # 玩过游戏
                response_dic.update({'status': 'fail', 'code': 1})
                return self.HttpResponse(response_dic)
            else:                                                       # 没玩
                return self.HttpResponse(response_dic)
        else:
            if parameter_info['age'] in login_limit['age_limit']:
                if int(acc_info['online_time']) >= login_limit['online_limit']:
                    response_dic.update({'status': 'fail', 'code': 2})
                    return self.HttpResponse(response_dic)
                if
