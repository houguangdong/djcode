# -*- coding:utf-8 -*-
import requests

from config.platform_mapping import platform
from config.server_conf import BMA_INFO
from core.view import View


class UseCdKey(View):
    def get(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    def do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        response_dic = {
            "platformId": platform["platformId"],
            "serverName": platform["server"][int(parameter_info["serverId"])]["server_name"],
        }

        parameter_info.update(response_dic)

        requests.post("http://%s:%s/usecdkey" % (BMA_INFO["host"], BMA_INFO["port"]), parameter_info)

        return self.HttpResponse({"state": True})
