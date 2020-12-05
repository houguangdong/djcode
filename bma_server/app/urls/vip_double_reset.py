# -*- coding:utf-8 -*-

from django.conf.urls import url

from app.logics.vip_double.recharge import VipDoubleRest

vip_double_reset_urls = [
    url("^VipDoubleRest", VipDoubleRest.as_view()),
]