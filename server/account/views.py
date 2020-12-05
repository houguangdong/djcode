# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
from django.conf.global_settings import SECRET_KEY
from django.http import HttpResponse

from apps.logics.utils.client_ip import get_addr
from apps.logics.utils.string_handler import str_change_md5
from rklib.utils import rkjson as json
import hashlib
import time
import hmac

from django.shortcuts import render

# Create your views here.
from apps.models.account import Account
from apps.models.account_mapping import AccountMapping
from apps.models.account_user import AccountUser
from apps.models.account_login_check import AccountLoginCheck
import re
from rklib.utils.guuid import get_uuid
from apps.common.project_const import const
from apps.logics.utils.time_handler import get_current_time, get_day_start_time, get_day_end_time


def register(request):
    """
    注册帐号
    :param request:
    :return:
    """
    request_context = request._request_context

    account_number = request_context.get_parameter('aname')     # 用户名
    pwd = request_context.get_parameter('pwd')                  # 密码

    res_code, msg = _check(account_number, pwd)
    if res_code:
        return HttpResponse(json.dumps({'r': res_code, 'msg': msg}), content_type='application/json')

    account = Account.get(account_number)
    if isinstance(account, Account):
        return HttpResponse(json.dumps({'r': 5, 'msg': 'accounts already exist'}), content_type='application/json')

    openid = get_uuid()
    openkey = _generate_token(SECRET_KEY)
    Account._install(account_number, str_change_md5(pwd), openid)
    AccountMapping._install(openid, account_number, openkey)

    return HttpResponse(json.dumps({'r': 0, 'msg': 'ok', 'openid': openid, 'openkey': openkey}), content_type='application/json')


def auto_register(request):
    """快速注册
    @param request:
    @return:
    """
    openid = get_uuid()
    account_number = des2thi(int(openid, 16))
    pwd = '123456'
    openkey = _generate_token(SECRET_KEY)
    Account._install(account_number, str_change_md5(pwd), openid)
    AccountMapping._install(openid, account_number, openkey)

    return HttpResponse(json.dumps({'r': 0, 'msg': 'ok', 'aname': account_number, 'pwd': pwd, 'openid': openid, 'openkey': openkey}))


def _generate_token(key, expire=31536000):
    """
    :param key:
    :param expire:
    :return:
    """
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, hashlib.sha1).hexdigest()
    token = ts_str + ":" + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def _check(account_number, pwd):
    res_flag = _check_account_number_format(account_number)
    if not res_flag:
        return 1, 'account name format error'
    res_flag = _check_account_number_size(account_number)
    if not res_flag:
        return 2, 'account name size error'
    res_flag = _check_pwd_format(pwd)
    if not res_flag:
        return 3, 'password format error'
    res_flag = _check_pwd_size(pwd)
    if not res_flag:
        return 4, 'password size error'
    return 0, 'ok'


def _check_account_number_format(account_number):
    """校验帐号格式 英文 数字 下划线构成
    \w 匹配字母或数字或下划线或汉字 等价于 '[^A-Za-z0-9_]'
    @param account_number:
    @return:
    """
    pattern = re.compile(r'^\w+$')
    m = pattern.match(account_number)
    if not m:
        return False
    return True

def _check_account_number_size(account_number):
    """校验帐号长度 30
    @param account_number:
    @return:
    """
    if len(account_number) > 30:
        return False
    return True

def _check_pwd_format(pwd):
    """
    @param pwd:
    @return:
    """
    pattern = re.compile(r'^\w+$')
    m = pattern.match(pwd)
    if not m:
        return False
    return True

def _check_pwd_size(pwd):
    """
    @param pwd:
    @return:
    """
    if len(pwd) < 6:
        return False
    return True


def login(request):
    """
    登陆帐号
    :param request:
    :return:
    """
    regip = get_addr(request)
    # print  'account login ip:', regip
    request_context = request._request_context

    account_number = request_context.get_parameter('aname')    # 用户名
    pwd = request_context.get_parameter('pwd')  # 密码

    account = Account.get(account_number)

    if not isinstance(account, Account):
        return HttpResponse(json.dumps({'r': 1, 'msg': 'account or password mistake'}),
                            content_type='application/json')

    if account_number == account.account_number and str_change_md5(pwd) == account.account_pwd:
        openid = account.openid
        accmpp = AccountMapping.get(openid)

        if not isinstance(accmpp, AccountMapping):
            return HttpResponse(json.dumps({'r': 1, 'msg': 'account or password mistake'}),
                                content_type='application/json')

        openkey = accmpp.openkey

        return HttpResponse(json.dumps({'r': 0, 'msg': 'ok', 'openid': openid, 'openkey': openkey}),
                            content_type='application/json')

    return HttpResponse(json.dumps({'r': 1, 'msg': 'account or password mistake'}), content_type='application/json')


def users(request):
    request_context = request._request_context

    openid = request_context.get_parameter('openid')    # 用户名

    account_user = AccountUser.get(openid)

    user_info = []

    if not isinstance(account_user, AccountUser):
        return HttpResponse(json.dumps({'r': 0, 'msg': 'ok', 'users': json.dumps(user_info)}), content_type='application/json')

    for key, value in account_user.user_info.iteritems():
        user_info.append(key)
        user_info.append(value)
    return HttpResponse(json.dumps({'r': 0, 'msg': 'ok', 'users': json.dumps(user_info)}), content_type='application/json')


