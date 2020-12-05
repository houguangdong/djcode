# -*- coding:utf-8 -*-


from django.conf.urls import url

from app.logics.channel_lock.channellockset import ChannelLockSet

channel_lock_urls = [
    url("^channellockset$", ChannelLockSet.as_view())
]