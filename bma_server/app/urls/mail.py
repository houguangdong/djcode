# -*- coding:utf-8 -*-

from django.conf.urls import url

from app.logics.mail.sendmail import SendMail
from app.logics.mail.sb_sendmail import SBSendMail

mail_urls = [
    url("^sendmailbychannelandserveridtochar", SendMail.as_view()),
    url("^sendmail", SBSendMail.as_view()),
]