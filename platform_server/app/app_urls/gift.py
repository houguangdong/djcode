# -*- coding:utf-8 -*-
from django.conf.urls import url

from app.logics.gift.use_cdkey import UseCdKey

gift_urls = [
    url("^use_cdkey", UseCdKey.as_view()),
]