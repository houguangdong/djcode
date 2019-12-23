#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/18 09:54


# 本文主要讲解 nginx + uwsgi socket 的方式来部署 Django，比 Apache mod_wsgi 要复杂一些，但这是目前主流的方法。
# 1. 运行开发服务器测试
# cd zqxt # 进入项目 zqxt 目录
# python manage.py runserver
# 运行开发服务器测试，确保开发服务器下能正常打开网站。

# 2. 安装 nginx 和 需要的包
# 2.1 安装 nginx 等软件
# ubuntu / Linux Mint 等，下面简写为 (ubuntu):
# sudo apt-get install python-dev nginx
# centos / Fedora/ redhat 等，下面简写为 (centos)
# sudo yum install epel-release
# sudo yum install python-devel nginx

# 2.2 安装 supervisor, 一个专门用来管理进程的工具，我们用它来管理 uwsgi 进程
# sudo pip install supervisor

# Ubuntu用户 请直接看 3，以下是CentOS 注意事项：
# CentOS下，如果不是非常懂 SELinux 和 iptables 的话，为了方便调试，可以先临时关闭它们，如果发现部署了之后出不来结果，可以临时关闭测试一下，这样就知道是不是 SELinux 和 iptables 的问题
# CentOS 7 iptables如何使用：http://stackoverflow.com/questions/24756240/
# 将 SELinux 设置为宽容模式，方便调试：
# sudo setenforce 0

# 防火墙相关的设置：
# 可以选择临时关闭防火墙
# sudo service iptables stop

# 或者开放一些需要的端口，比如
# sudo iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT

# 上面的两条命令，如果是 CentOS 7 用
# 临时关闭防火墙
# sudo systemctl stop firewalld
# 或者 开放需要的端口
# sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
# sudo firewall-cmd --reload
# 备注：由于我还没有用 最新版本的 Fedora ，新版 Fedora 需要用 dnf 来安装包，有需求的同学自测，可以参考这里。

# 3. 使用 uwsgi 来部署
# 安装 uwsgi
# sudo pip install uwsgi --upgrade

# 使用 uwsgi 运行项目
# uwsgi --http :8001 --chdir /path/to/project --home=/path/to/env --module project.wsgi
# 这样就可以跑了，--home 指定virtualenv 路径，如果没有可以去掉。project.wsgi 指的是 project/wsgi.py 文件

# 如果提示端口已经被占用:
# probably another instance of uWSGI is running on the same address (:8002).
# bind(): Address already in use [core/socket.c line 764]

# 这时可以把相关的进程 kill 掉:
# 按照端口进行查询：
# lsof -i :8002
# 可以查出：
# COMMAND  PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
# uwsgi   2208   tu    4u  IPv4 0x53492abadb5c9659      0t0  TCP *:teradataordbms (LISTEN)
# uwsgi   2209   tu    4u  IPv4 0x53492abadb5c9659      0t0  TCP *:teradataordbms (LISTEN)

# 这时根据 PID 可以用下面的命令 kill 掉相关程序：
# sudo kill -9 2208 2209
# 按照程序名称查询：
# ps aux | grep uwsgi

# 补充内容：
# 使用 gunicorn 代替 uwsgi 的方法
# sudo pip install gunicorn

# 在项目目录下运行下面的命令进行测试：
# gunicorn -w4 -b0.0.0.0:8001 zqxt.wsgi
# -w 表示开启多少个worker，-b 表示要使用的ip和port，我们这里用的是 8001，0.0.0.0代表监控电脑的所有 ip。

# 如果使用了 virtualenv 可以这样
# /path/to/env/bin/gunicorn --chdir /path/to/project --pythonpath /path/to/env/ -w4 -b0.0.0.0:8017 project.wsgi:application
# 用 --pythonpath 指定依赖包路径，多个的时候用逗号,隔开，如：'/path/to/lib,/home/tu/lib'

# 4. 使用supervisor来管理进程
# 安装 supervisor 软件包
# (sudo) pip install supervisor
# 生成 supervisor 默认配置文件，比如我们放在 /etc/supervisord.conf 路径中：
# (sudo) echo_supervisord_conf > /etc/supervisord.conf

