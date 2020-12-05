# -*- coding:utf-8 -*-
from django.conf.urls import url
from app.logics.mail.send_mail import SendMail

mail_urls = [
    url("^sendmail", SendMail.as_view()),
]