# -*- coding:utf-8 -*-

from django.conf.urls import url

from app.logics.common.channellist import ChannelList
from app.logics.common.platformlist import PlatformList
from app.logics.common.serverlist import ServerList


common_urls = [
    url("^platformlist$", PlatformList.as_view()),
    url("^channellist$", ChannelList.as_view()),
    url("^serverlist$", ServerList.as_view())
]