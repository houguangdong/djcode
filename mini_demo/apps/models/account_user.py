#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 20:27

from rklib.model import BaseModel


class AccountUser(BaseModel):
    """
    Attributes:
        openid: 平台id
        user_info: 记录所有服中有帐号的角色等级信息
    """
    def __init__(self, openid=None):
        BaseModel.__init__(self)

        self.openid = openid
        self.user_info = {}

    @classmethod
    def _install(cls, openid, is_put=True):
        account_user = cls()
        account_user.openid = openid
        if is_put:
            account_user.put()
        return account_user

    def modify_info(self, serverid, lv):
        self.user_info[str(serverid)] = str(lv)
        self.put()
        return