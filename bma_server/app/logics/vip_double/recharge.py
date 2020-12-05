# -*- coding:utf-8 -*-
from config.mapping_conf import platform_str_mapping
from core.views import ResetView
from config.game_server_config import platform_server_info
import arrow
import json
import requests


class VipDoubleRest(ResetView):
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

        platformId = parameter_info["platformId"]      # 平台
        serverId = parameter_info["serverId"]              # 区服
        platformId = platform_str_mapping.get(platformId, platformId)
        dic = {'status': 'ok', 'code': 1, 'info': ""}

        if not platform_server_info.get(platformId, None):  # 判断平台游戏服务器是否存在
            dic.update({"status": "fail, platform id not found", "code": 0})
            return self.HttpResponse(json.dumps(dic))

        # server_ids = map(int, serverIds.strip().split(',')) # 服务器id list
        m_timestamp = arrow.utcnow().timestamp              # 重置时间戳

        platform_conf = platform_server_info[int(platformId)]

        url = "http://%s:%s/platform_server/VipDoubleRest" % (platform_conf["host"], platform_conf["port"])

        send_http_data = {"serverId": serverId, "upTime": m_timestamp}

        http_info = requests.post(url, send_http_data)
        if http_info.status_code != 200:
            dic.update({"info": "server conn err", "status": "fail", "code": 0})
            return self.HttpResponse(json.loads(dic))
        dic.update({"info": http_info.text})
        ret = json.dumps(dic)
        return self.HttpResponse(ret)

