# -*- coding:utf-8 -*-
from django.conf.urls import url
from app.logics.date_rank.querycharrank import Qquerycharrank
from app.logics.date_rank.querycharrankcount import Qquerycharrankcount

date_rank_urls = [
    url("^querycharrank$", Qquerycharrank.as_view()),
    url("^querycharrankcount$", Qquerycharrankcount.as_view())
]