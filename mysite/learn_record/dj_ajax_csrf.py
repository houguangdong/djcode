#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/21 15:17

# Django Ajax CSRF 认证
# CSRF（Cross-site request forgery跨站请求伪造，也被称为“one click attack”或者session riding，通常缩写为CSRF或者XSRF。是一种对网站的恶意利用。
#
# XSS
# 假如A网站有XSS漏洞，访问A网站的攻击用户 用发帖的方式，在标题或内容等地方植入js代码，这些代码在某些场景下会被触发执行（比如点回帖时）。
# 当A网站的其它用户点回帖后，js运行了，这段js按道理可以做任何事，比如将用户的cookie发到指定服务器（攻击者所有），这样攻击者就可以使用cookie假冒用户访问A网站了，可以发贴，删帖等。
#
# CSRF
# 背景知识：浏览器在发送请求的时候，会自动带上当前域名对应的cookie内容，发送给服务端，不管这个请求是来源A网站还是其它网站，只要请求的是A网站的链接，就会带上A网站的cookie。浏览器的同源策略并不能阻止CSRF攻击，因为浏览器不会停止js发送请求到服务端，只是在必要的时候拦截了响应的内容。或者说浏览器收到响应之前它不知道该不该拒绝。
# 攻击过程：用户登陆A网站后，攻击者自己开发一个B网站，这个网站会通过js请求A网站，比如用户点击了某个按钮，就触发了js的执行。
# 预防：
# Double Submit Cookie
# 攻击者是利用cookie随着http请求发送的特性来攻击。但攻击都不知道 cookie里面是什么。
# Django中是在表单中加一个隐藏的 csrfmiddlewaretoken，在提交表单的时候，会有 cookie 中的内容做比对，一致则认为正常，不一致则认为是攻击。由于每个用户的 token 不一样，B网站上的js代码无法猜出token内容，对比必然失败，所以可以起到防范作用。
#
# Synchronizer Token
# 和上面的类似，但不使用 cookie，服务端的数据库中保存一个 session_csrftoken，表单提交后，将表单中的 token 和 session 中的对比，如果不一致则是攻击。
# 这个方法实施起来并不困难，但它更安全一些，因为网站即使有 xss 攻击，也不会有泄露token的问题。
#
# Django 中自带了 防止CSRF攻击的功能，但是一些新手不知道如何使用，给自己编程带来了麻烦。常常会出现下面django csrf token missing or incorrect的错误。
#
# GET 请求不需要 CSRF 认证，POST 请求需要正确认证才能得到正确的返回结果。一般在POST表单中加入 {% csrf_token %}
# <form method="POST" action="/post-url/">
# {% csrf_token %}
# <input name='zqxt' value="自强学堂学习Django技术">
# </form>

# 如果使用Ajax调用的时候，就要麻烦一些。需要注意以下几点：
# 在视图中使用 render （而不要使用 render_to_response）
# 使用 jQuery 的 ajax 或者 post 之前 加入这个 js 代码：http://www.ziqiangxuetang.com/media/django/csrf.js
# jQuery(document).ajaxSend(function(event, xhr, settings) {
#     function getCookie(name) {
#         var cookieValue = null;
#         if (document.cookie && document.cookie != '') {
#             var cookies = document.cookie.split(';');
#             for (var i = 0; i < cookies.length; i++) {
#                 var cookie = jQuery.trim(cookies[i]);
#                 // Does this cookie string begin with the name we want?
#                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
#                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
#                     break;
#                 }
#             }
#         }
#         return cookieValue;
#     }
#     function sameOrigin(url) {
#         // url could be relative or scheme relative or absolute
#         var host = document.location.host; // host + port
#         var protocol = document.location.protocol;
#         var sr_origin = '//' + host;
#         var origin = protocol + sr_origin;
#         // Allow absolute or scheme relative URLs to same origin
#         return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
#             (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
#             // or any other URL that isn't scheme relative or absolute i.e relative.
#             !(/^(\/\/|http:|https:).*/.test(url));
#     }
#     function safeMethod(method) {
#         return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
#     }
#     if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
#         xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
#     }
# });
#
# 或者 更为优雅简洁的代码（不能写在 .js 中，要直接写在模板文件中）：
# $.ajaxSetup({
#     data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
# });
# 这样之后，就可以像原来一样的使用 jQuery.ajax() 和 jQuery.post()了
# 最后，附上一个 Django Ajax CSRF 实例：exam.zip