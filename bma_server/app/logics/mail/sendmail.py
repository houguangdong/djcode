# -*- coding:utf-8 -*-
import time
import requests

from config.game_server_config import platform_server_info
from config.mapping_conf import platform_str_mapping
from core.views import ResetView


class SendMail(ResetView):
    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        from django.http import QueryDict
        _body = self.request.body
        _body = _body.replace(';', '%3B')
        parameter_info = QueryDict(_body)
        channelRange = parameter_info["channelRange"]  # 渠道范围
        channelId = parameter_info["channelId"]  # 渠道ID
        sendType = parameter_info["sendType"]  # 发送对象
        platformId = parameter_info["platformId"]  # 平台
        serverId = parameter_info["serverId"]  # 区服
        roleId = parameter_info["roleId"]  # 角色ID
        sender = parameter_info["sender"]  # 发件人
        title = parameter_info["title"]  # 标题
        content = parameter_info["content"]  # 内容
        items = str(parameter_info["items"])  # 奖励道具列表
        startTime = parameter_info["startTime"]  # 开始时间
        endTime = parameter_info["endTime"]  # 结束时间
        startTime = int(time.mktime(time.strptime(startTime, "%Y-%m-%d %H:%M:%S")))
        endTime = int(time.mktime(time.strptime(endTime, "%Y-%m-%d %H:%M:%S")))

        platformId = platform_str_mapping.get(platformId, platformId)

        response_dic = {
            "status": "success",  # 处理结果编码
            "code": 1,  # 处理结果
            "info": "",  # 错误信息
            "roleName": "",  # 角色名称
        }  # 基础返回数据

        if not platform_server_info.get(platformId, None):  # 判断平台游戏服务器是否存在
            response_dic.update({"status": "fail", "code": 0, "info": "platformId err"})
            return self.HttpResponse(response_dic)

        platform_conf = platform_server_info[platformId]
        url = "http://%s:%s/platform_server/sendmail" % (
            platform_conf["host"], platform_conf["port"])
        send_parameter = {"channelRange": channelRange, "channelId": channelId, "sendType": sendType,
                          "serverId": serverId, "roleId": roleId, "sender": sender, "title": title, "content": content,
                          "items": items, "startTime": startTime, "endTime": endTime, "test": [1, 2], "test2": []}
        http_info = requests.post(url, send_parameter)
        if http_info.status_code != 200:
            response_dic.update({"info": "server conn err", "status": "fail", "code": 0})
            return self.HttpResponse(response_dic)
        http_response_info = self.json_loads(http_info.text)
        if http_response_info["code"] != 1:
            http_response_info["status"] = "fail"
        response_dic.update(http_response_info)
        return self.HttpResponse(response_dic)