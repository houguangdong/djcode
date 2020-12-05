# -*- coding:utf-8 -*-
from config.mapping_conf import platform_mapping, platform_int_mapping
from core.views import ResetView


class PlatformList(ResetView):
    """
    查询游戏大区
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        response_list = []
        for platformId, platformName in platform_mapping.items():
            response_list.append({"platformId": platform_int_mapping[platformId], "platformName": platformName})
        return self.HttpResponse(response_list)