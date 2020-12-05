# -*- coding:utf-8 -*-
from config.platform_mapping import platform
import json
import requests
from core.view import View


class ChannelLockSet(View):
    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        locktype = int(parameter_info["type"])  # 开关类型
        channelId = int(parameter_info['channelId'])
        lockstatus = parameter_info['locktype']
        content = parameter_info['content']

        flag = _check_channelId(channelId)
        print flag

        if not flag:
            return self.HttpResponse(json.dumps({'code': 1, 'info': '本区没有该渠道'}))

        re_list = _transmit_url(locktype, channelId, lockstatus, content)
        print re_list

        return self.HttpResponse(json.dumps(re_list))


def _check_channelId(channelId):
    """判断是否下发协议(渠道开关设置)
    @return:
    """
    flag = False
    channel_list = platform['channel_list']
    if channelId in channel_list:
        flag = True
    return flag


def _transmit_url(locktype, channelId, lockstatus, content):
    """下发url访问各个服
    @return:
    """
    re_list = {}
    game_server_conf = platform['server']  # 配置数据
    for key, value in game_server_conf.items():
        host = value['host']
        port = value['port']
        url = "http://%s:%s/server_mba_api/channellockset" % (host, port)
        print url
        send_parameter = {"type": locktype, "channelId": channelId, 'locktype': lockstatus, 'content': content}
        try:
            response = requests.post(url, send_parameter)
            response.raise_for_status()
            result = json.loads(response.text)  # result = {'code': 1}
            re_list[key] = result
        except Exception, e:
            re_list[key] = {'code': 0}
            import traceback
            traceback.print_exc()
        continue
    return re_list