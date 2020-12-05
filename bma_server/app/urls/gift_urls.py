# -*- coding:utf-8 -*-

from django.conf.urls import url

from app.logics.gift.create_gift_card import CreateGiftCard
from app.logics.gift.create_gift_group import CreateGiftGroup
from app.logics.gift.get_available_gift_card import GetAvailableGiftCard
from app.logics.gift.modify_gift_card_state import ModifyGiftCardState
from app.logics.gift.query_gift_card_user_info import QueryGiftCardUserInfo
from app.logics.gift.query_gift_group import QueryGiftGroup
from app.logics.gift.delete_gift_group import DeleteGiftGroup
from app.logics.gift.query_gift_card import QueryGiftCard
from app.logics.gift.use_cdkey import UseCdKey

gift_urls = [
    url("^creategiftgroup$", CreateGiftGroup.as_view()),
    url("^creategiftcard$", CreateGiftCard.as_view()),
    url("^getavailablegiftcard$", GetAvailableGiftCard.as_view()),
    url("^querygiftcarduserinfo$", QueryGiftCardUserInfo.as_view()),
    url("^querygiftgroup$", QueryGiftGroup.as_view()),
    url("^deletegiftgroup$", DeleteGiftGroup.as_view()),
    url("^querygiftcard$", QueryGiftCard.as_view()),
    url("^usecdkey", UseCdKey.as_view()),
    url("^modifygiftcardstate", ModifyGiftCardState.as_view())
]
