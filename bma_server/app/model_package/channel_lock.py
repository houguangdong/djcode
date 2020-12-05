# -*- coding:utf-8 -*-

from django.db import models


class ChannelLock(models.Model):
    """渠道开关
    """
    channelId = models.CharField(max_length=8, primary_key=True)            # channelId
    # locktype = models.IntegerField(choices=((1, "充值"), (2, "登录")))      # 开关类型
    lockstatus = models.IntegerField(choices=((1, "打开"), (2, "关闭")))      # 开关状态
    content = models.TextField(blank=False)  # 公告

    # class Meta:
    #     unique_together = (('channelId', 'locktype'),)