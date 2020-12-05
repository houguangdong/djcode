# -*- coding:utf-8 -*-
from config.mapping_conf import channel
from core.views import ResetView


class ChannelList(ResetView):
    """
    查询渠道列表
    """
    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        response_list = []
        for channelId, channelName in channel.items():
            response_list.append({"channelId": channelId, "channelName": channelName})
        return self.HttpResponse(response_list)