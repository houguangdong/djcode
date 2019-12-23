# -*- encoding: utf-8 -*-
# 教程中所有的文件，没有特别说明的，都是以 utf8 格式编码的，请养成这个习惯。
# url(r'^add/$', calc_views.add, name='add'), 这里的 name='add' 是用来干什么的呢？
# 简单说，name 可以用于在 templates, models, views ……中得到对应的网址，
# 相当于“给网址取了个名字”，只要这个名字不变，网址变了也能通过名字获取到。

# 为了进一步弄清这个问题，我们先建一个首页的视图和url
# 这样，使用render的时候，Django 会自动找到 INSTALLED_APPS 中列出的各个 app 下的 templates 中的文件。
# 小提示，DEBUG=True 的时候，Django 还可以自动找到 各 app 下 static 文件夹中的静态文件（js，css，图片等资源），方便开发，后面有专门的章节会讲这些。
# 4. 我们在 calc 这个 app 中新建一个 templates 文件夹，在templates中新建一个 home.html （关于模板更详细的可以稍后看下一节）
# 文件 calc/templates/home.html 中写入以下内容（保存时用 utf8 编码）
# 我们计算加法的时候用的是/add/4/5/，后来需求发生变化，比如改成/4_add_5/，但在网页中，代码中很多地方都写死的/add/4/5/，比如模板中可能是这么写的
# <a href = "/add/4/5/" > 计算4 + 5 < / a >如果这样写“死网址”，会使得在改了网址（正则）后，模板（template)，视图(views.py，比如用于URL跳转)，
# 模型(models.py，获取记录访问地址等）用了此网址的，都必须进行相应的更改，修改的代价很大，一不小心，有的地方没改过来，就不能用了。
# 那么有没有更优雅的方式来解决这个问题呢？当然答案是肯定的。
# 我们先说一下如何用Python代码获取对应的网址（可以用在views.py，models.py等各种需要转换得到网址的地方）：
# 我们在终端上输入(推荐安装bpython, 这样Django会用bpython的shell)
# python manage.py shell
# >>> from django.core.urlresolvers import reverse  # django 1.4.x - django 1.10.x
# 或者
# >>> from django.urls import reverse  # Django 1.10.x - Django 2.x 新的，更加规范了
# >>> reverse('add2', args=(4, 5))
# u'/add/4/5/'
# >>> reverse('add2', args=(444, 555))
# u'/add/444/555/'
# reverse接收url中的name作为第一个参数，我们在代码中就可以通过reverse()来获取对应的网址（这个网址可以用来跳转，也可以用来计算相关页面的地址），
# 只要对应的url的name不改，就不用改代码中的网址。
# 在网页模板中也是一样，可以很方便的使用。
# 不带参数的：
# { % url 'name' %}
# 带参数的：参数可以是变量名
# { % url 'name' 参数 %}
# 例如：
# <a href = "{% url 'add2' 4 5 %}" >link</a>
# 上面的代码渲染成最终的页面是
# <a href = "/add/4/5/" >link</a>
# 这样就可以通过
# { % url 'add2' 4 5 %} 获取到对应的网址 /add/4/5/
# 当 urls.py 进行更改，前提是不改 name（这个参数设定好后不要轻易改），获取的网址也会动态地跟着变，比如改成：
#     url(r'^new_add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),
# 注意看重点 add 变成了 new_add，但是后面的 name='add2' 没改，这时 {% url 'add2' 4 5 %} 就会渲染对应的网址成 /new_add/4/5/
# 用在 views.py 或 models.py 等地方的 reverse函数，同样会根据 name 对应的url获取到新的网址。
# 想要改网址的时候，修改 urls.py 中的正则表达式部分（url 参数第一部分），name 不变的前提下，其它地方都不需要修改。

# 另外，比如用户收藏夹中收藏的URL是旧的，如何让以前的 /add/3/4/自动跳转到现在新的网址呢？
# 要知道Django不会帮你做这个，这个需要自己来写一个跳转方法：
# 具体思路是，在views.py写一个跳转的函数：
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse  # Django 1.4.x - Django 1.10.x
#  from django.urls import reverse  # Django 1.10.x - Django 2.x
def old_add2_redirect(request, a, b):
    return HttpResponseRedirect(
        reverse('add2', args=(a, b))
    )

# urls.py中：
# url(r'^add/(\d+)/(\d+)/$', calc_views.old_add2_redirect),
# url(r'^new_add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),
# 这样，假如用户收藏夹中有 /add/4/5/ ，访问时就会自动跳转到新的 /new_add/4/5/ 了
# 开始可能觉得直接写网址简单，但是用多了你一定会发现，用“死网址”的方法很糟糕。