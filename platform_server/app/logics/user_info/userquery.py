# -*- coding:utf-8 -*-
import json

from config.platform_mapping import platform
from core.view import View

import requests


class UserQuery(View):
    def post(self, request, *args, **kwargs):
        parameter_info = self.parameters
        get_type = int(parameter_info["type"])  # 参数类型  1-用户ID查询； 2-渠道ID查询；
        userId = parameter_info["userId"]  # 用户ID  当type=1时，传入用户ID
        channelId = parameter_info["channelId"]  # 渠道名称 当type=2时，传入渠道2个参数
        channelUserId = parameter_info["channelUserId"]  # 渠道用户ID

        roleLists = []

        if get_type == 2:
            if int(channelId) not in platform["channel_list"]:
                roleLists.append({"roleId": "", "roleName": "", "serverId": ""})
                return self.HttpResponse(json.dumps(roleLists))

        for serverId, server_info in platform["server"].items():
            url = "http://%s:%s/server_mba_api/userquery" % (server_info["host"], server_info["port"])
            send_data = {"type": get_type, "userId": userId, "channelId": channelId, "channelUserId": channelUserId}
            http_info = requests.post(url, send_data)
            if http_info.status_code != 200:
                continue
            http_ret = json.loads(http_info.text)
            if not http_ret["serverId"]:
                continue
            http_ret.update({"serverName": platform["server"][serverId]["server_name"]})
            roleLists.append(http_ret)
        return self.HttpResponse(roleLists)