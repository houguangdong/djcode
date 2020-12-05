#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 13:42

def login_pre(context):
    print 'login_pre'
    context.result["test"] += " login_pre"
    print context.result["test"]


def login_post(context):
    context.result["test"] += " login_post"