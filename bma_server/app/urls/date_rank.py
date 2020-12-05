# -*- coding:utf-8 -*-

from django.conf.urls import url
from app.logics.date_rank.querycharrank import Querycharrank


date_rank_urls = [
    url("^querycharrank$", Querycharrank.as_view()),
]