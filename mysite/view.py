# -*- encoding: utf-8 -*-
'''
Created on 2017年2月27日

@author: houguangdong
'''

from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
import datetime
import MySQLdb
# from mysite.books.models import Book


def hello(request):
    return HttpResponse("Hello world")


def current_datetime(request):
    now = datetime.datetime.now()
    # 方式1
    # t = get_template('current_datetime.html')
    # html = t.render(Context({'current_date': now}))
    # return HttpResponse(html)
    # 方式2
    # render_to_response()的第一个参数必须是要使用的模板名称。 如果要给定第二个参数，那么该参数必须是为该模板创建Context时所使用的字典。 如果不提供第二个参数， render_to_response()使用一个空字典。
    return render_to_response('current_datetime.html', {'current_date': now})


# def current_datetime(request):
#     # 方式3 使用 locals() 时要注意是它将包括 所有 的局部变量，它们可能比你想让模板访问的要多。
#     current_date = datetime.datetime.now()
#     return render_to_response('current_datetime.html', locals())


# 把模板存放于模板目录的子目录中是件很轻松的事情。 只需在调用 get_template() 时，把子目录名和一条斜杠添加到模板名称之前，如：
# t = get_template('dateapp/current_datetime.html')
# 由于 render_to_response() 只是对 get_template() 的简单封装， 你可以对 render_to_response() 的第一个参数做相同处理。
# return render_to_response('dateapp/current_datetime.html', {'current_date': now})
# 对子目录树的深度没有限制，你想要多少层都可以。 只要你喜欢，用多少层的子目录都无所谓。

# include 模板标签
# 下面这两个例子都包含了 nav.html 模板。这两个例子是等价的，它们证明单/双引号都是允许的。
# {% include 'nav.html' %}
# {% include "nav.html" %}
# 下面的例子包含了 includes/nav.html 模板的内容:

# {% include 'includes/nav.html' %}
# 下面的例子包含了以变量 template_name 的值为名称的模板内容：
# {% include template_name %}

# mypage.html
# <html>
#     <body>
#     {% include "includes/nav.html" %}
#     <h1>{{ title }}</h1>
#     </body>
# </html>

# includes/nav.html
# <div id="nav">
#     You are in: {{ current_section }}
# </div>
# 如果你用一个包含 current_section的上下文去渲染 mypage.html这个模板文件，这个变量将存在于它所包含（include）的模板里，就像你想象的那样。
# 如果{% include %}标签指定的模板没找到，Django将会在下面两个处理方法中选择一个：
# 如果 DEBUG 设置为 True ，你将会在 Django 错误信息页面看到 TemplateDoesNotExist 异常。
# 如果 DEBUG 设置为 False ，该标签不会引发错误信息，在标签位置不显示任何东西。


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In % hour(s), it will be %s.</body></html>" % (offset, dt)
    # assert False
    return HttpResponse(html)

# python manage.py shell
# 输入下面这些命令来测试你的数据库配置：
# from django.db import connection
# cursor = connection.cursor()


