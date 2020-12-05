# -*- coding:utf-8 -*-
import hashlib
import random
import string
import time


class GiftGroup(object):
    """
    礼品卡分组信息
    """

    def __init__(self):
        self.giftGroupId = None
        self.giftGroupName = None
        self.description = None
        self.isEnabled = 0

    @classmethod
    def install_gift_group(cls, groupName, description, isEnabled=1):
        """
        安装礼品卡分组
        """
        gift_group_obj = cls()
        data = "%s_%s" % (str(time.time()), ''.join(random.sample(string.ascii_letters + string.digits, 32)))
        gift_group_obj.giftGroupId = hashlib.md5(data.encode("utf8")).hexdigest()
        gift_group_obj.giftGroupName = groupName
        gift_group_obj.description = description
        gift_group_obj.isEnabled = isEnabled
        return gift_group_obj