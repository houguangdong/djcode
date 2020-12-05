# -*- coding:utf-8 -*-
import requests
import arrow
from config.platform_mapping import platform
from core.view import View


class SendMail(View):
    def post(self, request, *args, **kwargs):
        parameter_info = self.parameters
        channelRange = int(parameter_info["channelRange"])  # 渠道范围
        channelId = parameter_info["channelId"]  # 渠道ID
        sendType = int(parameter_info["sendType"])  # 发送对象
        serverId = parameter_info["serverId"]  # 区服
        roleId = parameter_info["roleId"]  # 角色ID
        sender = parameter_info["sender"]  # 发件人
        title = parameter_info["title"]  # 标题
        content = parameter_info["content"]  # 内容
        items = str(parameter_info["items"])  # 奖励道具列表
        startTime = parameter_info["startTime"]  # 开始时间
        endTime = parameter_info["endTime"]  # 结束时间

        utc_now = arrow.utcnow()
        today = utc_now.to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        response_dic = {
            'status': 'success',
            'code': 1,
            'info': '',
            'roleName': '',
            'rewardTime': today,
            'vipLevel': '',
            'level': ''
        }
        if channelRange == 2:
            flag = False
            for channel_key in map(int, channelId.split(",")):
                if channel_key in platform["channel_list"]:
                    flag = True
                    break
            if not flag:
                return self.HttpResponse({"code": 2, "info": "channel range err"})  # TODO code  特殊处理

        serverIds = [int(i) for i in serverId.split(",") if i]
        serverIds = serverIds if serverIds else platform["server"].keys()

        if sendType == 2 and len(serverIds) > 1:
            return self.HttpResponse({"code": 0, "info": "serverId too much err"})

        http_url = []
        for serverId in serverIds:
            if not platform["server"].get(serverId, None):
                return self.HttpResponse({"code": 0, "info": "server id err"})
            game_server = platform["server"][serverId]
            http_url.append("http://%s:%s/server_mba_api/sendmail" % (game_server["host"], game_server["port"]))

        items = ",".join(
            [("1:%s:%s" if int(i.split(":")[0]) < 10000 else "2:%s:%s") % (i.split(":")[0], i.split(":")[1]) for i in
             items.split(";") if i])
        send_data = {"sendType": sendType, "roleId": roleId, "sender": sender, "title": title, "content": content,
                     "items": items, "startTime": startTime, "endTime": endTime, "channelId": channelId}

        error_info = []
        for url in http_url:
            http_info = requests.post(url, send_data)
            if http_info.status_code != 200:
                error_info.append("http game server err %s" % url)
            http_ret = self.json_loads(http_info.text)
            if http_ret["code"] != 1:
                error_info.append("http game server err %s %s" % (url, http_ret["info"]))

        if error_info:
            response_dic["info"] = "\t".join(error_info)

        return self.HttpResponse(response_dic)