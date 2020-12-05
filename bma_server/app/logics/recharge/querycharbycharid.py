# -*- coding:utf-8 -*-
from config.mapping_conf import platform_str_mapping
from core.views import ResetView
import json
from config.game_server_config import platform_server_info
import requests
import arrow


class QueryCharByCharId(ResetView):
    """
    根据角色ID获取玩家的状态和充值金额信息
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters

        platformId = parameter_info["platformId"]  # 平台
        serverId = int(parameter_info["serverId"])  # 区服
        roleId = parameter_info["roleId"]  # 角色ID

        platformId = platform_str_mapping.get(platformId, platformId)

        rets = []
        # 遍历平台
        if platformId == "0":
            for pid in platform_server_info.keys():
                ret = call_on(pid, serverId, roleId)
                rets.extend(ret)
        else:
            ret = call_on(platformId, serverId, roleId)
            rets.extend(ret)

        dic = {
            "status": "ok",
            "code": 1,
            "info": "",
            "roleList": rets
        }
        return self.HttpResponse(json.dumps(dic))


def call_on(pid, serverId, roleId):
    """
    @param pid:
    @return:
    """
    platform_conf = platform_server_info[pid]
    url = "http://%s:%s/platform_server/querycharbycharid" % (platform_conf["host"], platform_conf["port"])
    send_parameter = {
        "serverId": serverId,
        "roleId": roleId,
    }
    ret = requests.post(url, send_parameter)
    if ret.status_code != 200:
        return []
    return json.loads(ret.text)