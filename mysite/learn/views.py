# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from blog.models import Article


class MyView(View):

    def get(self, request, *args, **kwargs):
        print('11111111111111')
        return HttpResponse('Hello, World!')


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context


class ArticleCounterRedirectView(RedirectView):

    url = ''    # 要跳转的网址 url 可以不给，用 pattern_name 和 get_redirect_url() 函数 来解析到要跳转的网址

    permanent = False   # 是否为永久重定向, 默认为 True
    query_string = True     # 是否传递GET的参数到跳转网址，True时会传递，默认为 False
    pattern_name = 'article-detail'     # 用来跳转的 URL, 看下面的 get_redirect_url() 函数

    # 如果url没有设定，此函数就会尝试用pattern_name和从网址中捕捉的参数来获取对应网址
    # 即 reverse(pattern_name, args) 得到相应的网址，
    # 在这个例子中是一个文章的点击数链接，点击后文章浏览次数加1，再跳转到真正的文章页面
    def get_redirect_url(self, *args, **kwargs):
        # if url is not set, get_redirect_url() tries to reverse the pattern_name using what was captured in the URL (both named and unnamed groups are used).
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.update_counter()    # 更新文章点击数，在models.py中实现
        return super(ArticleCounterRedirectView, self).get_redirect_url(*args, **kwargs)


# Create your views here.
def index(request):
    return HttpResponse(u"欢迎光临 自强学堂!")

# 注意：如果是在另一台电脑上访问要用
#     python manage.py ip:port的形式，比如监听所有ip:
#     python manage.py runserver 0.0.0.0:8000
#     监听机器上所有ip 8000端口，访问时用电脑的ip代替127.0.0.1
# Django中的urls.py 用的是正则进行匹配的，如果不熟悉，您可以学习正则表达式以及Python正则表达式。


# 定义视图函数相关的URL(网址)  （即规定访问什么网址对应什么内容）
# 我们打开mysite / mysite / urls.py这个文件, 修改其中的代码:
# 由于Django版本对urls.py进行了一些更改：
# Django1.7.x及以下的同学可能看到的是这样的：
# from django.conf.urls import patterns, include, url
#
# from django.contrib import admin
#
# admin.autodiscover()
#
# urlpatterns = patterns('',
#     url(r'^$', 'learn.views.index'),  # new
#     # url(r'^blog/', include('blog.urls')),
#     url(r'^admin/', include(admin.site.urls)),
# )


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))

BASE_DIR = settings.BASE_DIR        # 项目目录
# 假设图片放在static/pics/里面
PICS = os.listdir(os.path.join(BASE_DIR, 'static/pics'))
print PICS  # 启动时终端上可以看到有哪些图片，我只放了一张，测试完后这一行可以删除


def get_pic(requet):
    color = requet.GET.get('color')
    number = requet.GET.get('number')
    name = '{}_{}'.format(color, number)
    # 过滤出符合要求的图片，假设是以输入的开头的都返回
    result_list = filter(lambda x: x.startswith(name), PICS)
    print 'result_list', result_list
    return HttpResponse(
        json.dumps(result_list), content_type='application/json'
    )


def index1(request):
    return render(request, 'home.html')     # render 是渲染模板，不懂先照着打就好。


def home(request):
    string = u"我在自强学堂学习Django，用它来建网站"
    return render(request, 'home.html', {'string': string})


def home1(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    return render(request, 'home.html', {'TutorialList': TutorialList})


def home2(request):
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    return render(request, 'home.html', {'info_dict': info_dict})


def home3(request):
    List = map(str, range(100))# 一个长度为100的 List
    return render(request, 'home.html', {'List': List})




