# -*- coding:utf-8 -*-
from app.mba_models.gift import Gift
from core.views import ResetView


class QueryGiftCard(ResetView):
    """
    根据分组id获取礼品卡列表
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        groupId = parameter_info["groupId"]  # 分组id
        p = parameter_info["p"]  # 页码
        pageSize = parameter_info["pageSize"]  # 每页显示数量

        gift_obj = Gift()

        response_dic = {
            "status": "success",
            "code": 1,
            "info": "",
            "cardLists": [{
                "groupId": "分组id",
                "cardId": "礼品卡id",
                "cardName": "卡片名称",
                "sourceItems": "资源列表",
                "channelRange": "渠道范围",
                "channelList": "渠道列表",
                "useLimit": "使用限制",
                "status": "状态",
                "useNum": "使用数量",
                "cardNum": "生成数量",
                "createTime": "创建时间",
                "endTime": "失效时间",
                "isEnabled": "是否有效",
            }, ],
        }

        response_dic.update({"cardLists": gift_obj.get_group_card_info(groupId, True)})
        return self.HttpResponse(response_dic)