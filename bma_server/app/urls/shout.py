# -*- coding:utf-8 -*-

from django.conf.urls import url

from app.logics.shout.system_shout import SystemShout

shout_urls = [
    url("^SystemShout", SystemShout.as_view()),
]