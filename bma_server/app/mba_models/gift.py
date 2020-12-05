# -*- coding:utf-8 -*-
import json

from app.mba_models.gift_card import GiftCard
from app.mba_models.gift_group import GiftGroup
from app.model_package.gift import GiftGroupInfoModel
from core.model import BaseModel
from core.utils.redis_connet import gift_redis


class Gift(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.gift_key = "gift_group"                    # 礼品组
        self.gift_group_id = "gift_group_%s"            # 礼品组[1, 2, 3, 4]
        self.gift_card_info = "gift_card_info_%s"       # 礼物卡信息CDK  card_code [礼品码1、礼品码2、礼品码3]
        self.gift_card = "gift_card_%s"                 # 获取礼品卡 获取card 的详细信息
        self.group_card = "group_card_info_%s"          # 礼品组 [cardId1、cardId2]

    def get_gift_group_info(self, name):
        """
        根据组名获取组信息
        :param name: 组名
        """
        gift_group_info_objs = GiftGroupInfoModel.objects.filter(groupName__contains=name)
        group_ids = [i.giftGroupId for i in gift_group_info_objs]
        ret_info = {}
        for group_id in group_ids:
            group_info = gift_redis.hgetall(self.gift_group_id % group_id)
            ret_info[group_id] = group_info
            ret_info[group_id]["isEnabled"] = int(gift_redis.hget(self.gift_key, self.gift_group_id % group_id))
        return ret_info

    def create_gift_group(self, groupName, description, isEnabled=1):
        """
        创建礼品卡分组
        :param groupName:  分组名称
        :param description:  分组描述
        :param isEnabled:  是否有效
        """
        gift_model_objs = GiftGroupInfoModel.objects.filter(groupName=groupName)
        if gift_model_objs:
            return "group name existence ID：%s" % gift_model_objs[0].giftGroupId.encode("utf8")
        gift_group_obj = GiftGroup.install_gift_group(groupName, description, isEnabled)
        gift_group_key = self.gift_group_id % gift_group_obj.giftGroupId
        gift_redis.hmset(gift_group_key, {"groupName": groupName, "description": description})
        gift_redis.hset(self.gift_key, gift_group_key, isEnabled)
        GiftGroupInfoModel.objects.create(groupName=groupName, giftGroupId=gift_group_obj.giftGroupId)
        return gift_group_obj

    def get_group_card_info(self, groupId, is_cdk=False):
        """
        获取分组中的所有卡片信息
        :param groupId: 分组ID
        """
        card_ids = gift_redis.hgetall(self.group_card % groupId)
        card_ids = card_ids.keys()
        cardLists = []
        for card_id in card_ids:
            card_id = bytes.decode(card_id, "utf8") if isinstance(card_id, bytes) else card_id
            gift_card_key = self.gift_card % card_id
            card_info = gift_redis.hgetall(gift_card_key)
            cache = {"groupId": groupId, "cardId": card_id}
            for key, val in card_info.items():
                key = bytes.decode(key, "utf8") if isinstance(key, bytes) else key
                val = bytes.decode(val, "utf8") if isinstance(val, bytes) else val
                if is_cdk and key in ["giftGroupId", "CDK"]:
                    continue
                cache[str(key)] = val
            cardLists.append(cache)
        return cardLists

    def create_gift_card(self, useLimit, sourceItems, channelRange, channelList, endTime, cardNum, cardName,
                         giftGroupId):
        """
        创建礼品卡
        :param useLimit: 使用限制
        :param sourceItems: 获取资源信息
        :param channelRange: 使用的渠道限制
        :param channelList: 可使用的渠道列表
        :param endTime: 礼品卡失效时间
        :param cardNum: 礼品卡生成数量
        :param cardName:    礼品卡名称
        :param giftGroupId: 创建到那个分组
        """
        gift_gift_card_obj = GiftCard.install_gift_card(useLimit, sourceItems, channelRange, channelList, endTime,
                                                        cardNum, cardName,
                                                        giftGroupId)
        data = {"useLimit": gift_gift_card_obj.useLimit,
                "sourceItems": gift_gift_card_obj.sourceItems,
                "channelRange": gift_gift_card_obj.channelRange,
                "channelList": gift_gift_card_obj.channelList,
                "endTime": gift_gift_card_obj.endTime,
                "cardNum": gift_gift_card_obj.cardNum,
                "cardName": gift_gift_card_obj.cardName,
                "giftGroupId": gift_gift_card_obj.giftGroupId,
                "isEnabled": gift_gift_card_obj.isEnabled,
                "createTime": gift_gift_card_obj.createTime,
                "useNum": 0,
                "status": 1,
                "CDK": json.dumps(gift_gift_card_obj.giftCardCode)}

        gift_card_key = self.gift_card % gift_gift_card_obj.giftCardId
        gift_redis.hmset(gift_card_key, data)
        gift_redis.hset(self.group_card % giftGroupId, gift_gift_card_obj.giftCardId, "")
        for code in gift_gift_card_obj.giftCardCode:
            gift_redis.hmset(self.gift_card_info % code,
                             {"cardId": gift_gift_card_obj.giftCardId, "roleId": "", "userId": "", "serverId": "",
                              "platformId": "", "use_count": -100 if gift_gift_card_obj.useLimit == 1 else 1})
        return gift_gift_card_obj

    def check_group_id(self, group_id):
        """
        校验分组id
        :param group_id: 分组id
        """
        ret_info = gift_redis.hget(self.gift_key, self.gift_group_id % group_id)
        if ret_info:
            return True
        return False

    def check_card_code(self, card_code):
        """
        校验礼品码是否可用
        :param card_code: 礼品码
        """
        card_code_info = gift_redis.hgetall(self.gift_card_info % card_code)
        return card_code_info

    def del_group(self, groupId):
        """
        删除组
        :param groupId: 组id
        """

        for card_info in self.get_group_card_info(groupId):
            for cdk in json.loads(card_info["CDK"]):
                gift_redis.delete(self.gift_card_info % cdk)
            gift_card_key = self.gift_card % card_info["cardId"]
            gift_redis.delete(gift_card_key)
            gift_redis.hdel(self.group_card % groupId, card_info["cardId"])

        gift_group_key = self.gift_group_id % groupId
        gift_redis.delete(gift_group_key)
        gift_redis.hdel(self.gift_key, gift_group_key)
        GiftGroupInfoModel.objects.filter(giftGroupId=groupId).delete()
        return

    def modify_card_state(self, groupId, cardId, modify_state):
        """
        修改礼品卡状态
        :param cardId: 礼品卡id
        :param modify_state: 修改的状态
        """
        gift_card_key = self.gift_card % cardId

        modify_state_key = "status" if modify_state in [1, 2] else "isEnabled"

        state_map = {
            1: 1,
            2: 2,
            3: 0
        }

        if modify_state == 3:
            for card_info in self.get_group_card_info(groupId):
                if card_info["cardId"] != cardId:
                    continue
                for cdk in json.loads(card_info["CDK"]):
                    gift_redis.delete(self.gift_card_info % cdk)

            gift_redis.delete(gift_card_key)
            gift_redis.hdel(self.group_card % groupId, cardId)
        else:
            gift_redis.hset(gift_card_key, modify_state_key, state_map[modify_state])
        return

    def card_info(self, cardId):
        """
        获取礼品卡cdkey
        :param cardId: 礼品卡id
        """
        gift_card_key = self.gift_card % cardId
        cdk_str = gift_redis.hget(gift_card_key, "CDK")
        return json.loads(cdk_str) if cdk_str else []

    def get_card_info(self, card_id):
        """
        获取card 的详细信息
        """
        gift_card_key = self.gift_card % card_id
        return gift_redis.hgetall(gift_card_key)