#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 20:10

from django.conf.urls import include, url
from account import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^auto_register/$', views.auto_register),
    url(r'^login/$', views.login),
    url(r'^users/$', views.users),
    url(r'^modify_info/$', views.modify_info),

    url(r'^login_info/$', views.login_check),                       # 登录游戏验证 游戏客户端请求
    url(r'^modify_enter_game/$', views.modify_enter_game),          # 修改进入游戏状态, 游戏服调用
    url(r'^modify_play_time/$', views.modify_play_time),            # 修改玩游戏的时长
    url(r'^modify_recharge_money/$', views.modify_recharge_money),  # 修改未成年玩家充值的钱数
]