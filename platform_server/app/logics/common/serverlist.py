# -*- coding:utf-8 -*-
from config.platform_mapping import platform
from core.view import View
import json


class ServerList(View):
    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        response_list = []
        for serverId, serverInfo in platform["server"].items():
            response_list.append({"serverId": serverId, "serverName": serverInfo["server_name"]})
        return self.HttpResponse(json.dumps(response_list))