def book_list_base(request):
    db = MySQLdb.connect(user='me', db='mydb', passwd='secret', host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT name FROM books ORDER BY name')
    names = [row[0] for row in cursor.fetchall()]
    db.close()
    return render_to_response('book_list.html', {'names': names})


# def book_list(request):
#     books = Book.objects.order_by('name')
#     return render_to_response('book_list.html', {'books': books})


# 从Request对象中获取数据
# URL相关信息 HttpRequest对象包含当前请求URL的一些信息：
# request.path    除域名以外的请求路径，以正斜杠开头    "/hello/"
# request.get_host()    主机名（比如，通常所说的域名）    "127.0.0.1:8000" or "www.example.com"
# request.get_full_path()    请求路径，可能包含查询字符串    "/hello/?print=true"
# request.is_secure()    如果通过HTTPS访问，则此方法返回True， 否则返回False    True 或者 False


# GOOD
def current_url_view_good(request):
    return HttpResponse("Welcome to the page at %s" % request.path)


# 有关request的其它信息
# request.META 是一个Python字典，包含了所有本次HTTP请求的Header信息，比如用户IP地址和用户Agent（通常是浏览器的名称和版本号）。
# HTTP_REFERRER，进站前链接网页，如果有的话。
# HTTP_USER_AGENT，用户浏览器的user-agent字符串，如果有的话。
# REMOTE_ADDR 客户端IP，如："12.345.67.89" 。


def ua_display_good1(request):
    try:
        ua = request.META['HTTP_USER_AGENT']
    except KeyError:
        ua = 'unknown'
    return HttpResponse("Your browser is %s" % ua)


def ua_display_good2(request):
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    return HttpResponse("Your browser is %s" % ua)


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def sell(item, price, quantity):
    print "Selling %s unit(s) of %s at %s" % (quantity, item, price)

# 为了使用关键字参数来调用它，你要指定参数名和值
# sell(item='Socks', price='$2.50', quantity=6)
# 最后，你可以混合关键字和位置参数，只要所有的位置参数列在关键字参数之前。
# 在 Python 正则表达式中，命名的正则表达式组的语法是 (?P<name>pattern) ，这里 name 是组的名字，而 pattern 是匹配的某个模式。
# 下面是一个使用无名组的 URLconf 的例子:
# 例如，如果不带命名组，请求 /articles/2006/03/ 将会等同于这样的函数调用：
# month_archive(request, '2006', '03')
# urlpatterns = patterns('',
#     (r'^articles/(\d{4})/$', views.year_archive),
#     (r'^articles/(\d{4})/(\d{2})/$', views.month_archive),
# )
#
# 下面是相同的 URLconf，使用命名组进行了重写:
# 而带命名组，同样的请求就会变成这样的函数调用：
# month_archive(request, year='2006', month='03')
# urlpatterns = patterns('',
#     (r'^articles/(?P<year>\d{4})/$', views.year_archive),
#     (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
# )
# 理解匹配/分组算法
# 需要注意的是如果在URLconf中使用命名组，那么命名组和非命名组是不能同时存在于同一个URLconf的模式中的。


def foobar_view(request, template_name):
    # m_list = MyModel.objects.filter(is_new=True)
    # return render_to_response(template_name, {'m_list': m_list})
    pass


def my_view(request, month, day):
    pass


def object_list(request, model):
    obj_list = model.objects.all()
    template_name = 'mysite/%s_list.html' % model.__name__.lower()
    return render_to_response(template_name, {'object_list': obj_list})


# 提供视图配置选项 # 传递额外的参数到视图函数中
# def my_view(request, template_name):
#     var = do_something()
#     return render_to_response(template_name, {'var': var})


# 了解捕捉值和额外参数之间的优先级 额外的选项
# 当冲突出现的时候，额外URLconf参数优先于捕捉值。 也就是说，如果URLconf捕捉到的一个命名组变量和一个额外URLconf参数包含的变量同名时，额外URLconf参数的值会被使用。
# (r'^mydata/(?P<id>\d+)/$', views.my_view, {'id': 3}),


# 使用缺省视图参数
# (r'^blog/$', views.page),
# (r'^blog/page(?P<num>\d+)/$', views.page),
def page(request, num='1'):
    pass


# 就像前面解释的一样，这种技术与配置选项的联用是很普遍的。 以下这个例子比提供视图配置选项一节中的例子有些许的改进。
# def my_view(request, template_name='mysite/my_view.html'):
#     var = do_something()
#     return render_to_response(template_name, {'var': var})


# 特殊情况下的视图
# 在这种情况下，象 /auth/user/add/ 的请求将会被 user_add_stage 视图处理。 尽管URL也匹配第二种模式，它会先匹配上面的模式。 （这是短路逻辑。）
# ('^auth/user/add/$', views.user_add_stage),
# ('^([^/]+)/([^/]+)/add/$', views.add_stage),

# 从URL中捕获文本
def day_archive(request, year, month, day):
    date = datetime.date(int(year), int(month), int(day))


# 视图函数的高级概念
# def method_splitter(request, GET=None, POST=None):
#     if request.method == 'GET' and GET is not None:
#         return GET(request)
#     elif request.method == 'POST' and POST is not None:
#         return POST(request)
#     raise Http404


def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404


def some_page_get(request):
    assert request.method == 'GET'
    do_something_for_get()
    print '1111'
    return render_to_response('page.html')


def some_page_post(request):
    assert request.method == 'POST'
    do_something_for_post()
    print '22222'
    return HttpResponseRedirect('/someurl/')

def do_something_for_get():
    print '333333'
    pass

def do_something_for_post():
    print '44444'
    pass


# 包装视图函数
# from django.conf.urls.defaults import *
# from mysite.views import requires_login, my_view1, my_view2, my_view3
# urlpatterns = patterns('',
#     (r'^view1/$', requires_login(my_view1)),
#     (r'^view2/$', requires_login(my_view2)),
#     (r'^view3/$', requires_login(my_view3)),
# )
def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request, *args, **kwargs)
    return new_view


