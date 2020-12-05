# -*- coding:utf-8 -*-
from app.mba_models.gift import Gift
from app.model_package.gift import GiftUseInfo
from config.mapping_conf import platform_str_mapping
from core.views import ResetView


class UseCdKey(ResetView):
    """
    用户使用cdkey
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        from core.utils.redis_connet import gift_redis

        parameter_info = self.parameters
        platformId = parameter_info["platformId"]
        serverId = parameter_info["serverId"]
        serverName = parameter_info["serverName"]
        userId = parameter_info["userId"]
        roleName = parameter_info["roleName"]
        level = parameter_info["level"]
        cardCode = parameter_info["cardCode"]
        useTime = parameter_info["useTime"]
        cardId = parameter_info["cardId"]

        platformId = platform_str_mapping.get(platformId, platformId)

        response_dic = {
            "status": "success",
            "code": 1,
            "info": "",
        }

        gift_obj = Gift()
        group_info = gift_obj.get_gift_group_info("")
        groupId = ""
        for groupId in group_info.keys():
            card_ids = gift_redis.hgetall("group_card_info_%s" % groupId)
            if cardId in card_ids or bytes(cardId) in card_ids:
                break

        GiftUseInfo.install(platformId, serverId, serverName, userId, roleName, level, groupId, cardId, cardCode,
                            useTime)

        return self.HttpResponse(response_dic)