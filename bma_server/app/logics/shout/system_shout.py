# -*- coding:utf-8 -*-
from config.mapping_conf import platform_str_mapping
from core.views import ResetView
import json
from config.game_server_config import platform_server_info
import requests


class SystemShout(ResetView):
    """
    查询渠道列表
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters

        platformId = parameter_info["platformId"]  # 平台
        serverId = int(parameter_info["serverId"])      # 区服
        content = parameter_info["content"]             # 内容
        startTime = parameter_info["startTime"]         # 开始时间
        endTime = parameter_info["endTime"]             # 结束时间
        cycleTime = int(parameter_info["cycleTime"])    # 循环时间

        platformId = platform_str_mapping.get(platformId, platformId)

        dic = {'status': 'ok', 'code': 1, 'info': ''}

        if not platform_server_info.get(platformId, None):  # 判断平台游戏服务器是否存在
            dic.update({"status": "fail", "code": 0})
            return self.HttpResponse(json.dumps(dic))

        platform_conf = platform_server_info[int(platformId)]

        url = "http://%s:%s/platform_server/SystemShout" % (platform_conf["host"], platform_conf["port"])
        send_http_data = {"serverId": serverId, "content": content, "startTime": startTime, "endTime": endTime}
        http_info = requests.post(url, send_http_data)
        if http_info.status_code != 200:
            dic.update({"info": "server conn err", "status": "fail", "code": 0})
            return self.HttpResponse(json.loads(dic))
        data = dict(json.loads(http_info.text))
        if not data.get("state"):
            dic.update({"info": "game server conn err", "status": "fail", "code": 0})
            return self.HttpResponse(json.loads(dic))
        return self.HttpResponse(json.dumps(dic))