def modify_info(request):
    request_context = request._request_context

    serverid = request_context.get_parameter('serverid')
    openid = request_context.get_parameter('openid')
    lv = request_context.get_parameter('lv')

    account_user = AccountUser.get(openid)

    if not isinstance(account_user, AccountUser):
        account_user = AccountUser._install(openid, is_put=False)
        account_user.modify_info(serverid=serverid, lv=lv)
    else:
        account_user.modify_info(serverid=serverid, lv=lv)
    return HttpResponse(json.dumps({'r': 0, 'msg': 'ok'}), content_type='application/json')


def des2thi(string_num):
    base = [str(x) for x in range(10)] + [chr(x) for x in range(ord('A'), ord('A') + 22)]
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 32)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])


def login_check(request):
    """
    请求登录信息
    :param request:
    :return:
    """
    request_context = request._request_context
    openid = request_context.params.get('openid')
    openkey = request_context.params.get('openkey')
    channel_id = int(request_context.params.get('channel_id'))  # 渠道id(string)
    os_type = request_context.params.get('os_type')  # 设备类型(string)
    platform_id = request_context.params.get('platform_id')  # 平台id(string)
    app_version = request_context.params.get('app_version')  # 客户端app版本号(string)
    build_version = request_context.params.get('build_version')  # svn版本号(string)
    res_version = request_context.params.get('res_version')  # 资源版本号(string)
    uid = request_context.params.get('uid')  # uid(string) AccountId
    age_stage = int(request_context.params.get('age'))  # age：年龄段（int)   # 防沉迷值. 18:成年, 16: 16~18岁, 8: 8~16岁, 0: 0~8岁 -1: 未成年,
    istourist = int(request_context.params.get('istourist'))  # istourist ：是否是游客(int) # -2:未实名

    account_login_check = AccountLoginCheck.get(openid)

    if not isinstance(account_login_check, AccountLoginCheck):
        AccountLoginCheck._install(openid, openkey, channel_id, os_type, platform_id, app_version, build_version, res_version, uid, age_stage, istourist)
    else:
        if account_login_check.istourist == '-2' and account_login_check.enter_game == 1:
            return HttpResponse(json.dumps({'r': 1, 'msg': 'istourist is only play one time'}), content_type='application/json')
        if account_login_check.age_stage < const.PLAY_AGE_STAGE[0]:
            if get_day_start_time() + const.PLAY_LIMIT[0] <= get_current_time() <= get_day_end_time() + const.PLAY_LIMIT[1]:
                return HttpResponse(json.dumps({'r': 2, 'msg': 'minor player is not play between 22:00 and tomorrow 8:00'}), content_type='application/json')
            if account_login_check.play_time >= const.PLAY_TIME:
                return HttpResponse(json.dumps({'r': 3, 'msg': 'minor player is only play 90 minute'}), content_type='application/json')
        account_login_check.login_info(openkey, channel_id, os_type, platform_id, app_version, build_version, res_version, uid, age_stage, istourist)
        account_login_check.refresh_data()
    return HttpResponse(json.dumps({'r': 0, 'msg': 'ok'}), content_type='application/json')


def modify_enter_game(request):
    """
    游戏服务器调用 游客一辈子只能玩一次游戏
    :param request:
    :return:
    """
    request_context = request._request_context
    openid = request_context.params.get('openid')
    enter_game = int(request_context.params.get('enter_game'))
    account_login_check = AccountLoginCheck.get(openid)
    if not isinstance(account_login_check, AccountLoginCheck):
        return HttpResponse(json.dumps({'r': 1, 'msg': 'modify enter game status fail'}), content_type='application/json')
    account_login_check.modify_enter_game(enter_game, is_put=True)
    return HttpResponse(json.dumps({'r': 0, 'msg': 'ok'}), content_type='application/json')


def modify_play_time(request):
    """
    游戏服务器调用 修改未成年玩家玩游戏的时长
    :param request:
    :return:
    """
    request_context = request._request_context
    openid = request_context.params.get('openid')
    play_time = int(request_context.params.get('play_time'))
    account_login_check = AccountLoginCheck.get(openid)
    if not isinstance(account_login_check, AccountLoginCheck):
        return HttpResponse(json.dumps({'r': 1, 'msg': 'modify add play time fail'}), content_type='application/json')
    if account_login_check.age_stage >= const.PLAY_AGE_STAGE[0]:
        return HttpResponse(json.dumps({'r': 2, 'msg': 'player is big people'}), content_type='application/json')
    account_login_check.modify_play_time(play_time, is_put=True)
    return HttpResponse(json.dumps({'r': 0, 'msg': 'ok'}), content_type='application/json')


def modify_recharge_money(request):
    """
    游戏服务器调用 修改未成年玩家充值金额
    :param request:
    :return:
    """
    request_context = request._request_context
    openid = request_context.params.get('openid')
    age = int(request_context.params.get('age'))
    add_money = int(request_context.get('add_money'))
    account_login_check = AccountLoginCheck.get(openid)
    if not isinstance(account_login_check, AccountLoginCheck):
        return HttpResponse(json.dumps({'r': 1, 'msg': 'modify recharge money fail'}), content_type='application/json')
    if account_login_check.age_stage != age:
        return HttpResponse(json.dumps({'r': 2, 'msg': 'recharge fail'}), content_type='application/json')
    if not (account_login_check.recharge_week_money < const.RECHARGE_LIMIT[account_login_check.age_stage][0] and \
            account_login_check.recharge_month_money < const.RECHARGE_LIMIT[account_login_check.age_stage][1]):
        return HttpResponse(json.dumps({'r': 3, 'msg': 'recharge limit'}), content_type='application/json')
    account_login_check.modify_recharge_money(add_money, is_put=True)
    return HttpResponse(json.dumps({'r': 0, 'msg': 'ok'}), content_type='application/json')