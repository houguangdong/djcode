# -*- coding:utf-8 -*-
import requests
import json
from config.platform_mapping import platform
from core.view import View


class QueryCharByCharId(View):
    def get(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.do(request, *args, **kwargs)

    def do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        serverId = int(parameter_info["serverId"])          # 区服
        roleId = parameter_info["roleId"]  # 角色ID

        rets = []
        if serverId == 0:
            for sid in platform["server"].keys():
                ret = call_on(sid, roleId)
                rets.extend(ret)
        else:
            ret = call_on(serverId, roleId)
            rets.extend(ret)
        return self.HttpResponse(json.dumps(rets))


def call_on(serverId, roleId):
    host = platform["server"][serverId]["host"]
    port = platform["server"][serverId]["port"]
    url = "http://%s:%s/server_mba_api/querycharbycharid" % (host, port)
    parameters = {"roleId": roleId}
    ret = requests.post(url, parameters)
    if ret.status_code != 200:
        return []
    return json.loads(ret.text)

