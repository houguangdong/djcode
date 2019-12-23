# -*- encoding: utf-8 -*-
# django_admin.py startproject mysite
# 我们会发现执行命令后，新建了一个 mysite 目录，其中还有一个 mysite 目录，
# 这个子目录 mysite 中是一些项目的设置 settings.py 文件，总的urls配置文件
# urls.py 以及部署服务器时用到的 wsgi.py 文件， __init__.py 是python包的目录结构必须的，与调用有关

# 我们到外层那个 mysite 目录下(不是mysite中的mysite目录)
# 二, 新建一个应用(app), 名称叫 learn
# python manage.py startapp learn # learn 是一个app的名称
# 我们可以看到mysite中多个一个 learn 文件夹，其中有以下文件。
# learn/
# ├── __init__.py
# ├── admin.py
# ├── models.py
# ├── tests.py
# └── views.py
# 注：Django 1.8.x 以上的，还有一个 migrations 文件夹。Django 1.9.x 还会在 Django 1.8 的基础上多出一个 apps.py 文件。但是这些都与本文无关。


# 把我们新定义的app加到settings.py中的INSTALL_APPS中
# 修改 mysite/mysite/settings.py
# 备注,这一步是干什么呢? 新建的 app 如果不加到 INSTALL_APPS 中的话,
# django 就不能自动找到app中的模板文件(app-name/templates/下的文件)和
# 静态文件(app-name/static/中的文件) , 后面你会学习到它们分别用来干什么.
# 定义视图函数（访问页面时的内容）
# 我们在learn这个目录中,把views.py打开,修改其中的源代码,改成下面的



