# -*- coding:utf-8 -*-
from config.mapping_conf import platform_str_mapping
from core.views import ResetView
import json
from config.game_server_config import platform_server_info
import requests
import arrow


class SimulateRecharge(ResetView):
    """
    查询充值礼包列表
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters

        platformId = parameter_info["platformId"]  # 平台
        serverId = int(parameter_info["serverId"])  # 区服
        orderNo = parameter_info["orderNo"]  # 订单编号
        roleId = parameter_info["roleId"]  # 角色ID
        rechargeId = parameter_info["rechargeId"]  # 充值礼包ID
        sign = parameter_info["sign"]  # sign

        platformId = platform_str_mapping.get(platformId, platformId)

        utc_now = arrow.utcnow()
        today = utc_now.to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')

        dic = {
            'status': 'ok',
            'code': 1,
            'info': '',
            'roleName': '',
            'rewardTime': today
        }
        if not platform_server_info.get(platformId, None):  # 判断平台游戏服务器是否存在
            dic.update({"status": "fail", "code": 0})
            return self.HttpResponse(json.dumps(dic))

        platform_conf = platform_server_info[platformId]
        url = "http://%s:%s/platform_server/simulaterecharge" % (platform_conf["host"], platform_conf["port"])
        send_parameter = {
            "serverId": serverId,
            "orderNo": orderNo,
            "roleId": roleId,
            "rechargeId": rechargeId,
        }
        http_info = requests.post(url, send_parameter)
        if http_info.status_code != 200:
            dic.update({"info": "server conn err", "status": "fail", "code": 0})
            return self.HttpResponse(dic)
        ret_body = json.loads(http_info.text)

        return self.HttpResponse(json.dumps(ret_body))