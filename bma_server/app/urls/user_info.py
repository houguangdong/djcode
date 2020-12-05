# -*- coding:utf-8 -*-

from django.conf.urls import url

from app.logics.user_info.banchar import BanChar
from app.logics.user_info.banlist import BanList
from app.logics.user_info.charlist import CharList
from app.logics.user_info.qci import Qci
from app.logics.user_info.userquery import UserQuery

user_info_urls = [
    url("^qci$", Qci.as_view()),
    url("^charlist$", CharList.as_view()),
    url("^banlist$", BanList.as_view()),
    url("^banchar$", BanChar.as_view()),
    url("^userquery", UserQuery.as_view()),
]