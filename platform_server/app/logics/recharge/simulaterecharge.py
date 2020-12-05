# -*- coding:utf-8 -*-
import requests
import json
import arrow
from config.platform_mapping import platform
from core.view import View


class SimulateRecharge(View):
    def get(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    def do(self, request, *args, **kwargs):

        parameter_info = self.parameters

        print parameter_info

        roleId = parameter_info["roleId"]                   # 角色ID
        serverId = int(parameter_info["serverId"])          # 区服
        orderNo = parameter_info["orderNo"]                 # 订单编号
        rechargeId = int(parameter_info["rechargeId"])      # 充值礼包ID

        host = platform["server"][serverId]["host"]
        port = platform["server"][serverId]["port"]
        url = "http://%s:%s/server_mba_api/simulaterecharge" % (host, port)
        parameters = {"roleId": roleId, "orderNo": orderNo, "rechargeId": rechargeId}

        print url
        print parameters

        """
        {"roleName": "\u547c\u5ef6\u96c5\u9633", "vipLevel": "2", "level": "1"}
        """

        utc_now = arrow.utcnow()
        today = utc_now.to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')

        dic = {
            'status': 'ok',
            'code': 1,
            'info': '',
            'roleName': '',
            'rewardTime': today,
            'vipLevel':'',
            'level':''
        }

        ret = requests.post(url, parameters)
        if ret.status_code != 200:
            dic.update({"status": "fail", "code": 0})
            return self.HttpResponse(json.dumps(dic))
        ret_body = json.loads(ret.text)
        dic.update(ret_body)

        print dic
        return self.HttpResponse(json.dumps(dic))