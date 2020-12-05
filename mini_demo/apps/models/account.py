#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 15:57

import time
from rklib.model import BaseModel


class Account(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)

        self.account_number = None
        self.account_pwd = None
        self.openid = None
        self.add_time = None
        self.login_time = None

    @classmethod
    def _install(cls, account_number, account_pwd, openid):
        account = cls()
        account.account_number = account_number
        account.account_pwd = account_pwd
        account.openid = openid
        c_time = int(time.time())
        account.add_time = c_time
        account.login_time = c_time

        account.put()
        return account