#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/16 20:23


# Django 部署(Apache)
# Django + nginx + Gunicorn / uwsgi 部署方式，参见另一篇：Django部署（nginx）
# 自己的服务器（比如用的阿里云服务器）请看下文：
# 如果是新手，个人推荐用ubuntu, 除非你对linux非常熟悉，ubuntu服务器的优点：
# 一，开机apache2等都自动启动，不需要额外设置
# 二，安装软件非常方便apt-get搞定
# 三，安装ssh，git等也非常容易，几乎是傻瓜化
# 如果你在虚拟机或个人电脑中安装，也可以试试Linux Mint, 它用起来更简单，和ubuntu兼容。

# 下面是ubuntu上的部署详细步骤：

# 1.安装apache2和mod_wsgi
# sudo apt-get install apache2
# Python 2
# sudo apt-get install libapache2-mod-wsgi
# Python 3
# sudo apt-get install libapache2-mod-wsgi-py3
# 2.确认安装的apache2版本号
# apachectl - v
# 3.准备一个新网站
# ubuntu的apache2配置文件在 /etc/apache2/ 下
# 备注：centos 用户 apache 名称为 httpd 在 /etc/httpd/ 中（可以参考文章下面置顶的评论）
# 新建一个网站配置文件
# sudo vi /etc/apache2/sites-available/sitename.conf
# 示例内容如下：
# < VirtualHost *:80 >
#     ServerName
#     www.yourdomain.com
#     ServerAlias
#     otherdomain.com
#     ServerAdmin
#     tuweizhong @ 163.
#     com
#
#     Alias / media / / home / tu / blog / media /
#     Alias / static / / home / tu / blog / static /
#
#     < Directory / home / tu / blog / media >
#     Require
#     all
#     granted
#     < / Directory >
#
#     < Directory / home / tu / blog / static >
#       Require all granted
#     < / Directory >
#
#     WSGIScriptAlias / / home / tu / blog / blog / wsgi.py
#     # WSGIDaemonProcess ziqiangxuetang.com python-path=/home/tu/blog:/home/tu/.virtualenvs/blog/lib/python2.7/site-packages
#     # WSGIProcessGroup ziqiangxuetang.com
#
#     < Directory / home / tu / blog / blog >
#     < Files wsgi.py >
#       Require all granted
#     < / Files >
#     < / Directory >
# < / VirtualHost >


# 如果你的apache版本号是2.2.x（第二步有方法判断）
# 用下面的代替  Require all granted
# Order deny, allow
# Allow from all

# 备注：把上面配置文件中这两句的备注去掉，可以使用 virtualenv 来部署网站，当然也可以只写一个 /home/tu/blog
# WSGIDaemonProcess ziqiangxuetang.com python-path=/home/tu/blog:/home/tu/.virtualenvs/blog/lib/python2.7/site-packages
# WSGIProcessGroup ziqiangxuetang.com

# 4.修改wsgi.py文件
# 注意：上面如果写了 WSGIDaemonProcess 的话，这一步可以跳过，即可以不修改 wsgi.py 文件。
# 上面的配置中写的 WSGIScriptAlias / /home/tu/blog/blog/wsgi.py
# 就是把apache2和你的网站project联系起来了
# import os
# from os.path import join, dirname, abspath
#
# PROJECT_DIR = dirname(dirname(abspath(__file__)))  # 3
# import sys  # 4
#
# sys.path.insert(0, PROJECT_DIR)  # 5
#
# os.environ["DJANGO_SETTINGS_MODULE"] = "blog.settings"  # 7
#
# from django.core.wsgi import get_wsgi_application
#
# application = get_wsgi_application()

# 第 3，4，5 行为新加的内容，作用是让脚本找到django项目的位置，也可以在sitename.conf中做，用WSGIPythonPath,想了解的自行搜索, 第 7 行如果一台服务器有多个django project时一定要修改成上面那样，否则访问的时候会发生网站互相串的情况，即访问A网站到了B网站，一会儿正常，一会儿又不正常（当然也可以使用 mod_wsgi daemon 模式,点击这里查看）

