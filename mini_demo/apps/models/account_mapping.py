#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 21:00

from rklib.model import BaseModel


class AccountMapping(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)

        self.openid = None
        self.account_number = None
        self.openkey = None

    @classmethod
    def _install(cls, openid, account_number, openkey):
        account_mapping = cls()
        account_mapping.openid = openid
        account_mapping.account_number = account_number
        account_mapping.openkey = openkey
        account_mapping.put()

        return account_mapping