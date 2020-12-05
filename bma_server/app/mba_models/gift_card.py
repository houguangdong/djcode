# -*- coding:utf-8 -*-
import hashlib
import random
import string
import time
import json
from core.utils.redis_connet import gift_redis


class GiftCard(object):

    """
    礼品卡信息
        giftCardId          礼品卡id
        giftCardCode        礼品码
        useLimit            使用限制
        sourceItems         获取资源信息
        channelRange        使用的渠道限制
        channelList         可使用的渠道列表
        endTime             礼品卡失效时间
        cardNum             礼品卡生成数量
        cardName            礼品卡名称
        isEnabled           礼品卡是否有效
    """
    config_name = "gift_app"

    def __init__(self):
        self.giftCardId = None
        self.giftCardCode = []  # 礼品码
        self.useLimit = 1  # 使用限制
        self.sourceItems = []  # 获取的资源信息
        self.channelRange = []  # 使用渠道的限制
        self.channelList = 1  # 渠道范围
        self.endTime = 0  # 失效时间
        self.cardNum = 0  # 礼品卡生成的数量
        self.cardName = ""  # 礼品卡名称
        self.giftGroupId = ""  # 分组id
        self.isEnabled = 0  # 是否有效
        self.createTime = 0  # 创建时间

    @classmethod
    def install_gift_card(cls, useLimit, sourceItems, channelRange, channelList, endTime, cardNum, cardName,
                          giftGroupId):
        """
        安装礼品卡
        """
        gift_card_obj = cls()
        data = "%s_%s" % (str(time.time()), ''.join(random.sample(string.ascii_letters + string.digits, 32)))
        gift_card_obj.giftCardId = hashlib.md5(data.encode("utf8")).hexdigest()
        gift_card_obj.useLimit = useLimit
        gift_card_obj.sourceItems = sourceItems
        gift_card_obj.channelRange = channelRange
        gift_card_obj.channelList = channelList
        # gift_card_obj.endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endTime))
        gift_card_obj.endTime = endTime
        gift_card_obj.cardNum = cardNum
        gift_card_obj.cardName = cardName
        gift_card_obj.giftGroupId = giftGroupId
        gift_card_obj.giftCardCode = [''.join(random.sample(string.ascii_letters + string.digits, 16)).upper() for _ in
                                      range(cardNum)]
        gift_card_obj.createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        gift_card_obj.isEnabled = 1
        return gift_card_obj

    def put(self):
        gift_redis.set("gift_group", json.dumps(self.__dict__))
        return "put ok"