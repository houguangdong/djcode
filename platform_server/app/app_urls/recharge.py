# -*- coding:utf-8 -*-
from django.conf.urls import url
from app.logics.recharge.simulaterecharge import SimulateRecharge
from app.logics.recharge.querycharbycharid import QueryCharByCharId

recharge_url = [
    url("^simulaterecharge", SimulateRecharge.as_view()),
    url("^querycharbycharid", QueryCharByCharId.as_view()),
]