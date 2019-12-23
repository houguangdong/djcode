#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/19 19:55

# Python/Django 生成二维码
# 一，包的安装和简单使用
# 1.1 用Python来生成二维码很简单，可以看 qrcode 这个包：
# pip install qrcode
# qrcode 依赖 Image 这个包：
# pip install Image
# 如果这个包安装有困难，可选纯Python的包来实现此功能，见下文。
# 1.2 安装后就可以使用了，这个程序带了一个 qr 命令：
# qr 'http://www.ziqiangxuetang.com' > test.png
# 1.3 下面我们看一下如何在 代码 中使用
import qrcode
img = qrcode.make('http://www.tuweizhong.com')
# img <qrcode.image.pil.PilImage object at 0x1044ed9d0>

with open('test.png', 'wb') as f:
    img.save(f)
# 这样就可以生成一个带有网址的二维码，但是这样得把文件保存到硬盘中。

# 【备注】：纯Python的包的使用：
# 安装：
# pip install git+git://github.com/ojii/pymaging.git#egg=pymaging
# pip install git+git://github.com/ojii/pymaging-png.git#egg=pymaging-png

# 使用方法大致相同，命令行上：
# qr --factory=pymaging "Some text" > test.png

# Python中调用：
from qrcode.image.pure import PymagingImage
img = qrcode.make('Some data here', image_factory=PymagingImage)

# 二，Django 中使用
# 我们可以用 Django 直接把生成的内容返回到网页，以下是操作过程：
# 2.1 新建一个 zqxtqrcode 项目，tools 应用：
# django-admin.py startproject zqxtqrcode
# python manage.py startapp tools
# 2.2 将 tools 应用 添加到 项目 settings.py 中
# INSTALLED_APPS = (
#     'tools',
# )

# 2.3 我们修改 tools/views.py
from django.http import HttpResponse
import qrcode
from django.utils.six import BytesIO


def generate_qrcode(request, data):
    img = qrcode.make(data)

    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()

    response = HttpResponse(image_stream, content_type="image/png")
    return response

# 2.4 添加视图函数到 zqxtqrcode/urls.py
# url(r'^qrcode/(.+)$', 'tools.views.generate_qrcode', name='qrcode'),

# 2.5 同步数据库，打开开发服务器：
# python manage.py syncdb
# python manage.py runserver

# 打开：http://127.0.0.1:8000/qrcode/http://www.tuweizhong.com 就可以看到如下效果：
# 这样生成 二维码的接口就写好了 ^_^，实例采用的是返回图片流的方式，这样不用写文件到硬盘，接口调用更方便，如果要加速，可以用Django缓存来实现。
# 源代码下载：
# 基于 Django 1.8，tools app 可以在 Django 1.4-Django1.8之间使用，更低版本的自测，应该也没什么问题，建议按教程步骤来一遍，这样学的更好。Django 1.8 以上版本按照教程来也可以使用。