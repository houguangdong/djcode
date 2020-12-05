# -*- coding:utf-8 -*-
import binascii
import pickle

from config.mapping_conf import platform_str_mapping, platform_int_mapping
from core.views import ResetView
from config.game_server_config import platform_server_info
import requests
import json


class Querycharrank(ResetView):
    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        platformId = parameter_info["platformId"]  # 平台
        serverId = int(parameter_info["serverId"])  # 区服
        get_type = int(parameter_info["type"])  # 参数类型(1-玩家等级； 2-充值金额)
        p = parameter_info["p"]  # 页码
        pageSize = parameter_info["pageSize"]  # 每页显示数量

        platformId = platform_str_mapping.get(platformId, platformId)

        if not platform_server_info.get(platformId, None):  # 判断平台游戏服务器是否存在
            return self.HttpResponse({"status": "fail", "code": 0})
        host = platform_server_info[platformId]["host"]
        port = platform_server_info[platformId]["port"]
        name = platform_server_info[platformId]['name']
        totalCount = _get_totalCount(host, port, serverId)
        dataList = _get_record(host, port, platformId, name, serverId, p, pageSize)
        response_dic = {
            'status': 'ok',
            'code': '1',
            'info': '',
            'totalCount': totalCount,
            'dataList': dataList
        }

        return self.HttpResponse(json.dumps(response_dic))


def _get_totalCount(host, port, serverId):
    """
    @param host:
    @param port:
    @param serverId:
    @return:
    """
    totalCount = 0
    url = "http://%s:%s/platform_server/querycharrankcount" % (host, port)
    send_parameter = {"serverId": serverId}
    try:
        http_info = requests.post(url, send_parameter)
        http_info.raise_for_status()
        result = json.loads(http_info.text)
        totalCount = result['totalCount']
    except Exception as e:
        import traceback
        traceback.print_exc()
    return totalCount


def _get_record(host, port, platformId, platformName, serverId, p, pageSize):
    result = []
    url = "http://%s:%s/platform_server/querycharrank" % (host, port)
    send_parameter = {"serverId": serverId, 'p': p, 'pageSize': pageSize}
    try:
        http_info = requests.post(url, send_parameter)
        http_info.raise_for_status()
        result = json.loads(http_info.text)
    except Exception as e:
        import traceback
        traceback.print_exc()

    for item in result:
        item['platformId'] = platform_int_mapping[platformId]
        item['platformName'] = platformName

    return result