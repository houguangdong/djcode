#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/15 12:18

import datetime

from rklib.model import BaseModel
from apps.common import rkauth
from apps.common.project_const import const
from apps.logics.utils.time_handler import get_current_time

const.INITICONS = 40001


class User(BaseModel):
    """用户基本信息
    Attributes:
        uid: 用户ID str
        openid: 平台id
        username: 名称 str
        # gender: 性别 str
        icons: 头像 str
        # state: 账号状态 0-正常  1-冻结 2-注销 int
        channel_id: 渠道
        add_time: 添加应用时间 datetime
        login_time: 登录时间 datetime
        login_ip: 登录ip
        session_key: session_key

        game_info: 用户游戏信息
        ext_info: 扩展信息
        friend: 用户好友
        package: 用户包裹
    """

    def __init__(self, uid=None):
        """初始化用户基本信息
        Args:
            uid: 用户游戏ID
        """
        BaseModel.__init__(self)

        self.uid = uid              # 用户uid
        self.openid = None          # 平台id
        self.username = None        # 用户姓名
        # self.gender = None          # 性别
        self.icons = None           # 头像
        # self.state = 0              # 账号状态 0 正常，1 冻结，2 注销
        self.channel_id = 0         # 渠道
        self.add_time = None        # 安装时间
        self.login_time = None      # 最后登录时间
        self.login_ip = None    # 登录ip
        self.session_key = None # session_key

        self._game_info = None      # 用户游戏属性
        self._ext_info = None       # 扩展信息
        self._friend = None         # 用户好友
        self._package = None        # 用户包裹

    @property
    def game_info(self):
        """用户游戏属性
        """
        if not self._game_info:
            from apps.models.game_info import GameInfo

            self._game_info = GameInfo.get(self.uid)

            if not self._game_info:
                self._game_info = GameInfo._install(self.uid)

        return self._game_info

    @property
    def ext_info(self):
        """用户游戏扩展属性
        """
        if not self._ext_info:
            from apps.models.ext_info import ExtInfo

            self._ext_info = ExtInfo.get(self.uid)

            if not self._ext_info:
                self._ext_info = ExtInfo._install(self.uid)

        return self._ext_info

    @property
    def friend(self):
        """用户好友
        """
        if not self._friend:
            from apps.models.friend import Friend

            self._friend = Friend.get(self.uid)
            if not self._friend:
                self._friend = Friend._install(self.uid)

        return self._friend

    @property
    def package(self):
        """用户包裹
        """
        if not self._package:
            from apps.models.package import Package

            self._package = Package.get(self.uid)
            if not self._package:
                self._package = Package._install(self.uid)

        return self._package

    @classmethod
    def _install(cls, request_context):
        """检测安装用户

        Args:
            request_context: RequestContext实例
        """
        user_cookie = rkauth.auth_cookie(request_context)

        if user_cookie is None:
            return None, None

        if user_cookie in [-1020, -1021, -1022, -1301]:
            return user_cookie, None

        rk_user = cls.get(user_cookie['rk_uid'])

        if isinstance(rk_user, cls):
            pass
        else:
            rk_user = cls._install_new_user(user_cookie['rk_uid'], user_cookie['openid'], user_cookie.get('channel_id', 0))

        rk_user.openid = user_cookie['openid']
        rk_user.openkey = user_cookie['openkey']

        return 0, rk_user

    @classmethod
    def _install_new_user(cls, uid, openid, channel_id):
        """安装新用户，初始化用户及游戏数据
        Args:
            uid: 用户ID
            openid: 帐号唯一ID
        Return:
            rk_user: user object
        """
        rk_user = cls(uid)
        rk_user.openid = openid
        rk_user.icons = const.INITICONS
        rk_user.channel_id = channel_id
        rk_user.add_time = get_current_time()       # datetime.datetime.now()
        rk_user.login_time = get_current_time()
        rk_user._isfirst = 1
        rk_user.put()
        return rk_user