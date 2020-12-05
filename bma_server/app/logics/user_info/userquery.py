# -*- coding:utf-8 -*-
from app.logics.utility.time_handle import int_format_time
from config.mapping_conf import platform_mapping, channel, platform_int_mapping
from core.views import ResetView
from config.game_server_config import platform_server_info
import requests


class UserQuery(ResetView):
    """
    玩家查询
    """

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        get_type = int(parameter_info["type"])  # 参数类型(1-角色ID查询； 2-角色名查询)
        userId = parameter_info["userId"]  # 用户ID
        channelId = parameter_info["channelId"]  # 渠道名称
        channelUserId = parameter_info["channelUserId"]  # 渠道用户ID
        p = parameter_info["p"]                             # 页数
        pageSize = parameter_info["pageSize"]               # 条数

        response_dic = {
            "status": "success",  # 处理结果编码
            "code": 1,  # code
            "totalCount": 0,  # 角色列表总数
            "roleList": [],  # 角色列表
        }  # 基础返回数据

        roleList = []
        for platformId in platform_mapping.keys():
            platform_conf = platform_server_info.get(platformId, None)
            if not platform_conf:
                continue
            url = "http://%s:%s/platform_server/userquery" % (platform_conf["host"], platform_conf["port"])
            send_http_data = {"type": get_type, "userId": userId, "channelId": channelId,
                              "channelUserId": channelUserId}
            http_info = requests.post(url, send_http_data)
            if http_info.status_code != 200:
                response_dic.update({"info": "server conn err", "status": "fail", "code": 0})
                continue
            http_response_info = self.json_loads(http_info.text)
            for plat_info in http_response_info:
                plat_info.update({
                    "platformId": platform_int_mapping[platformId],
                    "platformName": platform_server_info[platformId]["name"],
                    "channelName": channel[int(plat_info["channelId"])]
                })
                roleList.append(plat_info)
        if roleList and not roleList[0]["roleId"]:
            response_dic.update({"status": "fail", "code": 0})
            return self.HttpResponse(response_dic)

        for index, val in enumerate(roleList):
            val["lastLoginTime"] = int_format_time(val["lastLoginTime"])
            val["createTime"] = int_format_time(val["createTime"])
            roleList[index] = val

        response_dic.update({"totalCount": len(roleList)})
        response_dic.update({"roleList": roleList[int(p) * int(pageSize) - int(pageSize):int(pageSize) * int(p)]})
        return self.HttpResponse(response_dic)
