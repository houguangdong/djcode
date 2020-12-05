# -*- coding:utf-8 -*-


from django.conf.urls import url

from app.logics.common.serverlist import ServerList


common_urls = [
    url("^serverlist", ServerList.as_view())
]