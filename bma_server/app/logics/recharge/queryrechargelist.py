# -*- coding:utf-8 -*-
from core.views import ResetView
import json


class QueryRechargeList(ResetView):
    """
    查询充值礼包列表
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters

        dic = {
            "status": "ok",
            "code": 1,
            "info": "",
            "giftLists": [{"giftId": 1, "giftName": u"60元宝"},
                          {"giftId": 2, "giftName": u"300元宝"},
                          {"giftId": 3, "giftName": u"680元宝"},
                          {"giftId": 4, "giftName": u"1980元宝"},
                          {"giftId": 5, "giftName": u"3280元宝"},
                          {"giftId": 6, "giftName": u"6480元宝"}, ]
        }
        return self.HttpResponse(json.dumps(dic))