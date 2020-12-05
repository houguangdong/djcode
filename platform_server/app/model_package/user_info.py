# -*- coding:utf-8 -*-
import time
from django.db import models


class BannedExt(models.Model):
    only_uid = models.CharField(max_length=32, primary_key=True)  # 用户id和serverid唯一值
    user_name = models.TextField(max_length=255)  # 用户名字
    remark = models.TextField(blank=False)


class Banned(models.Model):
    only_uid = models.CharField(max_length=32, primary_key=True)  # 用户id和serverid唯一值
    user_id = models.CharField(max_length=16)  # 用户id
    server_id = models.IntegerField()  # 服务器id
    state = models.IntegerField(choices=((-1, "正常"), (0, "冻结账号"), (1, "禁止发言")))  # 账号状态
    operate_time = models.BigIntegerField()  # 操作时间
    banned_time = models.BigIntegerField()  # 封禁时间
    unlock_time = models.BigIntegerField()  # 解封时间
    extend_info = models.OneToOneField("BannedExt")  # 封禁原因

    @classmethod
    def add_banned_info(cls, uid, server_id, user_name, state, operate_time, banned_time, unlock_time, remark):
        only_uid = "%s_%s" % (uid, server_id)
        banned_ext_objs = BannedExt.objects.filter(only_uid=only_uid)
        get_obj = cls.objects.filter(only_uid=only_uid)
        if banned_ext_objs:
            remark_obj = BannedExt.objects.get(only_uid=only_uid)
            remark_obj.user_name = user_name
            remark_obj.remark = remark
            remark_obj.save()
        else:
            remark_obj = BannedExt.objects.create(only_uid=only_uid, user_name=user_name, remark=remark)
        if get_obj:
            banned_obj = cls.objects.get(only_uid=only_uid)
            banned_obj.operate_time = operate_time
            banned_obj.unlock_time = int(time.time()) if unlock_time is None else int(unlock_time)
            banned_obj.extend_info = remark_obj
            if state:
                banned_obj.state = state
                banned_obj.banned_time = banned_time
            else:
                banned_obj.state = -1
            banned_obj.save()
        else:
            banned_obj = cls.objects.create(only_uid=only_uid, user_id=uid, server_id=server_id, state=state,
                                            operate_time=operate_time, banned_time=banned_time, unlock_time=unlock_time,
                                            extend_info=remark_obj)
        return banned_obj