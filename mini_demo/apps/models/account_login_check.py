#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/17 14:55


from rklib.model import BaseModel
from apps.common.project_const import const
from apps.logics.utils.time_handler import get_current_time, check_same_day


class AccountLoginCheck(BaseModel):
    """
    Attributes:
        openid: 平台id
    """
    def __init__(self, openid=None):
        BaseModel.__init__(self)

        self.openid = openid
        self.openkey = None
        self.channel_id = 0
        self.os_type = None
        self.platform_id = None
        self.app_version = None
        self.build_version = None
        self.res_version = None
        self.uid = None
        self.age_stage = 0
        self.istourist = 0
        self.enter_game = 0                         # 游客一辈子只能登录一次 0 | 1
        self.refresh_play_time = None               # 每天刷新玩家的游戏时长
        self.play_time = 0                          # 未成年玩游戏的时间 秒数
        self.refresh_week_time = None               # 每周刷新未成年充值金额
        self.recharge_week_money = 0                # 每周未成年充值金额
        self.refresh_month_time = None              # 每月刷新未成年充值金额
        self.recharge_month_money = 0               # 每月未成年充值金额

    @classmethod
    def _install(cls, openid, openkey, channel_id, os_type, platform_id, app_version, build_version, res_version, uid, age, istourist):
        '''
        初始化信息
        :param openid:
        :param openkey:
        :param channel_id:
        :param os_type:
        :param platform_id:
        :param app_version:
        :param build_version:
        :param res_version:
        :param uid:
        :param age:
        :param istourist:
        :return:
        '''
        account_login_check = cls()
        account_login_check.openid = openid
        account_login_check.openkey = openkey
        account_login_check.channel_id = channel_id  # 渠道id(string)
        account_login_check.os_type = os_type  # 设备类型(string)
        account_login_check.platform_id = platform_id  # 平台id(string)
        account_login_check.app_version = app_version  # 客户端app版本号(string)
        account_login_check.build_version = build_version  # svn版本号(string)
        account_login_check.res_version = res_version  # 资源版本号(string)
        account_login_check.uid = uid  # uid(string) AccountId
        account_login_check.age_stage = age  # age：年龄段（int)    # 防沉迷值. 18:成年, 16: 16~18岁, 8: 8~16岁, 0: 0~8岁 -1: 未成年,
        account_login_check.istourist = istourist  # istourist ：是否是游客(int)  # -2:未实名
        account_login_check.enter_game = 0
        account_login_check.refresh_play_time = get_current_time()
        account_login_check.play_time = 0
        account_login_check.refresh_week_time = get_current_time()
        account_login_check.recharge_week_money = 0
        account_login_check.refresh_month_time = get_current_time()
        account_login_check.recharge_month_money = 0
        account_login_check.put()
        return account_login_check

    def login_info(self, openkey, channel_id, os_type, platform_id, app_version, build_version, res_version, uid, age, istourist):
        '''
        修改登录信息
        :param openkey:
        :param channel_id:
        :param os_type:
        :param platform_id:
        :param app_version:
        :param build_version:
        :param res_version:
        :param uid:
        :param age:
        :param istourist:
        :return:
        '''
        self.openkey = openkey
        self.channel_id = channel_id
        self.os_type = os_type
        self.platform_id = platform_id
        self.app_version = app_version
        self.build_version = build_version
        self.res_version = res_version
        self.uid = uid
        self.age = age
        self.istourist = istourist
        self.put()
        return

    def refresh_data(self):
        '''
        刷新每天、每周、每月的数据
        :return:
        '''
        flag = False
        if not check_same_day(self.refresh_play_time):          # 每天玩游戏的时间
            self.refresh_play_time = get_current_time()
            self.play_time = 0
            flag = True
        if 1:                                                   # 每周玩家充值的钱数
            self.recharge_week_money = 0
            flag = True
        if 1:                                                   # 每月玩家充值的钱数
            self.recharge_month_money = 0
            flag = True
        if flag:
            self.put()

    def modify_enter_game(self, enter_game, is_put=False):
        '''
        修改游客是否玩过本游戏
        :param enter_game:
        :return:
        '''
        if self.istourist == -2 and self.enter_game == 0:
            self.enter_game = enter_game
        if is_put:
            self.put()

    def modify_play_time(self, play_time, add=True, is_put=False):
        '''
        统计未成年玩家玩游戏的时长
        :param play_time:
        :param add:
        :param is_put:
        :return:
        '''
        if self.age_stage < const.PLAY_AGE_STAGE[0]:
            if add:
                self.play_time += play_time
            else:
                self.play_time -= play_time
        if is_put:
            self.put()

    def modify_recharge_money(self, add_money, add=True, is_put=False):
        '''
        统计未成年玩家充值的金额
        :param add_money:
        :param add:
        :param is_put:
        :return:
        '''
        if self.recharge_week_money < const.RECHARGE_LIMIT[self.age_stage][0] and \
                self.recharge_month_money < const.RECHARGE_LIMIT[self.age_stage][1]:
            if add:
                self.recharge_week_money += add_money
                self.recharge_month_money += add_money
            else:
                self.recharge_week_money -= add_money
                self.recharge_month_money -= add_money
        if is_put:
            self.put()