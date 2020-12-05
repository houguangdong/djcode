# -*- coding:utf-8 -*-

import requests

from app.model_package.user_info import Banned
from config.platform_mapping import platform
from core.view import View

import time


class BanChar(View):
    def post(self, request, *args, **kwargs):
        parameter_info = self.parameters
        serverId = int(parameter_info["serverId"])  # 服
        oper_type = int(parameter_info["type"])  # 操作类型
        bannedType = parameter_info["bannedType"]  # 封禁类型
        roleId = int(parameter_info.get("roleId", 0))  # 角色id
        roleName = parameter_info["roleName"]  # 角色名
        bannedTime = parameter_info["bannedTime"]  # 封禁时长
        banned_remark = parameter_info["banned_remark"]  # 封禁或者解封原因

        response_dic = {
            "status": "fail",  # 处理结果编码
            "code": 1,  # 处理结果
            "info": "",  # 错误信息
            "roleId": "",  # 角色ID
            "roleName": "",  # 角色名称
            "bannedType": "",  # 封禁类型
            "lockTime": "",  # 封禁时间
            "unlockTime": "",  # 解封日期
        }  # 基础返回数据

        if not platform["server"].get(serverId, None):
            return self.HttpResponse({"code": 0, "info": "server id  err"})

        serverId = int(serverId)
        game_server_conf = platform["server"][serverId]
        url = "http://%s:%s/server_mba_api/banchar" % (game_server_conf["host"], game_server_conf["port"])
        send_data = {"oper_type": oper_type, "bannedType": bannedType, "roleId": roleId, "roleName": roleName,
                     "bannedTime": bannedTime, "banned_remark": banned_remark}
        http_info = requests.post(url, send_data)
        if http_info.status_code != 200:
            return self.HttpResponse({"code": 0, "info": "game server err"})

        http_ret = self.json_loads(http_info.text)

        response_dic.update(http_ret)
        if response_dic["code"] == 1:
            Banned.add_banned_info(response_dic["roleId"], serverId, response_dic["roleName"],
                                   response_dic["bannedType"], int(time.time()), int(time.time()),
                                   response_dic["unlockTime"], banned_remark.encode(encoding="utf8"))

        return self.HttpResponse(response_dic)