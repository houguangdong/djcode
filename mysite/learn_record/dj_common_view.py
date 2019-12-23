#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/21 20:39

# Django 通用视图
# 我们用Django开发，比如做一个博客，我们需要做一个文章列表，文章详情页，这种需求是比较普遍的，所以Django中提供了Class-Based Views。
# 有时候我们想直接渲染一个模板，不得不写一个视图函数
#
# def render_template_view(request):
#     return render(request, '/path/to/template.html')
#
# 其实可以用 TemplateView 可以直接写在 urls.py 中，不需要定义一个这样的函数。
# 这样的例子还有很多，下面一一介绍：
# 在urls.py中使用类视图的时候都是调用它的 .as_view() 函数
#
# 一，Base Views
# 1. django.views.generic.base.View
# 这个类是通用类的基类，其它类都是继承自这个类，一般不会用到这个类，个人感觉用函数更简单些。
# views.py
# from django.http import HttpResponse
# from django.views.generic import View
#
#
# class MyView(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('Hello, World!')
#
#
# # urls.py
# from django.conf.urls import patterns, url
#
# from myapp.views import MyView
#
# urlpatterns = patterns('',
#                        url(r'^mine/$', MyView.as_view(), name='my-view'),
#                        )
#
# 2. django.views.generic.base.TemplateView
# 在 get_context_data() 函数中，可以传一些 额外内容 到 模板
# views.py
#
# from django.views.generic.base import TemplateView
#
# from articles.models import Article
#
#
# class HomePageView(TemplateView):
#     template_name = "home.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(HomePageView, self).get_context_data(**kwargs)
#         context['latest_articles'] = Article.objects.all()[:5]
#         return context
#
#
# # urls.py
#
# from django.conf.urls import patterns, url
#
# from myapp.views import HomePageView
#
# urlpatterns = patterns('',
#                        url(r'^$', HomePageView.as_view(), name='home'),
#                        )
#
# 3. django.views.generic.base.RedirectView
# 用来进行跳转, 默认是永久重定向（301），可以直接在urls.py中使用，非常方便：
# from django.conf.urls import patterns, url
# from django.views.generic.base import RedirectView
#
# urlpatterns = patterns('',
#                        url(r'^go-to-django/$', RedirectView.as_view(url='http://djangoproject.com'),
#                            name='go-to-django'),
#                        url(r'^go-to-ziqiangxuetang/$',
#                            RedirectView.as_view(url='http://www.ziqiangxuetang.com', permant=False), name='go-to-zqxt'),
#                        )
# 其它的使用方式：(new in Django1.6)
# views.py
# from django.shortcuts import get_object_or_404
# from django.views.generic.base import RedirectView
#
# from articles.models import Article
#
#
# class ArticleCounterRedirectView(RedirectView):
#     url = ' # 要跳转的网址，
#     # url 可以不给，用 pattern_name 和 get_redirect_url() 函数 来解析到要跳转的网址
#
#     permanent = False  # 是否为永久重定向, 默认为 True
#     query_string = True  # 是否传递GET的参数到跳转网址，True时会传递，默认为 False
#     pattern_name = 'article-detail'  # 用来跳转的 URL, 看下面的 get_redirect_url() 函数
#
#     # 如果url没有设定，此函数就会尝试用pattern_name和从网址中捕捉的参数来获取对应网址
#     # 即 reverse(pattern_name, args) 得到相应的网址，
#     # 在这个例子中是一个文章的点击数链接，点击后文章浏览次数加1，再跳转到真正的文章页面
#     def get_redirect_url(self, *args, **kwargs):
#         # If url is not set, get_redirect_url() tries to reverse the pattern_name using what was captured in the URL(both
#         # named and unnamed groups are used).
#         article = get_object_or_404(Article, pk=kwargs['pk'])
#         article.update_counter()  # 更新文章点击数，在models.py中实现
#         return super(ArticleCounterRedirectView, self).get_redirect_url(*args, **kwargs)
#
#     # urls.py
#     from django.conf.urls import patterns, url
#     from django.views.generic.base import RedirectView
#
#     from article.views import ArticleCounterRedirectView, ArticleDetail
#
#     urlpatterns = patterns('',
#     url(r'^counter/(?P<pk>\d+)/$', ArticleCounterRedirectView.as_view(), name='article-counter'),
#     url(r'^details/(?P<pk>\d+)/$', ArticleDetail.as_view(), name='article-detail'),
# )

# 二，Generic Display View （通用显示视图）
# 1. django.views.generic.detail.DetailView
# DetailView 有以下方法：
# dispatch()
# http_method_not_allowed()
# get_template_names()
# get_slug_field()
# get_queryset()
# get_object()
# get_context_object_name()
# get_context_data()
# get()
# render_to_response()

# views.py
# from django.views.generic.detail import DetailView
# from django.utils import timezone
#
# from articles.models import Article
#
#
# class ArticleDetailView(DetailView):
#     model = Article  # 要显示详情内容的类
#
#     template_name = 'article_detail.html'
#
#     # 模板名称，默认为 应用名/类名_detail.html（即 app/modelname_detail.html）
#
#     # 在 get_context_data() 函数中可以用于传递一些额外的内容到网页
#     def get_context_data(self, **kwargs):
#         context = super(ArticleDetailView, self).get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context
#
#
# # urls.py
# from django.conf.urls import url
#
# from article.views import ArticleDetailView
#
# urlpatterns = [
#     url(r'^(?P<slug>[-_\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
# ]

# article_detail.html
# < h1 > 标题：{{object.title}} < / h1 >
# < p > 内容：{{object.content}} < / p >
# < p > 发表人: {{object.reporter}} < / p >
# < p > 发表于: {{object.pub_date | date}} < / p >
#
# < p > 日期: {{now | date}} < / p >

# 2. django.views.generic.list.ListView
# ListView 有以下方法：
# dispatch()
# http_method_not_allowed()
# get_template_names()
# get_queryset()
# get_context_object_name()
# get_context_data()
# get()
# render_to_response()

# views.py
# from django.views.generic.list import ListView
# from django.utils import timezone
#
# from articles.models import Article
#
#
# class ArticleListView(ListView):
#     model = Article
#
#     def get_context_data(self, **kwargs):
#         context = super(ArticleListView, self).get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context
#
#
# # urls.py:
#
# from django.conf.urls import url
#
# from article.views import ArticleListView
#
# urlpatterns = [
#     url(r'^$', ArticleListView.as_view(), name='article-list'),
# ]
#
# article_list.html
# <h1>文章列表</h1>
# <ul>
# {% for article in object_list %}
#     <li>{{ article.pub_date|date }} - {{ article.headline }}</li>
# {% empty %}
#     <li>抱歉，目前还没有文章。</li>
# {% endfor %}
# </ul>