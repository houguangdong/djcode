# -*- encoding: utf-8 -*-
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from view import hello, current_datetime, hours_ahead
from view import foobar_view, my_view
from view import method_splitter, some_page_get, some_page_post
from books import views
from contact import views as c_views
from learn import views as learn_views
from blog import views as b_views
from learn.views import MyView
from learn.views import HomePageView
from django.views.generic.base import RedirectView
from learn.views import ArticleCounterRedirectView


urlpatterns = [
    url(r'^index$', learn_views.index),
    url(r'^index1$', learn_views.index1),
    url(r'^home/$', learn_views.home),
    url(r'^add1/$', b_views.index, name='home'),                    # 注意修改了这一行
    url(r'^add/$', learn_views.add, name='add'),                    # 注意修改了这一行
    url(r'^add/(\d+)/(\d+)/$', learn_views.add2, name='add2'),      # 注意修改了这一行
    url(r'^admin/', admin.site.urls),
    url('^hello/$', hello),
    url('^time/$', current_datetime),
    url('^time/plus/(\d{1,2})/$', hours_ahead),
    url(r'^hello/$', views.hello),
    url(r'^time/$', views.current_datetime),
    url(r'^time/plus/(d{1,2})/$', views.hours_ahead),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),
    url(r'^contact/$', c_views.contact),
    url(r'^contact_new/$', c_views.contact_new),
    # url(r'^foo/$', foobar_view, {'template_name': 'template1.html'}),
    # url(r'^bar/$', foobar_view, {'template_name': 'template2.html'}),
    # url(r'^mydata/birthday/$', my_view, {'month': 'jan', 'day': '06'}),
    # url(r'^mydata/(?P<month>\w{3})/(?P<day>\d\d)/$', my_view),
    # url(r'^events/$', views.object_list, {'model': models.Event}),
    # url(r'^blog/entries/$', views.object_list, {'model': models.BlogEntry}),
    # url(r'^articles/(\d{4})/(\d{2})/(\d{2})/$', views.day_archive),
    url(r'^somepage/$', method_splitter, {'GET': some_page_get, 'POST': some_page_post}),
    url(r'^get_pic/$', learn_views.get_pic, name='get-pic'),
    url(r'^mine/$', MyView.as_view(), name='my-view'),
    url(r'^page_view/$', HomePageView.as_view(), name='page_view'),
    url(r'^go-to-django/$', RedirectView.as_view(url='http://djangoproject.com'), name='go-to-django'),
    url(r'^go-to-ziqiangxuetang/$', RedirectView.as_view(url='http://www.ziqiangxuetang.com', permant=False), name='go-to-zqxt'),
    url(r'^counter/(?P<pk>\d+)/$', ArticleCounterRedirectView.as_view(), name='article-counter'),
]


# 低版本的urlpatterns的用法
# from django.conf.urls.defaults import *
# urlpatterns = patterns('mysite.views',
#     (r'^hello/$', 'hello'),
#     (r'^time/$', 'current_datetime'),
#     (r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
# )
#
# urlpatterns += patterns('weblog.views',
#     (r'^tag/(\w+)/$', 'tag'),
# )

# if settings.DEBUG:
#     urlpatterns += patterns('',
#         (r'^debuginfo/$', views.debug),
#     )

