#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/23 15:56

# Django 中间件
# 提示：关于 Django 1.10 的变化在本文的最后面有详细的说明。
# 我们从浏览器发出一个请求 Request，得到一个响应后的内容 HttpResponse ，这个请求传递到 Django的过程如下：
# 也就是说，每一个请求都是先通过中间件中的 process_request 函数，这个函数返回 None 或者 HttpResponse 对象，如果返回前者，
# 继续处理其它中间件，如果返回一个 HttpResponse，就处理中止，返回到网页上。
# 中间件不用继承自任何类（可以继承 object ），下面一个中间件大概的样子：
class CommonMiddleware(object):

    def process_request(self, request):
        return None

    def process_response(self, request, response):
        return response

# 还有 process_view, process_exception 和 process_template_response 函数。
# 一，比如我们要做一个 拦截器，发现有恶意访问网站的人，就拦截他！
# 假如我们通过一种技术，比如统计一分钟访问页面数，太多就把他的 IP 加入到黑名单 BLOCKED_IPS（这部分没有提供代码，主要讲中间件部分）
# 项目 zqxt 文件名 zqxt/middleware.py
#
# class BlockedIpMiddleware(object):
#     def process_request(self, request):
#         if request.META['REMOTE_ADDR'] in getattr(settings, "BLOCKED_IPS", []):
#             return http.HttpResponseForbidden('<h1>Forbidden</h1>')


# 这里的代码的功能就是 获取当前访问者的 IP (request.META['REMOTE_ADDR'])，如果这个 IP 在黑名单中就拦截，如果不在就返回 None
# (函数中没有返回值其实就是默认为 None)，把这个中间件的 Python 路径写到settings.py中
# 1.1 Django 1.9 和以前的版本：
# MIDDLEWARE_CLASSES = (
#     'zqxt.middleware.BlockedIpMiddleware',
#     ...其它的中间件
# )
# 1.2 Django 1.10 版本 更名为 MIDDLEWARE（单复同形），写法也有变化，详见 第四部分。
# 如果用 Django 1.10版本开发，部署时用 Django 1.9版本或更低版本，要特别小心此处。
# MIDDLEWARE = (
#     'zqxt.middleware.BlockedIpMiddleware',
#     ...其它的中间件
# )
# Django 会从 MIDDLEWARE_CLASSES 或 MIDDLEWARE 中按照从上到下的顺序一个个执行中间件中的 process_request 函数，而其中 process_response 函数则是最前面的最后执行。

# 二，再比如，我们在网站放到服务器上正式运行后，DEBUG改为了 False，这样更安全，但是有时候发生错误我们不能看到错误详情，调试不方便，有没有办法处理好这两个事情呢？
# 普通访问者看到的是友好的报错信息
# 管理员看到的是错误详情，以便于修复 BUG
# 当然可以有，利用中间件就可以做到！代码如下：
import sys
from django.views.debug import technical_500_response
from django.conf import settings


class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())

# 把这个中间件像上面一样，加到你的 settings.py 中的 MIDDLEWARE_CLASSES 中，可以放到最后，这样可以看到其它中间件的 process_request的错误。
# 当访问者为管理员时，就给出错误详情，比如访问本站的不存在的页面：http://www.ziqiangxuetang.com/admin/
# 普通人看到的是普通的 404（自己点开看看），而我可以看到：

# 三，分享一个简单的识别手机的中间件，更详细的可以参考这个：django-mobi 或 django-mobile
MOBILE_USERAGENTS = ("2.0 MMP", "240x320", "400X240", "AvantGo", "BlackBerry",
                     "Blazer", "Cellphone", "Danger", "DoCoMo", "Elaine/3.0", "EudoraWeb",
                     "Googlebot-Mobile", "hiptop", "IEMobile", "KYOCERA/WX310K", "LG/U990",
                     "MIDP-2.", "MMEF20", "MOT-V", "NetFront", "Newt", "Nintendo Wii", "Nitro",
                     "Nokia", "Opera Mini", "Palm", "PlayStation Portable", "portalmmm", "Proxinet",
                     "ProxiNet", "SHARP-TQ-GX10", "SHG-i900", "Small", "SonyEricsson", "Symbian OS",
                     "SymbianOS", "TS21i-10", "UP.Browser", "UP.Link", "webOS", "Windows CE",
                     "WinWAP", "YahooSeeker/M1A1-R2D2", "iPhone", "iPod", "Android",
                     "BlackBerry9530", "LG-TU915 Obigo", "LGE VX", "webOS", "Nokia5800")


# class MobileTemplate(object):
#     """
#     If a mobile user agent is detected, inspect the default args for the view
#     func, and if a template name is found assume it is the template arg and
#     attempt to load a mobile template based on the original template name.
#     """
#
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         if any(ua for ua in MOBILE_USERAGENTS if ua in
#                 request.META["HTTP_USER_AGENT"]):
#             template = view_kwargs.get("template")
#             if template is None:
#                 for default in view_func.func_defaults:
#                     if str(default).endswith(".html"):
#                         template = default
#             if template is not None:
#                 template = template.rsplit(".html", 1)[0] + ".mobile.html"
#                 try:
#                     get_template(template)
#                 except TemplateDoesNotExist:
#                     pass
#                 else:
#                     view_kwargs["template"] = template
#                     return view_func(request, *view_args, **view_kwargs)
#         return None
# 参考文档：https://docs.djangoproject.com/en/1.8/topics/http/middleware/
#
# 四，补充：Django 1.10 接口发生变化，变得更加简洁
class SimpleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # 调用 view 之前的代码

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # 调用 view 之后的代码

        return response

# Django 1.10.x 也可以用函数来实现中间件，详见官方文档。
# 五，让 你写的中间件 兼容 Django新版本和旧版本
# try:
#     from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
# except ImportError:
#     MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x
#
#
# class SimpleMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         pass
#
#     def process_response(request, response):
#         pass

# 新版本中 django.utils.deprecation.MiddlewareMixin 的 源代码 如下：
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

# __call__ 方法会先调用 self.process_request(request)，接着执行 self.get_response(request) 然后调用 self.process_response(request, response)
# 旧版本(Django 1.4.x-Django 1.9.x) 的话，和原来一样。