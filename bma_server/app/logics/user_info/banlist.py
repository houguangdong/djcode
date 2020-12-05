# -*- coding:utf-8 -*-
import requests

from app.logics.utility.time_handle import int_format_time
from config.game_server_config import platform_server_info
from config.mapping_conf import platform_str_mapping
from core.views import ResetView


class BanList(ResetView):

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        platformId = parameter_info["platformId"]  # 平台
        serverId = int(parameter_info["serverId"])  # 区服
        page = int(parameter_info["page"])  # 页码
        pagesize = int(parameter_info["pagesize"])  # 每页现实数量
        platformId = platform_str_mapping.get(platformId, platformId)
        response_dic = {
            "status": "success",
            "code": 1,
            "totalCount": 0,
            "bannedLists": [
                {
                    "roleId": "角色id",
                    "roleName": "角色名称",
                    "bannedType": "封禁类型",
                    "lockTime": "封禁时间",
                    "unlockTime": "解封日期",
                    "optTime": "操作时间",
                    "remark": "封禁原因",
                }
            ],
        }  # 基础返回数据

        if not platform_server_info.get(platformId, None):  # 判断平台游戏服务器是否存在
            response_dic.update({"status": "fail", "code": 0})
            return self.HttpResponse(response_dic)

        platform_conf = platform_server_info[int(platformId)]
        url = "http://%s:%s/platform_server/banlist" % (platform_conf["host"], platform_conf["port"])
        send_http_data = {"serverId": serverId, "page": page, "pagesize": pagesize}
        http_info = requests.post(url, send_http_data)
        if http_info.status_code != 200:
            response_dic.update({"info": "server conn err", "status": "fail", "code": 0})
            return self.HttpResponse(response_dic)
        http_respoonse_info = self.json_loads(http_info.text)
        response_dic.update(http_respoonse_info)

        for index, val in enumerate(response_dic["bannedLists"]):
            if int(val["unlockTime"]) == 0:
                val["unlockTime"] = "永久"
            else:
                val["unlockTime"] = int_format_time(val["unlockTime"])
            val["lockTime"] = int_format_time(val["lockTime"])
            val["optTime"] = int_format_time(val["optTime"])
            response_dic["bannedLists"][index] = val

        return self.HttpResponse(response_dic)