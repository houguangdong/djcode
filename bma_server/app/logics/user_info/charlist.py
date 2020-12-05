# -*- coding:utf-8 -*-
import requests

from config.game_server_config import platform_server_info
from config.mapping_conf import platform_mapping, platform_str_mapping, platform_int_mapping
from core.views import ResetView


class CharList(ResetView):
    """
    查询渠道或者用户ID下的角色列表
    """

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        platformId = parameter_info.get("platformId")  # 平台
        serverId = parameter_info.get("serverId")  # 区服
        get_type = int(parameter_info["type"])  # 参数类型  1-用户ID查询； 2-渠道ID查询；
        userId = parameter_info["userId"]  # 用户ID  当type=1时，传入用户ID
        channelId = parameter_info["channelId"]  # 渠道名称 当type=2时，传入渠道2个参数
        channelUserId = parameter_info["channelUserId"]  # 渠道用户ID
        platformId = platform_str_mapping.get(platformId, platformId)
        response_dic = {
            "status": "success",  # 处理结果编码
            "code": 1,  # 处理结果
            "roleLists": [  # 角色列表
                {
                    "roleId": "",  # 用户id
                    "roleName": "",  # 用户名
                    "platformId": "",  # 区id
                    "serverId": ""  # 服务器id
                }
            ]
        }

        roleLists = []
        if platformId:
            if not platform_server_info.get(int(platformId)):
                response_dic.update({"status": "fail", "code": 0})
                return
            platform_conf = platform_server_info[int(platformId)]
            url = "http://%s:%s/platform_server/charlist" % (platform_conf["host"], platform_conf["port"])
            send_http_data = {"type": get_type, "userId": userId, "serverId": serverId, "channelId": channelId,
                              "channelUserId": channelUserId}
            http_info = requests.post(url, send_http_data)
            if http_info.status_code != 200:
                response_dic.update({"info": "server conn err", "status": "fail", "code": 0})
                return self.HttpResponse(response_dic)
            http_response_info = self.json_loads(http_info.text)
            for plat_info in http_response_info:
                plat_info["platformId"] = platform_int_mapping[platformId]
                roleLists.append(plat_info)
            if not roleLists[0]["roleId"]:
                response_dic.update({"status": "fail", "code": 0})
            response_dic.update({"roleLists": roleLists})
            return self.HttpResponse(response_dic)

        if serverId:
            for platformId in platform_mapping.keys():
                platform_conf = platform_server_info[platformId]
                url = "http://%s:%s/platform_server/charlist" % (platform_conf["host"], platform_conf["port"])
                send_http_data = {"type": get_type, "userId": userId, "serverId": serverId, "channelId": channelId,
                                  "channelUserId": channelUserId}
                http_info = requests.post(url, send_http_data)
                if http_info.status_code != 200:
                    response_dic.update({"info": "server conn err", "status": "fail", "code": 0})
                    return self.HttpResponse(response_dic)
                http_response_info = self.json_loads(http_info.text)
                for plat_info in http_response_info:
                    plat_info["platformId"] = platform_int_mapping[platformId]
                    roleLists.append(plat_info)
                if not roleLists[0]["roleId"]:
                    response_dic.update({"status": "fail", "code": 0})
                response_dic.update({"roleLists": roleLists})
                return self.HttpResponse(response_dic)

        if get_type == 1 or get_type == 2:
            for platformId in platform_mapping.keys():
                platform_conf = platform_server_info[platformId]
                url = "http://%s:%s/platform_server/charlist" % (platform_conf["host"], platform_conf["port"])
                send_http_data = {"type": get_type, "userId": userId, "serverId": serverId, "channelId": channelId,
                                  "channelUserId": channelUserId}
                http_info = requests.post(url, send_http_data)
                if http_info.status_code != 200:
                    response_dic.update({"info": "server conn err", "status": "fail", "code": 0})
                    continue
                http_response_info = self.json_loads(http_info.text)
                for plat_info in http_response_info:
                    plat_info["platformId"] = platform_int_mapping[platformId]
                    roleLists.append(plat_info)
            if not roleLists[0]["roleId"]:
                response_dic.update({"status": "fail", "code": 0})
            response_dic.update({"roleLists": roleLists})
            return self.HttpResponse(response_dic)
        else:
            response_dic.update({"code": 0, "status": "fail"})
            return self.HttpResponse(response_dic)