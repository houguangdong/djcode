# -*- coding:utf-8 -*-
from app.mba_models.gift import Gift
from core.views import ResetView


class GetAvailableGiftCard(ResetView):
    """
    导出
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        groupId = parameter_info["groupId"]
        cardId = parameter_info["cardId"]
        gift = Gift()
        cardCodeList = gift.card_info(cardId)
        response_dic = {
            "status": "success",
            "code": 1,
            "info": "",
            "cardCodeList": [{"cardCode": cdk} for cdk in cardCodeList],
        }
        return self.HttpResponse(response_dic)