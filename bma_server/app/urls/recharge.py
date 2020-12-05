# -*- coding:utf-8 -*-
from django.conf.urls import url

from app.logics.recharge.queryrechargelist import QueryRechargeList
from app.logics.recharge.simulaterecharge import SimulateRecharge
from app.logics.recharge.querycharbycharid import QueryCharByCharId
recharge_urls = [
    url("^queryrechargelist", QueryRechargeList.as_view()),
    url("^simulaterecharge", SimulateRecharge.as_view()),
    # url("^querycharbycharid", QueryCharByCharId.as_view()),
]