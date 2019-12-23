#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/16 09:42

# 本文干货较多，对部署有困惑的坚持读完，一定会有收获的，建议把此文分享给有同样困惑的小伙伴吧。
# 本文主要讲解在 Linux 平台下，使用 Nginx + uWSGI 的方式来部署来 Django，这是目前比较主流的方式。当然你也可以使用 Gunicorn 代替 uWSGI，不过原理都是类似的，弄懂了其中一种，其它的方式理解起来问题也不会很大。
# 有很多人曾经在邮件中咨询过问我如何部署，部署确实对开发者有着较高的要求，尤其是初学者来说，部署比较难，这很正常，千万不要轻易就放弃了。
# 回想我2013年刚开始接触也是一头雾水，整整弄了四五天才完全搞懂，部署好了真是欣喜若狂。我自认为算不上聪明，我都能搞明白，你也一定能行。最关键和宝贵的品质就是坚持不懈和勇于试错。下面就让我们一起开始正式的部署教程吧。

# 基础知识储备
# 当我们发现用浏览器不能访问的时候，我们需要一步步排查问题。
# 整个部署的链路是 Nginx -> uWSGI -> Python Web程序，通常还会提到supervisord工具。
# uWSGI是一个软件，部署服务的工具，了解整个过程，我们先了解一下WSGI规范，uwsgi协议等内容。
#
# WSGI（Web Server Gateway Interface)规范，WSGI规定了Python Web应用和Python Web服务器之间的通讯方式。
# 目前主流的Python Web框架，比如Django，Flask，Tornado等都是基于这个规范实现的。
#
# uwsgi协议是uWSGI工具独有的协议，简洁高效的uwsgi协议是选择uWSGI作为部署工具的重要理由之一，详细的 uwsgi协议 可以参考uWSGI的文档。
# uWSGI是 实现了uwsgi协议，WSGI规范和HTTP协议的 一个C语言实现的软件。
#
# Nginx是一个Web服务器，是一个反向代理工具，我们通常用它来部署静态文件。主流的Python Web开发框架都遵循WSGI规范。
# uWSGI通过WSGI规范和我们编写的服务进程通讯，然后通过自带的高效的 uwsgi 协议和 Nginx进行通讯，最终Nginx通过HTTP协议将服务对外透出。
# 当一个访问进来的时候，首先到 Nginx，Nginx会把请求（HTTP协议）转换uwsgi协议传递给uWSGI，uWSGI通过WSGI和web server进行通讯取到响应结果，再通过uwsgi协议发给Nginx，最终Nginx以HTTP协议发现响应给用户。
# 有些同学可能会说，uWSGI不是支持HTTP协议么，也支持静态文件部署，我不用Nginx行不行？
# 当然可以，这么做没问题，但目前主流的做法是用Nginx，毕竟它久经考验，更稳定，当然也更值得我们信赖。
#
# supervisor 是一个进程管理工具。任何人都不能保证程序不异常退出，不别被人误杀，所以一个典型的工程做法就是使用supervisor看守着你的进程，一旦异常退出它会立马进程重新启动起来。
# 如果服务部署后出现异常，不能访问。我们需要分析每一步有没有问题，这时候就不得不用到Linux中一些命令。
#
# 进程分析
# 进程是计算机分配资源的最小单位，我们的程序至少是运行在一个进程中。
# 1. 查看进程信息
#
# 通常我们使用 ps aux | grep python 来查看系统中运行的 python 进程，输出结果如下：
#
# tu@linux / $ ps uax | grep python
# USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
# root      1780  0.0  0.0  58888 10720 ?        Ss   Jan15   8:46 /usr/bin/python /usr/local/bin/supervisord -c /etc/supervisord.conf
# tu      4491  0.0 18.0 3489820 2960628 ?     Sl   Jan29   0:19 python a.py
# tu     12602  5.3 26.4 4910444 4343708 pts/1 Sl+  12:34   4:07 python b.py
# 有些同学习惯使用 ps -ef | grep xxx 结果也是类似的，读者可以自行尝试。
#
# 输出结果中 USER 后面的 PID 代表进程编号。
# 我们可以通过查看 /proc/PID/ 目录的文件信息来得到这个进程的一些信息（Linux中一切皆文件，进程信息也在文件中），比如它是在哪个目录启动的，启动命令是什么等信息。执行命令后输入内容如下：
# tu@linux /proc/4491 $ sudo ls -ahl
# ...
# dr-xr-xr-x   2 tu tu 0 Feb 17 13:32 attr
# -rw-r--r--   1 tu tu 0 Feb 17 13:32 autogroup
# -r--------   1 tu tu 0 Feb 17 13:32 auxv
# -r--r--r--   1 tu tu 0 Feb 17 13:32 cgroup
# --w-------   1 tu tu 0 Feb 17 13:32 clear_refs
# -r--r--r--   1 tu tu 0 Feb 17 12:49 cmdline  这个文件中有启动进程具体的命令
# -rw-r--r--   1 tu tu 0 Feb 17 13:32 comm
# -rw-r--r--   1 tu tu 0 Feb 17 13:32 coredump_filter
# -r--r--r--   1 tu tu 0 Feb 17 13:32 cpuset
# lrwxrwxrwx   1 tu tu 0 Feb 17 13:32 cwd -> /home/tu  启动进程时的工作目录
# -r--------   1 tu tu 0 Feb 17 13:32 environ  进程的环境变量列表
# lrwxrwxrwx   1 tu tu 0 Feb 17 12:00 exe -> /usr/bin/python2.7 链接到进程的执行命令文件
# ...省去了部分内容
#
# 2. 向进程发送信号
#
# 我们可以使用 kill PID 杀死一个进程，或者使用 kill -9 PID 强制杀死一个进程。
#
# 记得以前在研究生的时候师弟和师妹经常问我，kill -9 里面的 -9 是什么意思，我告诉他们，这是强制杀死进程的意思，让这个进程“九死一生”。当然这是开玩笑，这里的 -9 是信号的一种，kill 命令会向进程发送一个信号，-9代表 SIGKILL 之意，用于强制终止某个进程，当然这是一种无情地，野蛮地方式干掉进程。
# 我们可以通过 kill -l 命令查看到所有的信号
# HUP INT QUIT ILL TRAP ABRT BUS FPE KILL USR1 SEGV USR2 PIPE ALRM TERM STKFLT CHLD CONT STOP TSTP TTIN TTOU URG XCPU XFSZ VTALRM PROF WINCH POLL PWR SYS
#
# 上面的信号是有顺序的，比如第1个是 HUP，第9个是 KILL，下面两种方式是等价的：
# kill -1 PID 和 kill -HUP PID
# kill -9 PID 和 kill -KILL PID
# 信号HUP通常程序用这个信号进行优雅重载配置文件，重新启动并且不影响正在运行的服务。比如
# pkill -1 uwsgi 优雅重启uwsgi 进程，对服务器没有影响
# kill -1 NGINX_PID 优雅重启nginx进程，对服务器没有影响
# 除了知道可以这么使用之外，感兴趣的读者还可以自行学习，深入了解下uwsgi和nginx无损reload的机制。
# 我们常用CTRL+C中断一个命令的执行，其实就是发送了一个信号到该进程
# CTRL-C 发送 SIGINT 信号给前台进程组中的所有进程，常用于终止正在运行的程序。
# CTRL-Z 发送 SIGTSTP 信号给前台进程组中的所有进程，常用于挂起一个进程。
# 每个程序可能对部分信号的功能定义不一致，其它信号的含义大家可以自行学习。
#
#
# 3. 查看进程打开了哪些文件
#
# sudo lsof -p PID
#
# 如果是分析一个你不太了解的进程，这个命令比较有用。
# 可以使用 lsof -p PID | grep TCP 查看进程中的 TCP 连接信息。
#
#
# 4. 查看文件被哪个进程使用
#
# 使用这个命令查看一个文件被哪些进程正在使用 sudo lsof /path/to/file，示例如下：
#
# > sudo lsof /home/tu/.virtualenvs/mic/bin/uwsgi
# COMMAND   PID USER  FD   TYPE DEVICE SIZE/OFF     NODE NAME
# uwsgi    2071 tu txt    REG 253,17  1270899 13240576 /home/tu/.virtualenvs/mic/bin/uwsgi
# uwsgi   13286 tu txt    REG 253,17  1270899 13240576 /home/tu/.virtualenvs/mic/bin/uwsgi
# uwsgi   13287 tu txt    REG 253,17  1270899 13240576 /home/tu/.virtualenvs/mic/bin/uwsgi
# uwsgi   13288 tu txt    REG 253,17  1270899 13240576 /home/tu/.virtualenvs/mic/bin/uwsgi
#
#
# 5. 查看进程当前状态
#
# 当我们发现一个进程启动了，端口也是正常的，但好像这个进程就是不“干活”。比如我们执行的是数据更新进程，这个进程不更新数据了，但还是在跑着。可能数据源有问题，可能我们写的程序有BUG，也可能是更新时要写入到的数据库出问题了（数据库连接不上了，写数据死锁了）。我们这里主要说下第二种，我们自己的程序如果有BUG，导致工作不正常，我们怎么知道它当前正在干什么呢，这时候就要用到Linux中的调试分析诊断strace，可以使用 sudo strace -p PID这个命令。
#
# 通过执行后输出的一些信息，推测分析看是哪些出了问题。
#
# 这里我们讲了一些进程分析的工具和方法，关于进程分析工具和方法还有许多，大家需要不断练习，熟练运用这些工具去排查遇到的问题。
#
# 端口分析
# 比如我们在服务器上运行 Nginx，访问的时候就是连接不上，我们可以使用 ps aux | grep nginx看下nginx进程是不是启动了，也可以看下 80端口有没有被占用。换句话说，如果没有任何程序跑在这个端口上（或者说没有任何程序使用这个端口），证明忘了启动相关程序或者没能启动成功，或者说程序使用的端口被修改了，不是80了，那又怎么可能能访问到呢？
#
# 1. 查看全部端口占用情况
#
# Linux中我们可以使用 netstat 工具来进程网络分析，netstat 命令有非常多选项，这里只列出了常用的一部分
#
# -a或--all 显示所有连接中的Socket，默认不显示 LISTEN 相关的。
# -c或--continuous 持续列出网络状态，不断自动刷新输出。
# -l或--listening 显示监听中的服务器的Socket。
# -n或--numeric 直接使用IP地址，而不是展示域名。
# -p或--programs 显示正在使用Socket的程序进程PID和名称。
# -t或--tcp 显示TCP传输协议的连接。
# -u或--udp 显示UDP传输协议的连接。
# 比如我们可以查看服务器中监控了哪些端口，如果我们的nginx是使用80端口，uwsgi使用的是7001端口，我们就能知道通过下面的命令
# > netstat -nltp
# Active Internet connections (only servers)
# Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
# tcp        0      0 0.0.0.0:7001            0.0.0.0:*               LISTEN      2070/uwsgi
# tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN      1575/redis-server 1
# 就能知道80端口的 nginx 是不是启动成功了，7001端口的uwsgi是不是启动成功了。
# 注意：如果PID和Program Name显示不出来，证明是权限不够，可以使用sudo运行
# 2. 查看具体端口占用情况
#
# > sudo lsof -i :80 (注意端口80前面有个英文的冒号)
#
# COMMAND    PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
# nginx   4123   admin    3u  IPv4  13031      0t0  TCP *:http (LISTEN)
# nginx   4124   admin    3u  IPv4  13031      0t0  TCP *:http (LISTEN)
# 我们可以通过这个方法查询出占用端口的程序，如果遇到端口已经被占用，原来的进程没有正确地终止，可以使用kill命令停掉原来的进程，这样我们就又可以使用这个端口了。
#
# 除了上面讲的一些命令，在部署过程中会经常用到下面的一些Linux命令，如果不清楚它们是做什么的，可以提前自行学习下这些Linux基础命令：
# ls, touch, mkdir, mv, cp, ps, chmod, chown
# 学习完了这些内容，我们应该就具备了部署Linux服务器的基础知识了，在遇到问题后，应该也会有一些调查思路。
# 剩余部分大家再去 自强学堂上看 Django部署，应该会容易懂的多。