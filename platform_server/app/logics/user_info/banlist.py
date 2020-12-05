# -*- coding:utf-8 -*-
from django.db.models import Q

from app.model_package.user_info import Banned
from app.utility.time_handle import get_current_time
from core.view import View


class BanList(View):
    def post(self, request, *args, **kwargs):
        parameter_info = self.parameters
        serverId = int(parameter_info["serverId"])  # 区服
        page = int(parameter_info["page"])  # 页码
        pagesize = int(parameter_info["pagesize"])  # 每页现实数量
        bannedLists = []
        ret_data = {
            "bannedLists": [],
            "totalCount": 0
        }
        for banned_obj in Banned.objects.filter(Q(unlock_time__gte=get_current_time() + 1) | Q(unlock_time=0),
                                                server_id__gte=serverId):
            bannedLists.append({"roleId": banned_obj.user_id, "roleName": banned_obj.extend_info.user_name,
                                "bannedType": banned_obj.state, "lockTime": banned_obj.banned_time,
                                "unlockTime": banned_obj.unlock_time, "optTime": banned_obj.operate_time,
                                "remark": banned_obj.extend_info.remark})

        start_index = (pagesize * page) - pagesize
        end_index = pagesize * page
        ret_data["totalCount"] = len(bannedLists)
        ret_data["bannedLists"] = bannedLists[start_index:end_index]
        return self.HttpResponse(ret_data)