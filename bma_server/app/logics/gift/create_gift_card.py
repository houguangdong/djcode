# -*- coding:utf-8 -*-
from app.mba_models.gift import Gift
from core.views import ResetView


class CreateGiftCard(ResetView):
    """
    生成礼品卡
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        from django.http import QueryDict
        _body = self.request.body
        _body = _body.replace(';', '%3B')
        parameter_info = QueryDict(_body)
        groupId = parameter_info["groupId"]  # 分组id
        channelRange = int(parameter_info["channelRange"])  # 渠道范围(1:全渠道通用；2:选渠道使用)
        channelList = parameter_info[
            "channelList"]  # 渠道列表(channelRange=1此值为空字符串;当channelRange=2时为选择的渠道id，按照分号;隔开，格式:渠道1id;渠道2id)
        useLimit = int(parameter_info["useLimit"])  # 使用限制 (1:允许多人使用；2:仅限一人使用)
        sourceItems = parameter_info["sourceItems"]  # 资源列表 (格式为:a道具id:a道具数量;b道具id:b道具数量;)
        endTime = parameter_info["endTime"]  # 失效时间
        cardNum = int(parameter_info["cardNum"])  # 生成数量
        cardName = parameter_info["cardName"]  # 卡片名称

        gift_obj = Gift()

        response_dic = {
            "status": "fail",
            "code": 0,
            "info": "groupIdError",
            "groupId": "",
            "cardId": "",
            "isEnabled": 0,
            "cardCodeList": [{"cardCode": []}],
        }

        if not gift_obj.check_group_id(groupId):
            return self.HttpResponse(response_dic)

        new_gift_card_obj = gift_obj.create_gift_card(useLimit, sourceItems, channelRange, channelList, endTime,
                                                      cardNum, cardName, groupId)
        response_dic.update(
            {"status": "success", "groupId": groupId, "cardCodeList": [{"cardCode": i} for i in new_gift_card_obj.giftCardCode],
             "isEnabled": 1, "code": 1, "info": "", "cardId": new_gift_card_obj.giftCardId})
        return self.HttpResponse(response_dic)