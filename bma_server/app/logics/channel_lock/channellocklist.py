# -*- coding:utf-8 -*-
from app.model_package.channel_lock import ChannelLock
from config.mapping_conf import channel
from core.views import ResetView
import json


class ChannelLockList(ResetView):
    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        locktype = int(parameter_info["type"])  # 开关类型
        exact_str = '_%s' % locktype
        cllist = ChannelLock.objects.filter(channelId__contains=exact_str)

        channelLists = []
        for channellock in cllist:
            channelId, _ = channellock.channelId.split('_')
            item = {
                'channelId': channelId,
                'channelName': channel.get(int(channelId)),
                'lockstatus': channellock.lockstatus,
                'content': channellock.content
            }
            channelLists.append(item)
        response_dic = {
            'status': 'ok',
            'code': '1',
            'channelLists': channelLists
        }
        return self.HttpResponse(json.dumps(response_dic))
