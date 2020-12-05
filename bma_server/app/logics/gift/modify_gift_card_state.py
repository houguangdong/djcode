# -*- coding:utf-8 -*-
from app.mba_models.gift import Gift
from core.views import ResetView


class ModifyGiftCardState(ResetView):
    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        groupId = parameter_info["groupId"]  # 分组名称
        cardId = parameter_info["cardId"]
        modify_type = int(parameter_info["type"])

        gift_obj = Gift()
        gift_obj.modify_card_state(groupId, cardId, modify_type)

        response_dic = {
            "status": "success",  # 处理结果编码
            "code": 1,  # 处理结果
            "info": "",  # 错误信息
        }

        return self.HttpResponse(response_dic)