#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/23 17:53

# Python/Django 微信接口
# 注册或登陆 微信公众平台 点击左侧的 开发者中心
# 填写相应的网址，Token(令牌) 是随便写的，你自己想写什么就写什么，微信验证时检验是否写的和服务器上的TOKEN一样，一样则通过。
# 关注一下自强学堂的微信号吧，可以随时随地查阅教程哦，体验一下自强学堂的微信的各种功能再阅读效果更佳！
# 自己动手写微信的验证： views.py
# coding=utf-8
import hashlib
import json
from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from auto_reply.views import auto_reply_main  # 修改这里

WEIXIN_TOKEN = 'write-a-value'


@csrf_exempt
def weixin_main(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    else:
        xml_str = smart_str(request.body)
        request_xml = etree.fromstring(xml_str)
        response_xml = auto_reply_main(request_xml)  # 修改这里
        return HttpResponse(response_xml)

# auto_reply_main 是用来处理消息，回复消息的，需要自己进一步完善。

# 使用第三方包实现：
# 关于Django开发微信，有已经做好的现在的包可以使用 wechat_sdk 这个包，使用文档 也比较完善，但是在处理加密一部分没有做，在微信公众平台上，需要用明文验证，如果要加密，自己参照微信官网的加密算法。
# 使用 wechat_sdk 的例子（自强学堂微信号简化后的例子）：
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage

WECHAT_TOKEN = 'zqxt'
AppID = ''
AppSecret = ''

# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)


@csrf_exempt
def index(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()

    # 关注事件以及不匹配时的默认回复
    response = wechat_instance.response_text(
        content=(
            '感谢您的关注！\n回复【功能】两个字查看支持的功能，还可以回复任意内容开始聊天'
            '\n【<a href="http://www.ziqiangxuetang.com">自强学堂手机版</a>】'
        ))
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        if content == '功能':
            reply_text = (
                '目前支持的功能：\n1. 关键词后面加上【教程】两个字可以搜索教程，'
                '比如回复 "Django 后台教程"\n'
                '2. 回复任意词语，查天气，陪聊天，讲故事，无所不能！\n'
                '还有更多功能正在开发中哦 ^_^\n'
                '【<a href="http://www.ziqiangxuetang.com">自强学堂手机版</a>】'
            )
        elif content.endswith('教程'):
            reply_text = '您要找的教程如下：'

        response = wechat_instance.response_text(content=reply_text)

    return HttpResponse(response, content_type="application/xml")

# 下面是一个更详细复杂的使用例子：
# models.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class KeyWord(models.Model):
    keyword = models.CharField(
        '关键词', max_length=256, primary_key=True, help_text='用户发出的关键词')
    content = models.TextField(
        '内容', null=True, blank=True, help_text='回复给用户的内容')

    pub_date = models.DateTimeField('发表时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    published = models.BooleanField('发布状态', default=True)

    def __unicode__(self):
        return self.keyword

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name

# views.py
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.http.response import HttpResponse, HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
#
# from wechat_sdk import WechatBasic
# from wechat_sdk.exceptions import ParseError
# from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage,
#                                  VideoMessage, LinkMessage, LocationMessage, EventMessage
#                                  )
#
# from wechat_sdk.context.framework.django import DatabaseContextStore
# from .models import KeyWord as KeyWordModel
#
# # 实例化 WechatBasic
# wechat_instance = WechatBasic(
#     token='zqxt',
#     appid='xx',
#     appsecret='xx'
# )
#
#
# @csrf_exempt
# def index(request):
#     if request.method == 'GET':
#         # 检验合法性
#         # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
#         signature = request.GET.get('signature')
#         timestamp = request.GET.get('timestamp')
#         nonce = request.GET.get('nonce')
#
#         if not wechat_instance.check_signature(
#                 signature=signature, timestamp=timestamp, nonce=nonce):
#             return HttpResponseBadRequest('Verify Failed')
#
#         return HttpResponse(
#             request.GET.get('echostr', ''), content_type="text/plain")
#
#     # POST
#     # 解析本次请求的 XML 数据
#     try:
#         wechat_instance.parse_data(data=request.body)
#     except ParseError:
#         return HttpResponseBadRequest('Invalid XML Data')
#
#     # 获取解析好的微信请求信息
#     message = wechat_instance.get_message()
#     # 利用本次请求中的用户OpenID来初始化上下文对话
#     context = DatabaseContextStore(openid=message.source)
#
#     response = None
#
#     if isinstance(message, TextMessage):
#         step = context.get('step', 1)  # 当前对话次数，如果没有则返回 1
#         # last_text = context.get('last_text')  # 上次对话内容
#         content = message.content.strip()  # 当前会话内容
#
#         if message.content == '新闻':
#             response = wechat_instance.response_news([
#                 {
#                     'title': '自强学堂',
#                     'picurl': 'http://www.ziqiangxuetang.com/static/images/newlogo.png',
#                     'description': '自强学堂致力于提供优质的IT技术教程, 网页制作，服务器后台编写，以及编程语言，如HTML,JS,Bootstrap,Python,Django。同时也提供大量在线实例，通过实例，学习更容易，更轻松。',
#                     'url': 'http://www.ziqiangxuetang.com',
#                 }, {
#                     'title': '百度',
#                     'picurl': 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
#                     'url': 'http://www.baidu.com',
#                 }, {
#                     'title': 'Django 教程',
#                     'picurl': 'http://www.ziqiangxuetang.com/media/uploads/images/django_logo_20140508_061519_35.jpg',
#                     'url': 'http://www.ziqiangxuetang.com/django/django-tutorial.html',
#                 }
#             ])
#             return HttpResponse(response, content_type="application/xml")
#
#         else:
#             try:
#                 keyword_object = KeyWordModel.objects.get(keyword=content)
#                 reply_text = keyword_object.content
#             except KeyWordModel.DoesNotExist:
#                 try:
#                     reply_text = KeyWordModel.objects.get(keyword='提示').content
#                 except KeyWordModel.DoesNotExist:
#                     reply_text = ('/:P-(好委屈，数据库翻个遍也没找到你输的关键词！\n'
#                                   '试试下面这些关键词吧：\nKEYWORD_LIST\n'
#                                   '<a href="http://www.rxnfinder.org">RxnFinder</a>'
#                                   '感谢您的支持！/:rose'
#                                   )
#
#         # 将新的数据存入上下文对话中
#         context['step'] = step + 1
#         context['last_text'] = content
#         context.save()  # 非常重要！请勿忘记！临时数据保存入数据库！
#
#         if 'KEYWORD_LIST' in reply_text:
#             keyword_objects = KeyWordModel.objects.exclude(keyword__in=[
#                 '关注事件', '测试', 'test', '提示']).filter(published=True)
#             keywords = ('{}. {}'.format(str(i), k.keyword)
#                         for i, k in enumerate(keyword_objects, 1))
#             reply_text = reply_text.replace(
#                 'KEYWORD_LIST', '\n'.join(keywords))
#
#             # 文本消息结束
#
#     elif isinstance(message, VoiceMessage):
#         reply_text = '语音信息我听不懂/:P-(/:P-(/:P-('
#     elif isinstance(message, ImageMessage):
#         reply_text = '图片信息我也看不懂/:P-(/:P-(/:P-('
#     elif isinstance(message, VideoMessage):
#         reply_text = '视频我不会看/:P-('
#     elif isinstance(message, LinkMessage):
#         reply_text = '链接信息'
#     elif isinstance(message, LocationMessage):
#         reply_text = '地理位置信息'
#     elif isinstance(message, EventMessage):  # 事件信息
#         if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
#             follow_event = KeyWordModel.objects.get(keyword='关注事件')
#             reply_text = follow_event.content
#
#             # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
#             if message.key and message.ticket:
#                 reply_text += '\n来源：扫描二维码关注'
#             else:
#                 reply_text += '\n来源：搜索名称关注'
#         elif message.type == 'unsubscribe':
#             reply_text = '取消关注事件'
#         elif message.type == 'scan':
#             reply_text = '已关注用户扫描二维码！'
#         elif message.type == 'location':
#             reply_text = '上报地理位置'
#         elif message.type == 'click':
#             reply_text = '自定义菜单点击'
#         elif message.type == 'view':
#             reply_text = '自定义菜单跳转链接'
#         elif message.type == 'templatesendjobfinish':
#             reply_text = '模板消息'
#
#     response = wechat_instance.response_text(content=reply_text)
#     return HttpResponse(response, content_type="application/xml")