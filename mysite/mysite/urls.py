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
from views import hello, current_datetime, hours_ahead
from views import foobar_view, my_view
from views import method_splitter, some_page_get, some_page_post
from books import views
from contact import views as c_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^hello/$', hello),
    url('^time/$', current_datetime),
    url('^time/plus/(\d{1,2})/$', hours_ahead),
    # url(r'^hello/$', 'views.hello'),
    # url(r'^time/$', 'views.current_datetime'),
    # url(r'^time/plus/(d{1,2})/$', 'views.hours_ahead'),
    # url(r'^search-form/$', views.search_form),
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

