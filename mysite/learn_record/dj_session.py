#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/19 23:17

# Django session

# Django完全支持也匿名会话，简单说就是使用跨网页之间可以进行通讯，比如显示用户名，用户是否已经发表评论。session框架让你存储和获取访问者的数据信息，这些信息保存在服务器上（默认是数据库中），以 cookies 的方式发送和获取一个包含 session ID的值，并不是用cookies传递数据本身。
# 启用session
# 编辑settings.py中的一些配置
# MIDDLEWARE_CLASSES 确保其中包含以下内容
# 'django.contrib.sessions.middleware.SessionMiddleware',
# INSTALLED_APPS 是包含
# 'django.contrib.sessions',
# 这些是默认启用的。如果你不用的话，也可以关掉这个以节省一点服务器的开销。
# 提示：您也可以配置使用比如 cache 来存储 session

# 在视图中使用 session
# request.session 可以在视图中任何地方使用，它类似于python中的字典
# session 默认有效时间为两周，可以在 settings.py 中修改默认值：参见这里
# 创建或修改 session：
# request.session[key] = value
# 获取 session：
# request.session.get(key,default=None)
# 删除 session
# del request.session[key] # 不存在时报错
# session 例子
# 比如写一个不让用户评论两次的应用：
# from django.http import HttpResponse

# def post_comment(request, new_comment):
#     if request.session.get('has_commented', False):
#         return HttpResponse("You've already commented.")
#     c = comments.Comment(comment=new_comment)
#     c.save()
#     request.session['has_commented'] = True
#     return HttpResponse('Thanks for your comment!')

# 一个简化的登陆认证：
# def login(request):
#     m = Member.objects.get(username=request.POST['username'])
#     if m.password == request.POST['password']:
#         request.session['member_id'] = m.id
#         return HttpResponse("You're logged in.")
#     else:
#         return HttpResponse("Your username and password didn't match.")
#
#
# def logout(request):
#     try:
#         del request.session['member_id']
#     except KeyError:
#         pass
#     return HttpResponse("You're logged out.")
# 当登陆时验证用户名和密码，并保存用户id在 session 中，这样就可以在视图中用 request.session['member_id']来检查用户是否登陆，当退出的时候，删除掉它。