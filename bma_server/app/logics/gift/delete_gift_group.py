# -*- coding:utf-8 -*-
from app.mba_models.gift import Gift
from core.views import ResetView


class DeleteGiftGroup(ResetView):
    """
    删除分组及卡片
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        groupId = parameter_info["groupId"]  # 分组id

        gift_obj = Gift()
        gift_obj.del_group(groupId)

        response_dic = {
            "status": "success",  # 处理结果编码
            "code": 1,  # 处理结果
            "info": "",  # 错误信息
        }

        response_dic.update({"cardLists": gift_obj.get_group_card_info(groupId)})
        return self.HttpResponse(response_dic)