# 包含其他URLconf
# from django.conf.urls.defaults import *
# urlpatterns = patterns('',
#     (r'^weblog/', include('mysite.blog.urls')),
#     (r'^photos/', include('mysite.photos.urls')),
#     (r'^about/$', 'mysite.views.about'),
# )
#
# from django.conf.urls.defaults import *
# urlpatterns = patterns('',
#     (r'^(\d\d\d\d)/$', 'mysite.blog.views.year_detail'),
#     (r'^(\d\d\d\d)/(\d\d)/$', 'mysite.blog.views.month_detail'),
# )
#
# 通过这两个URLconf，下面是一些处理请求的例子：
# /weblog/2007/ ：在第一个URLconf中，模式 r'^weblog/' 被匹配。 因为它是一个 include() ，Django将截掉所有匹配的文本，在这里是 'weblog/' 。URL剩余的部分是 2007/ ， 将在 mysite.blog.urls 这个URLconf的第一行中被匹配到。 URL仍存在的部分为 2007/ ,与第一行的 mysite.blog.urlsURL设置相匹配。
# /weblog//2007/(包含两个斜杠) 在第一个URLconf中,r’^weblog/’匹配 因为它有一个include(),django去掉了匹配的部,在这个例子中匹配的部分是’weblog/’ 剩下的部分是/2007/ (最前面有一个斜杠),不匹配mysite.blog.urls中的任何一行.
# /about/ : 这个匹配第一个URLconf中的 mysite.views.about 视图。


# 捕获的参数如何和include()协同工作
# 一个被包含的URLconf接收任何来自parent URLconfs的被捕获的参数，比如:
# # root urls.py
# from django.conf.urls.defaults import *
# urlpatterns = patterns('',
#     (r'^(?P<username>\w+)/blog/', include('foo.urls.blog')),
# )
#
# # foo/urls/blog.py
# from django.conf.urls.defaults import *
# urlpatterns = patterns('',
#     (r'^$', 'foo.views.blog_index'),
#     (r'^archive/$', 'foo.views.blog_archive'),
# )
# 在这个例子中，被捕获的 username 变量将传递给被包含的 URLconf，进而传递给那个URLconf中的 每一个 视图函数。
# 注意，这个被捕获的参数 总是 传递到被包含的URLconf中的 每一 行，不管那些行对应的视图是否需要这些参数。 因此，这个技术只有在你确实需要那个被传递的参数的时候才显得有用。


# 额外的URLconf如何和include()协同工作
# 相似的，你可以传递额外的URLconf选项到 include() , 就像你可以通过字典传递额外的URLconf选项到普通的视图。 当你这样做的时候，被包含URLconf的 每一 行都会收到那些额外的参数。
# 比如，下面的两个URLconf在功能上是相等的。
# 第一个：
# # urls.py
# from django.conf.urls.defaults import *
# urlpatterns = patterns('',
#     (r'^blog/', include('inner'), {'blogid': 3}),
# )
#
# # inner.py
# from django.conf.urls.defaults import *
# urlpatterns = patterns('',
#     (r'^archive/$', 'mysite.views.archive'),
#     (r'^about/$', 'mysite.views.about'),
#     (r'^rss/$', 'mysite.views.rss'),
# )
#
# 第二个
# # urls.py
# from django.conf.urls.defaults import *
# urlpatterns = patterns('',
#     (r'^blog/', include('inner')),
# )
#
# # inner.py
# from django.conf.urls.defaults import *
# urlpatterns = patterns('',
#     (r'^archive/$', 'mysite.views.archive', {'blogid': 3}),
#     (r'^about/$', 'mysite.views.about', {'blogid': 3}),
#     (r'^rss/$', 'mysite.views.rss', {'blogid': 3}),
# )


# 第十一章 通用视图
# from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template
# from mysite.books.views import about_pages
#
# urlpatterns = patterns('',
#     (r'^about/$', direct_to_template, {
#         'template': 'about.html'
#     }),
#     (r'^about/(\w+)/$', about_pages),
# )

# from django.http import Http404
# from django.template import TemplateDoesNotExist
# from django.views.generic.simple import direct_to_template
#
# def about_pages(request, page):
#     try:
#         return direct_to_template(request, template="about/%s.html" % page)
#     except TemplateDoesNotExist:
#         raise Http404()

