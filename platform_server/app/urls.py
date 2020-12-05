# -*- coding:utf-8 -*-
from app.app_urls.common import common_urls
from app.app_urls.gift import gift_urls
from app.app_urls.mail import mail_urls
from app.app_urls.user_info import user_info_urls
from app.app_urls.date_rank import date_rank_urls
from app.app_urls.channel_lock import channel_lock_urls
from app.app_urls.shout import shout
from app.app_urls.vip_double_reset import vip_double_reset_urls
from app.app_urls.recharge import recharge_url

urlpatterns = []
urlpatterns.extend(common_urls)
urlpatterns.extend(user_info_urls)
urlpatterns.extend(date_rank_urls)
urlpatterns.extend(mail_urls)
urlpatterns.extend(channel_lock_urls)
urlpatterns.extend(gift_urls)
urlpatterns.extend(shout)
urlpatterns.extend(vip_double_reset_urls)
urlpatterns.extend(recharge_url)