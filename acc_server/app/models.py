# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Account(models.Model):

    """
    账号类信息
    """
    open_id = models.CharField(max_length=128, primary_key=True)        # 账号id
    platform_id = models.IntegerField()                                 # 平台id
    channelId = models.CharField(max_length=32)                         # 渠道
    serverId = models.IntegerField()                                    # 区服
    uid = models.CharField(max_length=32)                               # uid
    os_type = models.CharField(max_length=32)                           # 设备类型
    app_version = models.CharField(max_length=32)                       # 客户端app版本号
    build_version = models.CharField(max_length=32)                     # svn版本号
    res_version = models.CharField(max_length=32)                       # 资源版本号
    age = models.IntegerField()                                         # 年龄段
    istourist = models.IntegerField()                                   # 是否是游客
    online_time = models.IntegerField()                                 # 在线时长 分钟

    @classmethod
    def install(cls, open_id, platform_id, channelId, serverId, uid, os_type, app_version, build_version, res_version, age, istourist, online_time):
        new_obj = cls.objects.create(
            open_id=open_id,
            platform_id=platform_id,
            channelId=channelId,
            serverId=serverId,
            uid=uid,
            os_type=os_type,
            app_version=app_version,
            build_version=build_version,
            res_version=res_version,
            age=age,
            istourist=istourist,
            online_time=online_time
        )
        return new_obj

    @classmethod
    def search_open_id(cls, open_id):
        acc_info = Account.objects.filter(open_id=open_id)
        if not acc_info:
            return None
        return acc_info


class Recharge(models.Model):
    """
    充值类
    """
    order_id = models.CharField()
    open_id = models.CharField()
