#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/21 15:23
# Django Sitemap 站点地图
# Django 中自带了 sitemap框架，用来生成 xml 文件
# Django sitemap 演示：http://www.ziqiangxuetang.com/sitemap.xml
# sitemap 很重要，可以用来通知搜索引擎页面的地址，页面的重要性，帮助站点得到比较好的收录。
# 开启sitemap功能的步骤
# settings.py 文件中 django.contrib.sitemaps 和 django.contrib.sites 要在 INSTALL_APPS 中
# INSTALLED_APPS = (
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.sites',
#     'django.contrib.sitemaps',
#     'django.contrib.redirects',
#
#     #####
#     # othther apps
#     #####
# )
# Django 1.7 及以前版本：
# TEMPLATE_LOADERS 中要加入 'django.template.loaders.app_directories.Loader'，像这样：
# TEMPLATE_LOADERS ＝ (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )
# Django 1.8 及以上版本新加入了 TEMPLATES 设置，其中 APP_DIRS 要为 True，比如：
# NOTICE: code for Django 1.8, not work on Django 1.7 and below
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [
#             os.path.join(BASE_DIR,'templates').replace('\\', '/'),
#         ],
#         'APP_DIRS': True,
#     },
# ]
# 然后在 urls.py 中如下配置：
# from django.conf.urls import url
# from django.contrib.sitemaps import GenericSitemap
# from django.contrib.sitemaps.views import sitemap
#
# from blog.models import Entry
#
# sitemaps = {
#     'blog': GenericSitemap({'queryset': Entry.objects.all(), 'date_field': 'pub_date'}, priority=0.6),
#     # 如果还要加其它的可以模仿上面的
# }
#
# urlpatterns = [
#     # some generic view using info_dict
#     # ...
#
#     # the sitemap
#     url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
#         name='django.contrib.sitemaps.views.sitemap'),
# ]
# 但是这样生成的 sitemap，如果网站内容太多就很慢，很耗费资源，可以采用分页的功能：
# from django.conf.urls import url
# from django.contrib.sitemaps import GenericSitemap
# from django.contrib.sitemaps.views import sitemap
#
# from blog.models import Entry
#
# from django.contrib.sitemaps import views as sitemaps_views
# from django.views.decorators.cache import cache_page
#
# sitemaps = {
#     'blog': GenericSitemap({'queryset': Entry.objects.all(), 'date_field': 'pub_date'}, priority=0.6),
#     # 如果还要加其它的可以模仿上面的
# }
#
# urlpatterns = [
#     url(r'^sitemap\.xml$',
#         cache_page(86400)(sitemaps_views.index),
#         {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
#     url(r'^sitemap-(?P<section>.+)\.xml$',
#         cache_page(86400)(sitemaps_views.sitemap),
#         {'sitemaps': sitemaps}, name='sitemaps'),
# ]
# 这样就可以看到类似如下的 sitemap，如果本地测试访问 http://localhost:8000/sitemap.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml</loc></sitemap>
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml?p=2</loc></sitemap>
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml?p=3</loc></sitemap>
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml?p=4</loc></sitemap>
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml?p=5</loc></sitemap>
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml?p=6</loc></sitemap>
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml?p=7</loc></sitemap>
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml?p=8</loc></sitemap>
# <sitemap><loc>http://www.ziqiangxuetang.com/sitemap-tutorials.xml?p=9</loc></sitemap>
# </sitemapindex>
# 查看了下分页是实现了，但是全部显示成了 ?p=页面数，而且在百度站长平台上测试，发现这样的sitemap百度报错，于是看了下 Django的源代码：
# 在这里 https://github.com/django/django/blob/1.7.7/django/contrib/sitemaps/views.py
# 于是对源代码作了修改，变成了本站的sitemap的样子，比 ?p=2 这样更优雅
# 引入 下面这个 比如是 sitemap_views.py
# import warnings
# from functools import wraps
#
# from django.contrib.sites.models import get_current_site
# from django.core import urlresolvers
# from django.core.paginator import EmptyPage, PageNotAnInteger
# from django.http import Http404
# from django.template.response import TemplateResponse
# from django.utils import six
#
#
# def x_robots_tag(func):
#     @wraps(func)
#     def inner(request, *args, **kwargs):
#         response = func(request, *args, **kwargs)
#         response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
#         return response
#
#     return inner
#
#
# @x_robots_tag
# def index(request, sitemaps,
#           template_name='sitemap_index.xml', content_type='application/xml',
#           sitemap_url_name='django.contrib.sitemaps.views.sitemap',
#           mimetype=None):
#     if mimetype:
#         warnings.warn("The mimetype keyword argument is deprecated, use "
#                       "content_type instead", DeprecationWarning, stacklevel=2)
#         content_type = mimetype
#
#     req_protocol = 'https' if request.is_secure() else 'http'
#     req_site = get_current_site(request)
#
#     sites = []
#     for section, site in sitemaps.items():
#         if callable(site):
#             site = site()
#         protocol = req_protocol if site.protocol is None else site.protocol
#         for page in range(1, site.paginator.num_pages + 1):
#             sitemap_url = urlresolvers.reverse(
#                 sitemap_url_name, kwargs={'section': section, 'page': page})
#             absolute_url = '%s://%s%s' % (protocol, req_site.domain, sitemap_url)
#             sites.append(absolute_url)
#
#     return TemplateResponse(request, template_name, {'sitemaps': sites},
#                             content_type=content_type)
#
#
# @x_robots_tag
# def sitemap(request, sitemaps, section=None, page=1,
#             template_name='sitemap.xml', content_type='application/xml',
#             mimetype=None):
#     if mimetype:
#         warnings.warn("The mimetype keyword argument is deprecated, use "
#                       "content_type instead", DeprecationWarning, stacklevel=2)
#         content_type = mimetype
#
#     req_protocol = 'https' if request.is_secure() else 'http'
#     req_site = get_current_site(request)
#
#     if section is not None:
#         if section not in sitemaps:
#             raise Http404("No sitemap available for section: %r" % section)
#         maps = [sitemaps[section]]
#     else:
#         maps = list(six.itervalues(sitemaps))
#
#     urls = []
#     for site in maps:
#         try:
#             if callable(site):
#                 site = site()
#             urls.extend(site.get_urls(page=page, site=req_site,
#                                       protocol=req_protocol))
#         except EmptyPage:
#             raise Http404("Page %s empty" % page)
#         except PageNotAnInteger:
#             raise Http404("No page '%s'" % page)
#     return TemplateResponse(request, template_name, {'urlset': urls},
#                             content_type=content_type)
# 如果还是不懂，可以下载附件查看：zqxt_sitemap.zip