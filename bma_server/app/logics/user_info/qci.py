# -*- coding:utf-8 -*-
from app.logics.utility.time_handle import int_format_time
from config.mapping_conf import platform_str_mapping
from core.views import ResetView
from config.game_server_config import platform_server_info
import requests


class Qci(ResetView):
    """
    查询玩家信息
    """

    def post(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self._do(request, *args, **kwargs)

    def _do(self, request, *args, **kwargs):
        parameter_info = self.parameters
        platformId = parameter_info["platformId"]  # 平台
        serverId = int(parameter_info["serverId"])  # 区服
        get_type = int(parameter_info["type"])  # 参数类型(1-角色ID查询； 2-角色名查询)
        val = parameter_info["val"]  # 参数值
        platformId = platform_str_mapping.get(platformId, platformId)

        response_dic = {
            "status": "success",
            "code": 1,
            "info": "",
            "roleId": "",  # 角色id 0
            "userId": "",  # 用户id 1
            "roleName": "",  # 角色名 1
            "usedRole": "",  # 曾用角色 0
            "majorId": "",  # 职业id 0
            "majorName": "",  # 职业名称 0
            "level": "",  # 等级 1
            "vipLevel": "",  # vip等级 1
            "power": "",  # 战力 0
            "empiricalValue": "",  # 经验值 1
            "realm": "",  # 境界 0
            "ownForce": "",  # 势力 0
            "starCoin": "",  # 绑定元宝 0
            "topUpStarCoin": "",  # 元宝 1
            "copper": "",  # 金币 1
            "xiaYiValue": "",  # 侠义值 0
            "channel": "",  # 渠道 0
            "mobile": "",  # 手机号 0
            "currentOnlineTime": "",  # 当前在线时间 0
            "totalOnline": "",  # 在线总时间 0
            "rechargeAmount": "",  # 充值金额 1
            "channelId": "",  # 渠道id 0
            "bannedType": "",  # 封禁状态(1-禁止发言；0-冻结账号；-1正常) 1
            "createTime": "",  # 创建时间 1
            "lastOptTime": "",  # 最后操作时间 0
            "lastLoginTime": "",  # 最后登陆时间 1
            "lastLoginIP": "",  # 最后登陆ip 0
            "clientVersion": "",  # 客户端版本 0
            "lastRechargeTime": "",  # 最近充值时间 1
            "attackValue": 0,  # 攻击 0
            "defenceValue": 0,  # 防御 0
            "hpValue": 0,  # 生命 0
            "strikeRatio": 0,  # 暴击率 0
            "hitValue": 0,  # 命中 0
            "dodgeValue": 0,  # 闪避 0
            "attackPower": 0,  # 攻击强度 0
            "moveSpeed": 0,  # 移动速度 0
            "elementAttack": 0,  # 元素攻击 0
            "elementDefense": 0,  # 元素防御 0
            "damageBonus": 0,  # 伤害加成 0
            "damageReduction": 0,  # 伤害减免 0
            "criticalDamage": 0,  # 暴击加成 0
            "explosiveReduction": 0,  # 爆伤减免 0
            "rechargeMoney": 0,  # 最近充值金额 1
            "divineTroopsLists": [
                {
                    "divineTroopsId": "",  # 神兵id
                    "divineTroopsName": "",  # 神兵名称
                    "divineTroopsLevel": "",  # 神兵等级
                    "divineTroopsAttr": "",  # 神兵属性
                }
            ],  # 神兵列表 0
            "shenwenLists": [
                {
                    "shenwenId": "",  # 神纹id
                    "shenwenName": "",  # 神纹名称
                    "shenwenLevel": "",  # 神纹等级
                    "shenwenAttr": "",  # 神纹属性
                }
            ],  # 神纹列表 0
            "zuoqiLists": [
                {
                    "zuoqiId": "",  # 坐骑id
                    "zuoqiName": "",  # 坐骑名称
                    "zuoqiLevel": "",  # 坐骑等级
                    "zuoqiAttr": "",  # 坐骑属性
                }
            ],  # 坐骑列表 0
            "magicWingLists": [
                {
                    "magicWingId": "",  # 幻翼id
                    "magicWingName": "",  # 幻翼名称
                    "magicWingLevel": "",  # 幻翼等级
                    "magicWingAttr": "",  # 幻翼属性
                }
            ],  # 幻翼列表 0
            "entourageLists": [
                {
                    "entourageId": "",  # 随从id
                    "entourageName": "",  # 随从名称
                    "entourageLevel": "",  # 随从等级
                    "entourageOrder": "",  # 随从阶数
                    "entourageAttr": "",  # 随从属性
                }
            ],  # 随从列表 0
            "goodsLists": [  # 背包列表
                {
                    "goodsId": "",  # 物品id
                    "goodsName": "",  # 物品名称
                    "quantity": "",  # 数量
                    "status": "",  # 状态（备包、仓库、拍卖中等）
                }
            ],
            "rechargeInfoLists": [  # 充值列表
                {
                    "platformOrderNo": "",  # 平台单号
                    "rechargeMoney": "",  # 充值金额
                    "rechargeVcoin": "",  # 充值元宝
                    "giftId": "",  # 充值礼包id
                    "giftName": "",  # 充值礼包名称
                    "rechargeTime": "",  # 充值时间
                    "isTrue": "",  # 是否真实充值(0-否；1-是)
                }
            ]
        }  # 基础返回数据

        if not platform_server_info.get(platformId, None):  # 判断平台游戏服务器是否存在
            response_dic.update({"status": "fail", "code": 0})
            return self.HttpResponse(response_dic)

        platform_server_conf = platform_server_info[platformId]

        url = "http://%s:%s/platform_server/qci" % (platform_server_conf["host"], platform_server_conf["port"])
        send_parameter = {"serverId": serverId, "type": get_type, "val": val}
        http_info = requests.post(url, send_parameter)
        if http_info.status_code != 200:
            response_dic.update({"info": "server conn err", "status": "fail", "code": 0})
            return self.HttpResponse(response_dic)

        http_response_info = self.json_loads(http_info.text)

        if not http_response_info["status"]:
            response_dic.update({"status": "fail", "code": 0, "info": http_response_info["errorMessage"]})
            return self.HttpResponse(response_dic)
        del http_response_info["errorMessage"]
        response_dic.update(http_response_info)
        response_dic["lastLoginTime"] = int_format_time(response_dic["lastLoginTime"])
        response_dic["createTime"] = int_format_time(response_dic["createTime"])
        response_dic["lastRechargeTime"] = int_format_time(response_dic["lastRechargeTime"])

        for index, val in enumerate(response_dic["rechargeInfoLists"]):
            val["rechargeTime"] = int_format_time(val["rechargeTime"])
            response_dic["rechargeInfoLists"][index] = val
        return self.HttpResponse(response_dic)