# -*- coding:utf-8 -*-
from core.view import View
import json
import requests
from config.platform_mapping import platform


class SystemShout(View):
    def get(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    def do(self, request, *args, **kwargs):

        parameter_info = self.parameters

        serverId = int(parameter_info["serverId"])      # 区服
        content = parameter_info["content"]             # 内容
        startTime = parameter_info["startTime"]         # 开始时间
        endTime = parameter_info["endTime"]             # 结束时间

        host = platform["server"][serverId]["host"]
        port = platform["server"][serverId]["port"]
        url = "http://%s:%s/server_mba_api/system_shout" % (host, port)
        parameters = {"content": content, "startTime": startTime, "endTime": endTime}

        print url
        print parameters

        ret = requests.post(url, parameters)
        if ret.status_code != 200:
            return self.HttpResponse(json.dumps({"state": False}))
        return self.HttpResponse(json.dumps({"state": True}))