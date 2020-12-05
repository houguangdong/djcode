# -*- coding:utf-8 -*-
from core.view import View
import json
import requests
from config.platform_mapping import platform


class VipDoubleRest(View):
    """
    VIP 首冲重置
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        """
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        parameter_info = self.parameters
        print parameter_info

        serverId = parameter_info["serverId"]  # 区服
        upTime = int(parameter_info["upTime"])  # 重置时间戳

        server_ids = map(int, serverId.strip().split(','))  # 服务器id list
        server_config = platform["server"]
        ret = {}
        for server_id in server_ids:
            if server_id not in platform["server"]:
                ret[server_id] = 0
                continue
            host = server_config[server_id]["host"]
            port = server_config[server_id]["port"]
            url = "http://%s:%s/server_mba_api/vip_double_rest" % (host, port)
            parameters = {"upTime": upTime}
            http_info = requests.post(url, parameters)
            if http_info.status_code != 200:
                ret[server_id] = 0
                continue
            ret[server_id] = 1
        print ret
        return self.HttpResponse(json.dumps(ret))