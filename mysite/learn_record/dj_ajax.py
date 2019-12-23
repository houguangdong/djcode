#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/20 15:21

# Django Ajax
# 有时候我们需要在不刷新的情况下载入一些内容，在网页的基本知识中我们介绍了 ajax 技术。
# 在本文中讲解如何用 Django 来实现 不刷新网页的情况下加载一些内容。
# 由于用 jQuery 实现 ajax 比较简单，所以我们用 jQuery库来实现，想用原生的 javascript 的同学可以参考：ajax 教程，下面也有例子提供下载。
# 本节有多个实例提供下载，通过看代码可以更快的学习。
# 第一节，源代码下载：zqxt_ajax_1.zip
# 这里用 Django 表单 第一节 中的一个例子，我们要实现的是在不刷新的情况下显示计算结果到页面上。
# 修改 index.html 文件

# <!DOCTYPE html>
# <html>
# <body>
# <p>请输入两个数字</p>
# <form action="/add/" method="get">
# a: <input type="text" id="a" name="a"> <br>
# b: <input type="text" id="b" name="b"> <br>
# <p>result: <span id='result'></span></p>
# <button type="button" id='sum'>提交</button>
# </form>

# <script src="http://apps.bdimg.com/libs/jquery/1.11.1/jquery.min.js"></script>
# <script>
# $(document).ready(function(){
# $("#sum").click(function(){
# var a = $("#a").val();
# var b = $("#b").val();
# $.get("/add/",{'a':a,'b':b}, function(ret){
# $('#result').html(ret)
# })
# });
# });
# </script>
# </body>
# </html>

# 在原来的基础上，在一些元素上加了 id, 以便于获取值和绑定数据，然后我们用了jQuery.get() 方法，并用 $(selector).html() 方法将结果显示在页面上，如下图：
# 备注：关于请求头和 request.is_ajax() 方法使用
# views.py 中可以用  request.is_ajax() 方法判断是否是 ajax 请求，需要添加一个 HTTP 请求头：
# 原生javascript：
# xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
# 用 jQuery：
# 用 $.ajax 方法代替 $.get，因为 $.get 在 IE 中不会发送 ajax header
# 服务器端会将请求头的值全部大写，中划线改成下划线，并在非标准的头前面加上 HTTP_，这个过程可以认为相当于以下Python代码：
# STANDARD_HEADERS = ['REFER', 'HOST', ]  # just for example
#
#
# def handle_header(value):
#     value = value.replace('-', '_').upper()
#
#     if value in STANDARD_HEADERS:
#         return value
#
#     return 'HTTP_' + value
# 判断ajax方法，以及原生的 javascript实现ajax的示例下载：zqxt_views_ajax.zip

# 第二节，源代码下载：zqxt_ajax_list_dict.zip
# 更复杂的例子，传递一个数组或字典到网页，由JS处理，再显示出来。
# views.py
# from django.http import HttpResponse
# import json
#
#
# def ajax_list(request):
#     a = range(100)
#     return HttpResponse(json.dumps(a), content_type='application/json')
#
#
# def ajax_dict(request):
#     name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
#     return HttpResponse(json.dumps(name_dict), content_type='application/json')

# Django 1.7 及以后的版本有更简单的方法（使用 JsonResponse(官方文档))：
# from django.http import JsonResponse
#
#
# def ajax_list(request):
#     a = range(100)
#     return JsonResponse(a, safe=False)
#
#
# def ajax_dict(request):
#     name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
#     return JsonResponse(name_dict)

# 在 django 1.6 及以前的旧版本中可以自己写一个 JsonResponse 方法，如下：
# from django.http import HttpResponse
#
# import json
#
#
# class JsonResponse(HttpResponse):
#     def __init__(self,
#                  content={},
#                  mimetype=None,
#                  status=None,
#                  content_type='application/json'):
#         super(JsonResponse, self).__init__(
#             json.dumps(content),
#             mimetype=mimetype,
#             status=status,
#             content_type=content_type)

# 写好后，我们在 urls.py 中添加以下两行：
# url(r'^ajax_list/$', 'tools.views.ajax_list', name='ajax-list'),
# url(r'^ajax_dict/$', 'tools.views.ajax_dict', name='ajax-dict'),

