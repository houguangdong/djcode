# -*- coding:utf-8 -*-

from django.conf.urls import url

from app.logics.channel_lock.channellocklist import ChannelLockList
from app.logics.channel_lock.channellockset import ChannelLockSet

channel_lock_urls = [
    url("^channellocklist$", ChannelLockList.as_view()),
    url("^channellockset$", ChannelLockSet.as_view()),
]