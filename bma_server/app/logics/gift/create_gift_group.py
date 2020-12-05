# -*- coding:utf-8 -*-
from app.mba_models.gift import Gift
from core.views import ResetView


class CreateGiftGroup(ResetView):
    """
    新建分组
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        groupName = parameter_info["groupName"]
        description = parameter_info["description"]
        response_dic = {"status": "success", "code": 1, "info": "", "groupId": "", "isEnabled": 0}
        gift_obj = Gift()
        new_gift_group_obj = gift_obj.create_gift_group(groupName, description, 1)
        if isinstance(new_gift_group_obj, str):
            response_dic.update({"status": "fail", "code": 0, "info": new_gift_group_obj})
            return self.HttpResponse(response_dic)
        response_dic.update({"groupId": new_gift_group_obj.giftGroupId, "isEnabled": new_gift_group_obj.isEnabled})
        return self.HttpResponse(response_dic)