# 打开开发服务器 python manage.py runserver
# 我们访问对应的网址会看到输出值：
# 下一步就是在无刷新的情况下把内容加载到网页了，我们修改一下首页的模板 index.html
# <!DOCTYPE html>
# <html>
# <body>
# <p>请输入两个数字</p>
# <form action="/add/" method="get">
# a: <input type="text" id="a" name="a"> <br>
# b: <input type="text" id="b" name="b"> <br>
# <p>result: <span id='result'></span></p>
# <button type="button" id='sum'>提交</button>
# </form>
# <div id="dict">Ajax 加载字典</div>
# <p id="dict_result"></p>
# <div id="list">Ajax 加载列表</div>
# <p id="list_result"></p>
# <script src="http://apps.bdimg.com/libs/jquery/1.11.1/jquery.min.js"></script>
# <script>
# $(document).ready(function(){
# // 求和 a + b
# $("#sum").click(function(){
# var a = $("#a").val();
# var b = $("#b").val();
# $.get("/add/",{'a':a,'b':b}, function(ret){
# $('#result').html(ret);
# })
# });

# // 列表 list
# $('#list').click(function(){
# $.getJSON('/ajax_list/',function(ret){
# //返回值 ret 在这里是一个列表
# for (var i = ret.length - 1; i >= 0; i--) {
# // 把 ret 的每一项显示在网页上
# $('#list_result').append(' ' + ret[i])
# };
# })
# })

# // 字典 dict
# $('#dict').click(function(){
# $.getJSON('/ajax_dict/',function(ret){
# //返回值 ret 在这里是一个字典
# $('#dict_result').append(ret.twz + '<br>');
# // 也可以用 ret['twz']
# })
# })
# });
# </script>
# </body>
# </html>

# 技能提升：getJSON中的写的对应网址，用 urls.py 中的 name 来获取是一个更好的方法!
# 标签：{% url 'name' %}
# <script>
#     $(document).ready(function(){
#       // 求和 a + b
#       $("#sum").click(function(){
#         var a = $("#a").val();
#         var b = $("#b").val();
#         $.get("{% url 'add' %}", {'a': a, 'b': b}, function(ret){
#         $('#result').html(ret);
#         })
#         });
#
#         // 列表list
#     $('#list').click(function(){
#         $.getJSON("{% url 'ajax-list' %}", function(ret){
#         // 返回值ret   在这里是一个列表
#         for (var i = ret.length - 1; i >= 0; i--) {
#             // 把 ret 的每一项显示在网页上
#             $('#list_result').append(' ' + ret[i])
#         };
#     })
#     })
#
#     // 字典 dict
#     $('#dict').click(function(){
#         $.getJSON("{% url 'ajax-dict' %}", function(ret){
#         // 返回值 ret 在这里是一个字典
#         $('#dict_result').append(ret.twz + '<br>');
#         // 也可以用 ret['twz']
# })
# })
# });
# </script>

# 这样做最大的好处就是在修改 urls.py 中的网址后，不用改模板中对应的网址。
# 补充：如果是一个复杂的 列表 或 字典，因为比如如下信息：
# person_info_dict = [
#     {"name":"xiaoming", "age":20},
#     {"name":"tuweizhong", "age":24},
#     {"name":"xiaoli", "age":33},
# ]
# 这样我们遍历列表的时候，每次遍历得到一个字典，再用字典的方法去处理，当然有更简单的遍历方法：
# 用 $.each() 方法代替 for 循环，html 代码（jQuery)
# $.getJSON('ajax-url-to-json', function(ret) {
#     $.each(ret, function(i,item){
#         // i 为索引，item为遍历值
#     });
# });
# 补充：如果 ret 是一个字典，$.each 的参数有所不同，详见：http://api.jquery.com/jquery.each/
# $.getJSON('ajax-get-a-dict', function(ret) {
#     $.each(ret, function(key, value){
#         // key 为字典的 key，value 为对应的值
#     });
# });

# 最后，附上一个返回图片并显示的ajax实例：