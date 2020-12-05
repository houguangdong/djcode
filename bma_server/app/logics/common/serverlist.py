# -*- coding:utf-8 -*-
import requests

from config.game_server_config import platform_server_info
from config.mapping_conf import platform_str_mapping
from core.views import ResetView
import json


class ServerList(ResetView):
    """
    查询服列表
    """

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        platformId = parameter_info["platformId"]  # 平台id

        platformId = platform_str_mapping.get(platformId, platformId)

        url = "http://%s:%s/platform_server/serverlist" % (
            platform_server_info[platformId]["host"], platform_server_info[platformId]["port"])

        response = requests.post(url)
        result = json.loads(response.text)
        return self.HttpResponse(json.dumps(result))