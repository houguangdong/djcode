# -*- coding:utf-8 -*-
from config.platform_mapping import platform
from core.view import View

import requests


class Qci(View):
    def post(self, request, *args, **kwargs):
        parameter_info = self.parameters
        serverId = int(parameter_info.get("serverId"))
        get_type = parameter_info.get("type")
        val = parameter_info.get("val")
        game_server_conf = platform["server"][serverId]
        url = "http://%s:%s/server_mba_api/qci" % (game_server_conf["host"], game_server_conf["port"])
        send_parameter = {"type": get_type, "val": val}
        print send_parameter
        http_info = requests.post(url, send_parameter)

        return self.HttpResponse(http_info.text)