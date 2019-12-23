#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/18 10:33

# Django 发送邮件
# 我们常常会用到一些发送邮件的功能，比如有人提交了应聘的表单，可以向HR的邮箱发邮件，这样，HR不看网站就可以知道有人在网站上提交了应聘信息。
# 1. 配置相关参数
# 如果用的是 阿里云的企业邮箱，则类似于下面：
# 在 settings.py 的最后面加上类似这些
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = False
# EMAIL_HOST = 'smtp.tuweizhong.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'mail@tuweizhong.com'
# EMAIL_HOST_PASSWORD = 'xxxx'
# DEFAULT_FROM_EMAIL = 'mail@tuweizhong.com'
# 或者
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'xxx@qq.com' # 帐号
# EMAIL_HOST_PASSWORD = 'p@ssw0rd'  # 密码
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# EMAIL_USE_SSL 和 EMAIL_USE_TLS 是互斥的，即只能有一个为 True。
# DEFAULT_FROM_EMAIL 还可以写成这样：
# DEFAULT_FROM_EMAIL = 'tuweizhong <tuweizhong@163.com>'

# 其它邮箱参数可能登陆邮箱看寻找帮助信息，也可以尝试在搜索引擎中搜索："SMTP 邮箱名称"，比如："163 SMTP" 进行查找。

# 2. 发送邮件：
# 2.1 官网的一个例子：
# from django.core.mail import send_mail
# send_mail('Subject here', 'Here is the message.', 'from@example.com',
#           ['to@example.com'], fail_silently=False)

# 2.2 一次性发送多个邮件：
# from django.core.mail import send_mass_mail
# message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
# message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])
# send_mass_mail((message1, message2), fail_silently=False)
# 备注：send_mail 每次发邮件都会建立一个连接，发多封邮件时建立多个连接。
# 而 send_mass_mail 是建立单个连接发送多封邮件，所以一次性发送多封邮件时 send_mass_mail 要优于 send_mail。

# 2.3 如果我们想在邮件中添加附件，发送 html 格式的内容
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
#
# from_email = settings.DEFAULT_FROM_EMAIL
# # subject 主题 content 内容 to_addr 是一个列表，发送给哪些人
# msg = EmailMultiAlternatives(subject, content, from_email, [to_addr])
# msg.content_subtype = "html"
# # 添加附件（可选）
# msg.attach_file('./twz.pdf')
# # 发送
# msg.send()

# 上面的做法可能有一些风险，除非你确信你的接收者都可以阅读 html 格式的 邮件。
# 为安全起见，你可以弄两个版本，一个纯文本(text/plain)的为默认的，另外再提供一个 html 版本的（好像好多国外发的邮件都是纯文本的）
# from __future__ import unicode_literals
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# subject = '来自自强学堂的问候'
# text_content = '这是一封重要的邮件.'
# html_content = '<p>这是一封<strong>重要的</strong>邮件.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to @ youemail.com])
# msg.attach_alternative(html_content, "text/html")
# msg.send()