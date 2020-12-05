# -*- coding:utf-8 -*-
from app.model_package.channel_lock import ChannelLock
from config.game_server_config import platform_server_info
from core.views import ResetView
import json
import requests


class ChannelLockSet(ResetView):
    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        locktype = int(parameter_info["type"])  # 开关类型
        channelId = parameter_info['channelId']
        lockstatus = parameter_info['locktype']
        content = parameter_info['content']

        cid = '%s_%s' % (channelId, locktype)
        cl = ChannelLock.objects.filter(channelId=cid)
        if cl:
            channel_lock = cl[0]
            channel_lock.lockstatus = lockstatus
            channel_lock.content = content
            channel_lock.save()
        else:
            ChannelLock.objects.create(**{'channelId': cid, 'lockstatus': lockstatus, 'content': content})

        response_dic = {
            'status': 'ok',
            'code': '1',
            'info': '',
        }

        re_list = _transmit_url(locktype, channelId, lockstatus, content)

        return self.HttpResponse(json.dumps(response_dic))


def _transmit_url(locktype, channelId, lockstatus, content):
    """
    :param locktype:
    :param channelId:
    :param lockstatus:
    :param content:
    :return:
    """
    re_list = {}
    for key, value in platform_server_info.items():
        host = value['host']
        port = value['port']
        url = "http://%s:%s/platform_server/channellockset" % (host, port)
        send_parameter = {"type": locktype, "channelId": channelId, 'locktype': lockstatus, 'content': content}
        try:
            response = requests.post(url, send_parameter)
            response.raise_for_status()
            result = json.loads(response.text)  # result = {'code': 1}
            re_list[key] = result
        except Exception as e:
            re_list[key] = {'code': 0}
            import traceback
            traceback.print_exc()
    return re_list