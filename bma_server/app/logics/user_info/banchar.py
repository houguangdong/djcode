# -*- coding:utf-8 -*-
import requests

from app.logics.utility.time_handle import int_format_time
from config.game_server_config import platform_server_info
from config.mapping_conf import platform_str_mapping
from core.views import ResetView


class BanChar(ResetView):
    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters

        platformId = parameter_info["platformId"]  # 平台
        serverId = int(parameter_info["serverId"])  # 服
        oper_type = parameter_info["type"]  # 操作类型
        bannedType = parameter_info["bannedType"]  # 封禁类型
        roleId = parameter_info["roleId"]  # 角色id
        roleName = parameter_info["roleName"]  # 角色名
        bannedTime = parameter_info["bannedTime"]  # 封禁时长
        banned_remark = parameter_info["bannedReason"]  # 封禁说明

        platformId = platform_str_mapping.get(platformId, platformId)

        response_dic = {
            "status": "success",  # 处理结果编码
            "code": 1,  # 处理结果
            "info": "",  # 错误信息
            "roleId": "",  # 角色ID
            "roleName": "",  # 角色名称
            "bannedType": "",  # 封禁类型
            "lockTime": "",  # 封禁时间
            "unlockTime": "",  # 解封日期
        }  # 基础返回数据

        if not platform_server_info.get(platformId, None):  # 判断平台游戏服务器是否存在
            response_dic.update({"status": "fail", "code": 0, "info": "platformId err"})
            return self.HttpResponse(response_dic)

        platform_conf = platform_server_info[int(platformId)]
        url = "http://%s:%s/platform_server/banchar" % (platform_conf["host"], platform_conf["port"])

        send_http_data = {"serverId": serverId, "type": oper_type, "bannedType": bannedType, "roleId": roleId,
                          "roleName": roleName, "bannedTime": bannedTime, "banned_remark": banned_remark}
        http_info = requests.post(url, send_http_data)
        if http_info.status_code != 200:
            response_dic.update({"info": "server conn err", "status": "fail", "code": 0})
            return self.HttpResponse(response_dic)
        http_response_info = self.json_loads(http_info.text)

        if http_response_info["code"] != 1:
            http_response_info["status"] = "fail"

        response_dic.update(http_response_info)
        response_dic["unlockTime"] = int_format_time(response_dic["unlockTime"])
        response_dic["lockTime"] = int_format_time(response_dic["lockTime"])
        return self.HttpResponse(response_dic)
