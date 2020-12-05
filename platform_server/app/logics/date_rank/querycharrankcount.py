# -*- coding:utf-8 -*-
from app.logics.date_rank.querycharrank import _get_num
from config.platform_mapping import platform
from core.view import View

import requests


class Qquerycharrankcount(View):
    """
    """
    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        """
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        parameter_info = self.parameters
        serverId = int(parameter_info.get("serverId"))
        if serverId == 0:
            return self.HttpResponse({'totalCount': sum(_get_num())})
        else:
            total_num_dict = _get_num()

            return self.HttpResponse({'totalCount': total_num_dict.get(serverId, 0)})