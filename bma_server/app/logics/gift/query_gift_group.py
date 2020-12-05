# -*- coding:utf-8 -*-
from app.mba_models.gift import Gift
from core.views import ResetView


class QueryGiftGroup(ResetView):
    """
    获取分组列表
    """

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        groupName = parameter_info["groupName"]  # 分组名称
        p = parameter_info["p"]  # 页码
        pageSize = parameter_info["pageSize"]  # 每页显示数量

        response_dic = {
            "status": "success",
            "code": 1,
            "info": "",
            "groupLists": [{
                "groupId": "分组id",
                "groupName": "分组名称",
                "description": "分组描述",
                "isEnabled": "是否有效",
            }, ],
        }

        groupLists = []
        totalCount = 0
        gift = Gift()
        gift_group_info = gift.get_gift_group_info(groupName)
        for gift_group_id, group_info in gift_group_info.items():
            cache = {"groupId": gift_group_id}
            for key, val in group_info.items():
                key = bytes.decode(key, "utf8") if isinstance(key, bytes) else key
                val = bytes.decode(val, "utf8") if isinstance(val, bytes) else val
                cache[key] = val
            groupLists.append(cache)
        totalCount = len(groupLists)
        if p:
            groupLists = groupLists[int(p) * int(pageSize) - int(pageSize):int(pageSize) * int(p)]
        response_dic.update({"groupLists": groupLists})
        return self.HttpResponse(response_dic)