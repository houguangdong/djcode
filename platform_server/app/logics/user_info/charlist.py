# -*- coding:utf-8 -*-
import json

from config.platform_mapping import platform
from core.view import View

import requests


class CharList(View):
    def post(self, request, *args, **kwargs):
        parameter_info = self.parameters
        serverId = parameter_info.get("serverId")  # 区服
        get_type = int(parameter_info["type"])  # 参数类型  1-用户ID查询； 2-渠道ID查询；
        userId = parameter_info["userId"]  # 用户ID  当type=1时，传入用户ID
        channelId = parameter_info["channelId"]  # 渠道名称 当type=2时，传入渠道2个参数
        channelUserId = parameter_info["channelUserId"]  # 渠道用户ID

        roleLists = []

        if not serverId:
            if get_type == 2:
                if int(channelId) not in platform["channel_list"]:
                    roleLists.append({"roleId": "", "roleName": "", "serverId": ""})
                    return self.HttpResponse(json.dumps(roleLists))

            for serverId, server_info in platform["server"].items():
                url = "http://%s:%s/server_mba_api/charlist" % (server_info["host"], server_info["port"])
                send_data = {"type": get_type, "userId": userId, "channelId": channelId, "channelUserId": channelUserId}
                http_info = requests.post(url, send_data)
                if http_info.status_code != 200:
                    continue
                http_ret = json.loads(http_info.text)
                if not http_ret["serverId"]:
                    continue
                roleLists.append(http_ret)
            return self.HttpResponse(roleLists)

        serverId = int(serverId)
        get_type = parameter_info.get("type")
        game_server_conf = platform["server"][serverId]
        url = "http://%s:%s/server_mba_api/charlist" % (game_server_conf["host"], game_server_conf["port"])
        send_data = {"type": get_type, "userId": userId, "channelId": channelId, "channelUserId": channelUserId}
        http_info = requests.post(url, send_data)
        if http_info.status_code != 200:
            roleLists.append({"roleId": "", "roleName": "", "serverId": serverId})
        else:
            roleLists.append(json.loads(http_info.text))
        return self.HttpResponse(roleLists)
