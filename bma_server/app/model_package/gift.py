# -*- coding:utf-8 -*-
import time

from django.db import models


class GiftGroupInfoModel(models.Model):
    """
    卡片信息
    """
    groupName = models.CharField(max_length=128, primary_key=True)  # 组名
    giftGroupId = models.CharField(max_length=64)  # 组id


class GiftUseInfo(models.Model):
    """
    cdk使用记录
    "platformId": "平台id",
    "platformName": "平台名称",
    "serverId": "区服id",
    "serverName": "区服名称",
    "userId": "账号id",
    "roleId": "角色id",
    "roleName": "角色名称",
    "level": "玩家等级",
    "groupId": "分组id",
    "cardId": "礼品卡id",
    "cardName": "卡片名称",#
    "sourceItems": "资源列表", #
    "channelRange": "渠道范围", #
    "useLimit": "使用限制", #
    "isEnabled": "是否有效",#
    "cardCode": "礼品码",
    "createTime": "创建时间", #
    "useTime": "使用时间",
    "endTime": "失效时间", #
    """
    platformId = models.IntegerField()  # 平台id
    serverId = models.IntegerField()  # 区服id
    serverName = models.CharField(max_length=64)  # 区服名称
    userId = models.CharField(max_length=128)  # 账号id
    roleName = models.CharField(max_length=64)  # 角色名称
    level = models.IntegerField()  # 玩家等级
    groupId = models.CharField(max_length=128)  # 分组id
    cardId = models.CharField(max_length=128)  # 礼品卡id
    cardCode = models.CharField(max_length=64)  # 礼品码
    useTime = models.BigIntegerField()  # 使用时间

    @classmethod
    def install(cls, platformId, serverId, serverName, userId, roleName, level, groupId, cardId, cardCode, useTime):
        new_obj = cls.objects.create(
            platformId=platformId,
            serverId=serverId,
            serverName=serverName,
            userId=userId,
            roleName=roleName,
            level=level,
            groupId=groupId,
            cardId=cardId,
            cardCode=cardCode,
            useTime=useTime,
        )
        return new_obj