# 要为所有的出版商创建一个列表页面，我们使用下面的URL配置：
# from django.conf.urls.defaults import *
# from django.views.generic import list_detail
# from mysite.books.models import Publisher
#
# publisher_info = {
#     'queryset': Publisher.objects.all(),
#     'template_name': 'publisher_list_page.html'，
#     'template_object_name': 'publisher',
# }
#
# urlpatterns = patterns('',
#     (r'^publishers/$', list_detail.object_list, publisher_info)
# )
# 在缺少template_name的情况下，object_list通用视图将自动使用一个对象名称。 在这个例子中，这个推导出的模板名称将是 "books/publisher_list.html" ，其中books部分是定义这个模型的app的名称， publisher部分是这个模型名称的小写。
# 这个模板将按照 context 中包含的变量 object_list 来渲染，这个变量包含所有的书籍对象。 一个非常简单的模板看起来象下面这样：
# {% extends "base.html" %}
# {% block content %}
#     <h2>Publishers</h2>
#     <ul>
#         {% for publisher in object_list %}
#             <li>{{ publisher.name }}</li>
#         {% endfor %}
#     </ul>
# {% endblock %}

# 扩展通用视图
# 制作友好的模板Context
# 添加额外的Context
# def get_books():
#     return Book.objects.all()
#
# publisher_info = {
#     'queryset': Publisher.objects.all(),
#     'template_object_name': 'publisher',
#     'extra_context': {'book_list': get_books}
# }

# 或者你可以使用另一个不是那么清晰但是很简短的方法，事实上 Publisher.objects.all 本身就是可以调用的：
# publisher_info = {
#     'queryset': Publisher.objects.all(),
#     'template_object_name': 'publisher',
#     'extra_context': {'book_list': Book.objects.all}
# }
# 注意 Book.objects.all 后面没有括号；这表示这是一个函数的引用，并没有真正调用它（通用视图将会在渲染时调用它）。

# 显示对象的子集
# book_info = {
#     'queryset': Book.objects.order_by('-publication_date'),
# }
# urlpatterns = patterns('',
#     (r'^publishers/$', list_detail.object_list, publisher_info),
#     (r'^books/$', list_detail.object_list, book_info),
# )

# apress_books = {
#     'queryset': Book.objects.filter(publisher__name='Apress Publishing'),
#     'template_name': 'books/apress_list.html'
# }
#
# urlpatterns = patterns('',
#     (r'^publishers/$', list_detail.object_list, publisher_info),
#     (r'^books/apress/$', list_detail.object_list, apress_books),
# )
# 注意 在使用一个过滤的 queryset 的同时，我们还使用了一个自定义的模板名称。 如果我们不这么做，通用视图就会用以前的模板，这可能不是我们想要的结果。

# 用函数包装来处理复杂的数据过滤
# urlpatterns = patterns('',
#     (r'^publishers/$', list_detail.object_list, publisher_info),
#     (r'^books/(\w+)/$', books_by_publisher),
# )
#
# from django.shortcuts import get_object_or_404
# from django.views.generic import list_detail
# from mysite.books.models import Book, Publisher
#
# def books_by_publisher(request, name):
#
#     # Look up the publisher (and raise a 404 if it can't be found).
#     publisher = get_object_or_404(Publisher, name__iexact=name)
#
#     # Use the object_list view for the heavy lifting.
#     return list_detail.object_list(
#         request,
#         queryset = Book.objects.filter(publisher=publisher),
#         template_name = 'books/books_by_publisher.html',
#         template_object_name = 'book',
#         extra_context = {'publisher': publisher}
#     )
# 注意在前面这个例子中我们在 extra_context中传递了当前出版商这个参数。

# 处理额外工作
# from mysite.books.views import author_detail
# urlpatterns = patterns('',
#     (r'^authors/(?P<author_id>\d+)/$', author_detail),
# )

# import datetime
# from django.shortcuts import get_object_or_404
# from django.views.generic import list_detail
# from mysite.books.models import Author
#
# def author_detail(request, author_id):
#     # Delegate to the generic view and get an HttpResponse.
#     response = list_detail.object_detail(
#         request,
#         queryset = Author.objects.all(),
#         object_id = author_id,
#     )
#
#     # Record the last accessed date. We do this *after* the call
#     # to object_detail(), not before it, so that this won't be called
#     # unless the Author actually exists. (If the author doesn't exist,
#     # object_detail() will raise Http404, and we won't reach this point.)
#     now = datetime.datetime.now()
#     Author.objects.filter(id=author_id).update(last_accessed=now)
#
#     return response
# 注意
# 除非你添加 last_accessed 字段到你的 Author 模型并创建 books/author_detail.html 模板，否则这段代码不能真正工作。

