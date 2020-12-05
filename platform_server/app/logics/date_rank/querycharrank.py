# -*- coding:utf-8 -*-
import json

from config.platform_mapping import platform
from core.view import View

import requests


class Qquerycharrank(View):
    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        serverId = int(parameter_info.get("serverId"))
        p = int(parameter_info.get("p"))
        pageSize = int(parameter_info.get("pageSize"))
        offset = p * pageSize - pageSize  # 开始
        max_num = offset + pageSize  # 结束
        game_server_conf = platform['server']
        result = []
        if serverId == 0:
            tmp = 0  # 总记录数量
            num_dict = _get_num()
            tmp_num_dict = num_dict.items()
            for index, item in enumerate(tmp_num_dict):
                print tmp, offset, item
                if tmp <= offset <= tmp + item[1] - 1:
                    serverId = item[0]
                    host = game_server_conf[serverId]['host']
                    port = game_server_conf[serverId]['port']
                    serverName = game_server_conf[serverId]['server_name']
                    result += _get_querycharrank(host, port, (offset - tmp) / pageSize, pageSize, serverId, serverName)
                    if (max_num > tmp + item[1]) and (index != len(tmp_num_dict) - 1):
                        next_item = tmp_num_dict[index + 1]
                        serverId = next_item[0]
                        host = game_server_conf[serverId]['host']
                        port = game_server_conf[serverId]['port']
                        serverName = game_server_conf[serverId]['server_name']
                        result += _get_querycharrank(host, port, 0, tmp + item[1] - max_num, serverId, serverName)
                tmp += item[1]
        else:
            host = game_server_conf[serverId]['host']
            port = game_server_conf[serverId]['port']
            serverName = game_server_conf[serverId]['server_name']
            result += _get_querycharrank(host, port, p, pageSize, serverId, serverName)

        return self.HttpResponse(json.dumps(result))


def _get_num():
    """取得所有游戏服中mysql记录总数
    @return:
    """
    game_server_conf = platform['server']  # 配置数据
    num_dict = {}
    for key, value in game_server_conf.items():
        host = value['host']
        port = value['port']
        count_url = "http://%s:%s/server_mba_api/querycharrankcount" % (host, port)
        try:
            response = requests.post(count_url)
            response.raise_for_status()
            result = json.loads(response.text)
            num = result['num']
            num_dict[key] = num
        except Exception, e:
            import traceback
            traceback.print_exc()
            continue
    return num_dict


def _get_querycharrank(host, port, offset, pageSize, serverId, serverName):
    """从游戏服拿取数据
    @param host:
    @param port:
    @param offset:
    @param pageSize:
    @return:
    """

    print "offset : %s, pageSize: %s" % (offset, pageSize)
    result = []
    user_url = "http://%s:%s/server_mba_api/querycharrank?p=%s&pageSize=%s" % (
        host, port, offset, pageSize)
    try:
        response = requests.post(user_url)
        response.raise_for_status()
        result = json.loads(response.text)
    except Exception, e:
        import traceback
        traceback.print_exc()

    ret = []
    for item in result:
        print item
        dic = {
            'serverId': serverId,  # 区服ID
            'serverName': serverName,  # 区服名称
            'userId': item['openid'],  # 账号id
            'roleId': item['uid'],  # 角色id
            'roleName': item['username'] if item['username'] else '',  # 角色名称
            'level': item['ulv'],  # 玩家等级
            'vipLevel': item['lv'],  # VIP等级
            'rechargeAmount': item['rechargeAmount'],  # 充值金额
        }
        ret.append(dic)
    return ret