# 打开 supervisor.conf 在最底部添加（每一行前面不要有空格，防止报错）：
# [program:zqxt]
# command=/path/to/uwsgi --http :8003 --chdir /path/to/zqxt --module zqxt.wsgi
# directory=/path/to/zqxt
# startsecs=0
# stopwaitsecs=0
# autostart=true
# autorestart=true

# command 中写上对应的命令，这样，就可以用 supervisor 来管理了。

# 启动 supervisor
# (sudo) supervisord -c /etc/supervisord.conf
# 重启 zqxt 程序（项目）：
# (sudo) supervisorctl -c /etc/supervisord.conf restart zqxt
# 启动，停止，或重启 supervisor 管理的某个程序 或 所有程序：
# (sudo) supervisorctl -c /etc/supervisord.conf [start|stop|restart] [program-name|all]

# 以 uwsgi 为例，上面这样使用一行命令太长了，我们使用 ini 配置文件来搞定，比如项目在 /home/tu/zqxt 这个位置，
# 在其中新建一个 uwsgi.ini 全路径为 /home/tu/zqxt/uwsgi.ini
# [uwsgi]
# socket = /home/tu/zqxt/zqxt.sock
# chdir = /home/tu/zqxt
# wsgi-file = zqxt/wsgi.py
# touch-reload = /home/tu/zqxt/reload
#
# processes = 2
# threads = 4
#
# chmod-socket = 664
# chown-socket = tu:www-data
#
# vacuum = true

# 注意上面的 /home/tu/zqxt/zqxt.sock ，一会儿我们把它和 nginx 关联起来。
# 在项目上新建一个空白的 reload 文件，只要 touch 一下这个文件（touch reload) 项目就会重启。
# 注意：不建议把 sock 文件放在 /tmp 下，比如 /tmp/xxx.sock (不建议)！有些系统的临时文件是 namespaced 的，
# 进程只能看到自己的临时文件，导致 nginx 找不到 uwsgi 的 socket 文件，访问时显示502，
# nginx 的 access log 中显示 unix: /tmp/xxx.sock failed (2: No such file or directory)，
# 所以部署的时候建议用其它目录来放 socket 文件，比如放在运行nginx用户目录中，也可以专门弄一个目录来存放 sock 文件，比如 /tmp2/

# sudo mkdir -p /tmp2/ && sudo chmod 777 /tmp2/
# 然后可以用 /tmp2/zqxt.sock 这样的路径了
# 详细参考 http://stackoverflow.com/questions/32974204/got-no-such-file-or-directory-error-while-configuring-nginx-and-uwsgi

# 修改 supervisor 配置文件中的 command 一行：
# [program:zqxt]
# command=/path/to/uwsgi --ini /home/tu/zqxt/uwsgi.ini
# directory=/path/to/zqxt
# startsecs=0

# 然后重启一下 supervisor：
# (sudo) supervisorctl -c /etc/supervisord.conf restart zqxt
# 或者
# (sudo) supervisorctl -c /etc/supervisord.conf restart all

# 5. 配置 Nginx
# 新建一个网站 zqxt
# sudo vim /etc/nginx/sites-available/zqxt.conf
# 写入以下内容：
# server {
#     listen 80;
#     server_name www.ziqiangxuetang.com;
#     charset utf-8;
#     client_max_body_size 75M;
#
#     location /media
#     {
#         alias /path/to/project/media;
#     }
#
#     location /static
#     {
#         alias /path/to/project/static;
#     }
#
#     location / {
#         uwsgi_pass unix: ///home/tu/zqxt/zqxt.sock;
#         include /etc/nginx/uwsgi_params;
#     }
# }

# 激活网站：
# sudo ln -s /etc/nginx/sites-available/zqxt.conf /etc/nginx/sites-enabled/zqxt.conf

# 测试配置语法问题
# sudo service nginx configtest 或 /path/to/nginx -t

# 重启 nginx 服务器：
# sudo service nginx reload 或 sudo service nginx restart 或 /path/to/nginx -s reload

# uwsgi ini 配置文件：http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html#configuring-uwsgi-to-run-with-a-ini-file