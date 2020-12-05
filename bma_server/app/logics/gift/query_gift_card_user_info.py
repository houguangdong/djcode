# -*- coding:utf-8 -*-
from app.logics.utility.time_handle import int_format_time
from app.mba_models.gift import Gift
from app.model_package.gift import GiftUseInfo
from config.mapping_conf import platform_mapping, platform_str_mapping, platform_int_mapping
from core.views import ResetView


class QueryGiftCardUserInfo(ResetView):
    """
    卡片查询
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        get_type = int(parameter_info["type"])  # 类型 1,2
        platformId = parameter_info["platformId"]  # 平台ID
        serverId = parameter_info["serverId"]  # 区服ID
        codeInfo = parameter_info["codeInfo"]  # 角色id或者礼品码
        p = parameter_info["p"]  # 页码。当传空字符串的时候，表示查询全部的数据
        pageSize = parameter_info["pageSize"]

        platformId = platform_str_mapping.get(platformId, platformId)

        if get_type == 1:
            platformId, serverId = int(platformId), int(serverId)
            query_info = GiftUseInfo.objects.filter(platformId=platformId, serverId=serverId, roleName=codeInfo)
        elif get_type == 2:
            query_info = GiftUseInfo.objects.filter(cardCode=codeInfo)
        else:
            raise RuntimeError

        if p.isdigit():
            p, page_size = int(p), int(pageSize)
            query_info = query_info[page_size * p - page_size: page_size * 10]

        player_lists = []

        card_info = {}

        gift_obj = Gift()

        for query in query_info:
            card_obj = card_info.setdefault(query.cardId, gift_obj.get_card_info(query.cardId))
            card_info[query.cardId].setdefault("cardId", query.cardId)
            player_lists.append({
                "platformId": platform_int_mapping[query.platformId],
                "platformName": platform_mapping[query.platformId],
                "serverId": query.serverId,
                "serverName": query.serverName,
                "userId": query.userId,
                "roleId": query.userId,
                "roleName": query.roleName,
                "level": query.level,
                "groupId": query.groupId,
                "cardId": query.cardId,
                "cardName": card_obj["cardName"],
                "sourceItems": card_obj["sourceItems"],
                "channelRange": card_obj["channelRange"],
                "useLimit": card_obj["useLimit"],
                "isEnabled": card_obj["isEnabled"],
                "cardCode": query.cardCode,
                "createTime": card_obj["createTime"],
                "useTime": int_format_time(query.useTime),
                "endTime": card_obj["endTime"],
            })

        response_dic = {
            "status": "success",
            "code": 1,
            "info": "",
            "groupId": "",
            "cardId": "",
            "cardName": "",
            "sourceItems": "",
            "channelRange": "",
            "useLimit": "",
            "isEnabled": "",
            "playerLists": player_lists,
        }

        if get_type == 2:
            if card_info:
                card_obj = card_info.values()[0]
                cache_response_dic = {
                    "groupId": card_obj["giftGroupId"],
                    "cardId": card_obj["cardId"],
                    "cardName": card_obj["cardName"],
                    "sourceItems": card_obj["sourceItems"],
                    "channelRange": card_obj["channelRange"],
                    "useLimit": card_obj["useLimit"],
                    "isEnabled": card_obj["isEnabled"]
                }
                response_dic.update(cache_response_dic)

        return self.HttpResponse(response_dic)