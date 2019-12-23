#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/19 20:26

# Django 生成静态页面
# 如果网站的流量过大，每次访问时都动态生成，执行SQL语句，消耗大量服务器资源，这时候可以考虑生成静态页面。
# 生成静态很简单，下面是一个例子:
# 只要在views.py中这样写就行了

# from django.shortcuts import render
# from django.template.loader import render_to_string
# import os
#
#
# def my_view(request):
#     context = {'some_key': 'some_value'}
#
#     static_html = '/path/to/static.html'
#
#     if not os.path.exists(static_html):
#         content = render_to_string('template.html', context)
#         with open(static_html, 'w') as static_file:
#             static_file.write(content)
#
#     return render(request, static_html)

# 上面的例子中，当用户访问时，如果判断没有静态页面就自动生成静态页面，然后返回静态文件，当文件存在的时候就不再次生成。
# 也可以用一个文件夹，比如在project下建一个 static_html 文件夹，把生成的静态文件都放里面，让用户像访问静态文件那样访问页面。
# 更佳办法
# 但是一般情况下都不需要生成静态页面，因为Django 有缓存功能，使用 Django Cache(缓存) 就相当于生成静态页面，而且还有自动更新的功能，比如30分钟刷新一下页面内容。
# 用Django管理静态网站内容
# 如果服务器上不支持Django环境，你可以在本地上搭建一个Django环境，然后生成静态页面，把这些页面放到不支持 Django 的服务器上去，在本地更新，然后上传到服务器，用Django来管理和更新网站的内容，也是一个不错的做法，还可以更安全，听说有很多黑客都是这么做的。


# Django表单用在模板中的时候我们会加一句 {% csrf_token %}