# 5. 设置目录和文件权限
# 一般目录权限设置为 755，文件权限设置为 644
# 假如项目位置在 /home/tu/zqxt （在zqxt 下面有一个 manage.py，zqxt 是项目名称）

# cd /home/tu/
# sudo chmod -R 644 zqxt
# sudo find zqxt -type d | xargs chmod 755

# apache 服务器运行用户可以在 /etc/apache2/envvars 文件里面改，这里使用的是默认值，当然也可以更改成自己的当前用户，这样的话权限问题就简单很多，但在服务器上推荐有 www-data 用户，更安全。以下是默认设置：

# Since there is no sane way to get the parsed apache2 config in scripts, some
# settings are defined via environment variables and then used in apache2ctl,
# /etc/init.d/apache2, /etc/logrotate.d/apache2, etc.

# export APACHE_RUN_USER=www-data
# export APACHE_RUN_GROUP=www-data

# 上传文件夹权限
# media 文件夹一般用来存放用户上传文件，static 一般用来放自己网站的js，css，图片等，在settings.py中的相关设置
# STATIC_URL 为静态文件的网址 STATIC_ROOT 为静态文件的根目录，
# MEDIA_URL 为用户上传文件夹的根目录，MEDIA_URL为对应的访问网址
# 在settings.py中设置：

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# upload folder
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 在 Linux 服务器上，用户上传目录还要设置给 www-data 用户的写权限，下面的方法比较好，不影响原来的用户的编辑。
# 假如上传目录为 zqxt/media/uploads 文件夹,进入media文件夹，将 uploads 用户组改为www-data，并且赋予该组写权限:
# cd media/ # 进入media文件夹
# sudo chgrp -R www-data uploads
# sudo chmod -R g+w uploads

# 备注：这两条命令，比直接用sudo chown -R www-data:www-data uploads 好，因为下面的命令不影响文件原来所属用户编辑文件，fedora系统应该不用设置上面的权限，但是个人强烈推荐用ubuntu,除非你对linux非常熟悉，你自己选择。
# 如果你使用的是sqlite3数据库，还会提示 Attempt to write a readonly database,同样要给www-data写数据库的权限
# 进入项目目录的上一级，比如project目录为 /home/tu/blog 那就进入 /home/tu 执行下面的命令（和修改上传文件夹类似）

# sudo chgrp www-data blog
# sudo chmod g+w blog
# sudo chgrp www-data blog/db.sqlite3  # 更改为你的数据库名称
# sudo chmod g+w blog/db.sqlite3
# 备注：上面的不要加 -R ,-R是更改包括所有的子文件夹和文件，这样不安全。个人建议可以专门弄一个文件夹,用它来放sqlite3数据库，给该文件夹www-data写权限，而不是整个项目给写权限，有些文件只要读的权限就够了，给写权限会造成不安全。

# 6. 激活新网站
# sudo a2ensite sitename 或 sudo a2ensite sitename.conf
# 如果顺利，这样网站就搭建成功，访问你的网址试试看，如果出现问题就接着看下面的。

# 7.错误排查
# 一，没有静态文件，网站打开很乱，没有布局，多半是静态文件没有生效。
# 1 确保你的配置文件中的路径是正确的
# 2 确保你的settings.py中的文件设置正确
# 3 收集静态文件(详细静态文件部署教程）

# python manage.py collectstatic

# 二，网站打开后报错
# 这时你可以把settings.py更改
# DEBUG = True
# 重启服务器
# sudo service apache2 restart
# 再访问网站 来查看具体的出错信息。
# 如果这样做还看不到出错信息，只是显示一个服务器错误，你可以查看apache2的错误日志
# cat /var/log/apache2/error.log
# 根据错误日志里面的内容进行修正！

# 总结:
# 部署时文件对应关系:
# sitename.conf --> wsgi.py --> settings.py --> urls.py --> views.py
# 扩展
# 明白了上面的关系, 一个 Django project 使用多个域名或让app使用子域名很简单,只要新建一个 wsgi.py 文件,更改里面对应的settings文件,新的settings文件可以对应新的urls.py,从而做到访问与原来不同的地址!