#
# 我们可以用同样的方法修改通用视图的返回值。 如果我们想要提供一个供下载用的 纯文本版本的author列表，我们可以用下面这个视图：
# def author_list_plaintext(request):
#     response = list_detail.object_list(
#         request,
#         queryset = Author.objects.all(),
#         mimetype = 'text/plain',
#         template_name = 'books/author_list.txt'
#     )
#     response["Content-Disposition"] = "attachment; filename=authors.txt"
#     return response
# 这个方法之所以工作是因为通用视图返回的 HttpResponse 对象可以象一个字典 一样的设置HTTP的头部。 随便说一下，这个 Content-Disposition 的含义是 告诉浏览器下载并保存这个页面，而不是在浏览器中显示它。




# 第十二章 部署Django
# (0) 准备你的代码库
# (1) 关闭Debug模式.
# (3) 来关闭模板Debug模式。 TEMPLATE_DEBUG = False
# (4) 实现一个404模板
# 这里有一个`` 404.html``的示例，你可以从它开始。 假定你使用的模板继承并定义一个 `` base.html``,该页面由titlecontent两块组成。
# {% extends "base.html" %}
# {% block title %}Page not found{% endblock %}
# {% block content %}
# <h1>Page not found</h1>
# <p>Sorry, but the requested page could not be found.</p>
# {% endblock %}
# 要测试你的404.html页面是否正常工作，仅仅需要将DEBUG 设置为`` False`` ，并且访问一个并不存在的URL。 （它将在`` sunserver`` 上工作的和开发服务器上一样好）
# (5) 实现一个500模板
# 这里有一个关于500.html的比较棘手的问题。你永远不能确定`` 为什么``会显示这个模板，所以它不应该做任何需要连接数据库，或者依赖任何可能被破坏的基础构件的事情。 （例如：它不应该使用自定义模板标签。）如果它用到了模板继承，那么父模板也就不应该依赖可能被破坏的基础构件。 因此，最好的方法就是避免模板继承，并且用一些非常简单的东西。 这是一个`` 500.html`` 的例子，可以把它作为一个起点：
# <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
#     "http://www.w3.org/TR/html4/strict.dtd">
# <html lang="en">
# <head>
#     <title>Page unavailable</title>
# </head>
# <body>
#     <h1>Page unavailable</h1>
#
#     <p>Sorry, but the requested page is unavailable due to a
#     server hiccup.</p>
#
#     <p>Our engineers have been notified, so check back later.</p>
# </body>
# </html>
# (6) 设置错误警告
# 默认情况下，Django在你的代码引发未处理的异常时，将会发送一封Email至开发者团队。但你需要去做两件事来设置这种行为。
# 首先，改变你的ADMINS设置用来引入你的E-mail地址，以及那些任何需要被注意的联系人的E-mail地址。 这个设置采用了类似于(姓名, Email)元组，像这样：
# ADMINS = (
#     ('John Lennon', 'jlennon@example.com'),
#     ('Paul McCartney', 'pmacca@example.com'),
# )
# 第二，确保你的服务器配置为发送电子邮件。 设置好postfix,sendmail或其他本书范围之外但是与Django设置相关的邮件服务器,你需要将将 EMAIL_HOST设置为你的邮件服务器的正确的主机名. 默认模式下是设置为’localhost’, 这个设置对大多数的共享主机系统环境适用. 取决于你的安排的复杂性,你可能还需要设置 EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,EMAIL_PORT或EMAIL_USE_TLS。
# 你还可以设置EMAIL_SUBJECT_PREFIX以控制Django使用的 error e-mail的前缀。 默认情况下它被设置为'[Django] '
# (7) 设置连接中断警报
# 如果你安装有CommonMiddleware(比如，你的MIDDLEWARE_CLASSES设置包含了’django.middleware.common.CommonMiddleware’的情况下，默认就安装了CommonMiddleware),你就具有了设置这个选项的能力：有人在访问你的Django网站的一个非空的链接而导致一个404错误的发生和连接中断的情况，你将收到一封邮件. 如果你想激活这个特性，设置SEND_BROKEN_LINK_EMAILS 为True(默认为False),并设置你的MANAGERS为某个人或某些人的邮件地址，这些邮件地址将会收到报告连接中断错误的邮件. MANAGERS使用和ADMINS 同样的语法.例如:
#
# MANAGERS = (
#     ('George Harrison', 'gharrison@example.com'),
#     ('Ringo Starr', 'ringo@example.com'),
# )
# 请注意，错误的Email会令人感到反感，对于任何人来说都是这样。
# (8) 使用针对产品的不同的设置
# 如果你想把你的配置文件按照产品设置和开发设置组织起来，你可以通过下面三种方法的其中一种达到这个目的。
# 8.1 设置成两个全面的，彼此独立的配置文件
# 8.2 设置一个基本的配置文件（比如，为了开发)和第二个（为了产品)配置文件，第二个配置文件仅仅从基本的那个配置文件导入配置，并对需要定义的进行复写.
# # settings.py
# DEBUG = True
# TEMPLATE_DEBUG = DEBUG
# DATABASE_ENGINE = 'postgresql_psycopg2'
# DATABASE_NAME = 'devdb'
# DATABASE_USER = ''
# DATABASE_PASSWORD = ''
# DATABASE_PORT = ''
#
# # ...
# # settings_production.py
# from settings import *
# DEBUG = TEMPLATE_DEBUG = False
# DATABASE_NAME = 'production'
# DATABASE_USER = 'app'
# DATABASE_PASSWORD = 'letmein'
# 8.3 使用一个单独的配置文件，此配置文件包含一个Python的逻辑判断根据上下文环境改变设置
# # settings.py
#
# import socket
# if socket.gethostname() == 'my-laptop':
#     DEBUG = TEMPLATE_DEBUG = True
# else:
#     DEBUG = TEMPLATE_DEBUG = False
#
# 重命名settings.py
# 随便将你的settings.py重命名为settings_dev.py或settings/dev.py或foobar.py，Django 并不在乎你的配置文件取什么名字，只要你告诉它你使用的哪个配置文件就可以了。
# 但是如果你真的重命名了由django-admin.py startproject 命令创建的settings.py文件，你会发现manage.py会给出一个错误信息说找不到配置文件。 那是由于它尝试从这个文件中导入一个叫做settings的模块，你可以通过修改manage.py 文件，将 import settings 语句改为导入你自己的模块，或者使用django-admin.py而不是使用manage.py,在后一种方式中你需要设置 DJANGO_SETTINGS_MODULE 环境变量为你的配置文件所在的python 路径.(比如’mysite.settings’）。
# DJANGO_SETTINGS_MODULE
# 通过这种方式的代码改变后，本章的下一部分将集中在对具体环境(比如Apache)的发布所需要的指令上。 这些指令针对每一种环境都不同，但是有一件事情是相同的。 在每一种环境中，你都需要告诉Web服务器你的DJANGO_SETTINGS_MODULE是什么,这是你的Django应用程序的进入点。 DJANGO_SETTINGS_MODULE指向你的配置文件，在你的配置文件中指向你的ROOT_URLCONF,在ROOT_URLCONF中指向了你的视图以及其他的部分。
# DJANGO_SETTINGS_MODULE是你的配置文件的python的路径 比如，假设mysite是在你的Python路径中，DJANGO_SETTINGS_MODULE对于我们正在进行的例子就是’mysite.settings’。
# (9)用Apache和mod_python来部署Django
# 目前，Apache和mod_python是在生产服务器上部署Django的最健壮搭配。
# mod_python (http://www.djangoproject.com/r/mod_python/)是一个在Apache中嵌入Python的Apache插件，它在服务器启动时将Python代码加载到内存中。 (译注：
# Django 需要Apaceh 2.x 和mod_python 3.x支持。
# 基本配置
# 为了配置基于 mod_python 的 Django，首先要安装有可用的 mod_python 模块的 Apache。 这通常意味着应该有一个 LoadModule 指令在 Apache 配置文件中。 它看起来就像是这样：
# LoadModule python_module /usr/lib/apache2/modules/mod_python.so
# Then, edit your Apache configuration file and add a <Location> directive that ties a specific URL path to a specific Django installation. 例如：
# <Location "/">
#     SetHandler python-program
#     PythonHandler django.core.handlers.modpython
#     SetEnv DJANGO_SETTINGS_MODULE mysite.settings
#     PythonDebug Off
# </Location>
# 要确保把 DJANGO_SETTINGS_MODULE 中的 mysite.settings 项目换成与你的站点相应的内容。
# 它告诉 Apache，任何在 / 这个路径之后的 URL 都使用 Django 的 mod_python 来处理。 它 将 DJANGO_SETTINGS_MODULE 的值传递过去，使得 mod_python 知道这时应该使用哪个配置。
# Apache 可能不但会运行在你正常登录的环境中，也会运行在其它不同的用户环境中；也可能会有不同的文件路径或 sys.path。 你需要告诉 mod_python 如何去寻找你的项目及 Django 的位置。
# PythonPath "['/path/to/project', '/path/to/django'] + sys.path"
# 你也可以加入一些其它指令，比如 PythonAutoReload Off 以提升性能。 查看 mod_python 文档获得详细的指令列表。
# 注意，你应该在成品服务器上设置 PythonDebug Off 。如果你使用 PythonDebug On 的话，在程序产生错误时，你的用户会看到难看的（并且是暴露的） Python 回溯信息。 如果你把 PythonDebug 置 On,当mod_python出现某些错误,你的用户会看到丑陋的（也会暴露某些信息)Python的对错误的追踪的信息。
# 重启 Apache 之后所有对你的站点的请求（或者是当你用了 <VirtualHost> 指令后则是虚拟主机）都会由 Djanog 来处理。
# 在同一个 Apache 的实例中运行多个 Django 程序
# 在同一个 Apache 实例中运行多个 Django 程序是完全可能的。 当你是一个独立的 Web 开发人员并有多个不同的客户时，你可能会想这么做。
# 只要像下面这样使用 VirtualHost 你可以实现：
# NameVirtualHost *
# <VirtualHost *>
#     ServerName www.example.com
#     # ...
#     SetEnv DJANGO_SETTINGS_MODULE mysite.settings
# </VirtualHost>
#
# <VirtualHost *>
#     ServerName www2.example.com
#     # ...
#     SetEnv DJANGO_SETTINGS_MODULE mysite.other_settings
# </VirtualHost>
# 如果你需要在同一个 VirtualHost 中运行两个 Django 程序，你需要特别留意一下以 确保 mod_python 的代码缓存不被弄得乱七八糟。 使用 PythonInterpreter 指令来将不 同的 <Location> 指令分别解释：
# <VirtualHost *>
#     ServerName www.example.com
#     # ...
#     <Location "/something">
#         SetEnv DJANGO_SETTINGS_MODULE mysite.settings
#         PythonInterpreter mysite
#     </Location>
#
#     <Location "/otherthing">
#         SetEnv DJANGO_SETTINGS_MODULE mysite.other_settings
#         PythonInterpreter mysite_other
#     </Location>
# </VirtualHost>
# 这个 PythonInterpreter 中的值不重要，只要它们在两个 Location 块中不同。
# 用 mod_python 运行一个开发服务器
# 因为 mod_python 缓存预载入了 Python 的代码，当在 mod_python 上发布 Django 站点时，你每 改动了一次代码都要需要重启 Apache 一次。 这还真是件麻烦事，所以这有个办法来避免它： 只要 加入 MaxRequestsPerChild 1 到配置文件中强制 Apache 在每个请求时都重新载入所有的 代码。 但是不要在产品服务器上使用这个指令，这会撤销 Django 的特权。
# 如果你是一个用分散的 print 语句（我们就是这样）来调试的程序员，注意这 print 语 句在 mod_python 中是无效的；它不会像你希望的那样产生一个 Apache 日志。 如果你需要在 mod_python 中打印调试信息，可能需要用到 Python 标准日志包（Pythons standard logging package）。 更多的信息请参见 http://docs.python.org/lib/module-logging.html 。另一个选择是在模板页面中加入调试信息。
# 使用相同的Apache实例来服务Django和Media文件
# Django本身不用来服务media文件；应该把这项工作留给你选择的网络服务器。 我们推荐使用一个单独的网络服务器（即没有运行Django的一个）来服务media。 想了解更多信息，看下面的章节。
# 不过，如果你没有其他选择，所以只能在同Django一样的Apache VirtualHost 上服务media文件，这里你可以针对这个站点的特定部分关闭mod_python：
# <Location "/media/">
#     SetHandler None
# </Location>
# 将 Location 改成你的media文件所处的根目录。
# 你也可以使用 <LocationMatch> 来匹配正则表达式。 比如，下面的写法将Django定义到网站的根目录，并且显式地将 media 子目录以及任何以 .jpg ， .gif ， 或者 .png 结尾的URL屏蔽掉:
# <Location "/">
#     SetHandler python-program
#     PythonHandler django.core.handlers.modpython
#     SetEnv DJANGO_SETTINGS_MODULE mysite.settings
# </Location>
# <Location "/media/">
#     SetHandler None
# </Location>
# <LocationMatch "\.(jpg|gif|png)$">
#     SetHandler None
# </LocationMatch>
# 在所有这些例子中，你必须设置 DocumentRoot ，这样apache才能知道你存放静态文件的位置。
# 错误处理
# 当你使用 Apache/mod_python 时，错误会被 Django 捕捉，它们不会传播到 Apache 那里，也不会出现在 Apache 的 错误日志 中。
# 除非你的 Django 设置的确出了问题。 在这种情况下，你会在浏览器上看到一个 内部服务器错误的页面，并在 Apache 的 错误日志 中看到 Python 的完整回溯信息。 错误日志 的回溯信息有多行。 当然，这些信息是难看且难以阅读的。
# 处理段错误
# 有时候，Apache会在你安装Django的时候发生段错误。 这时，基本上 总是 有以下两个与Django本身无关的原因其中之一所造成：
# 有可能是因为，你使用了 pyexpat 模块（进行XML解析）并且与Apache内置的版本相冲突。 详情请见 http://www.djangoproject.com/r/articles/expat-apache-crash/.
# 也有可能是在同一个Apache进程中，同时使用了mod_python 和 mod_php，而且都使用MySQL作为数据库后端。 在有些情况下，这会造成PHP和Python的MySQL模块的版本冲突。 在mod_python的FAQ中有更详细的解释。
# 如果还有安装mod_python的问题，有一个好的建议，就是先只运行mod_python站点，而不使用Django框架。 这是区分mod_python特定问题的好方法。 下面的这篇文章给出了更详细的解释。 http://www.djangoproject.com/r/articles/getting-modpython-working/.
# 下一个步骤应该是编辑一段测试代码，把你所有django相关代码import进去，你的views,models,URLconf,RSS配置，等等。 把这些imports放进你的handler函数中，然后从浏览器进入你的URL。 如果这些导致了crash，你就可以确定是import的django代码引起了问题。 逐个去掉这些imports，直到不再冲突，这样就能找到引起问题的那个模块。 深入了解各模块，看看它们的imports。 要想获得更多帮助，像linux的ldconfig，Mac OS的otool和windows的ListDLLs（form sysInternals）都可以帮你识别共享依赖和可能的版本冲突。
#
#
# 一种替代方案： mod_wsgi模块
# 作为一个mod_python模块的替代，你可以考虑使用mod_wsgi模块(http://code.google.com/p/modwsgi/),此模块开发的时间比mod_python的开发时间离现在更近一些，在Django社区已有一些使用。 一个完整的概述超出了本书的范围，你可以从官方的Django文档查看到更多的信息。
#
# 慢慢变大
# 下面的这些步骤都是上面最后一个的变体：
# 当你需要更好的数据库性能，你可能需要增加数据库的冗余服务器。 MySQL内置了备份功能；PostgreSQL应该看一下Slony (http://www.djangoproject.com/r/slony/) 和 pgpool (http://www.djangoproject.com/r/pgpool/) ，这两个分别是数据库备份和连接池的工具。
# 如果单个均衡器不能达到要求，你可以增加更多的均衡器，并且使用轮训（round-robin）DNS来实现分布访问。
# 如果单台媒体服务器不够用，你可以增加更多的媒体服务器，并通过集群来分布流量。
# 如果你需要更多的高速缓存（cache），你可以增加cache服务器。
# 在任何情况下，只要集群工作性能不好，你都可以往上增加服务器。
#
# 禁用 Keep-Alive
# Keep-Alive 是HTTP提供的功能之一，它的目的是允许多个HTTP请求复用一个TCP连接，也就是允许在同一个TCP连接上发起多个HTTP请求，这样有效的避免了每个HTTP请求都重新建立自己的TCP连接的开销。
# 这一眼看上去是好事，但它足以杀死Django站点的性能。 如果你从单独的媒体服务器上向用户提供服务，每个光顾你站点的用户都大约10秒钟左右发出一次请求。 这就使得HTTP服务器一直在等待下一次keep-alive 的请求，空闲的HTTP服务器和工作时消耗一样多的内存。
#
# 使用 memcached
# 尽管Django支持多种不同的cache后台机制，没有一种的性能可以 接近 memcached。 如果你有一个高流量的站点，不要犹豫，直接选择memcached。
#
# 经常使用memcached
# 当然，选择了memcached而不去使用它，你不会从中获得任何性能上的提升。 Chapter 15 is your best friend here: 学习如何使用Django的cache框架，并且尽可能地使用它。 大量的可抢占式的高速缓存通常是一个站点在大流量下正常工作的唯一瓶颈。