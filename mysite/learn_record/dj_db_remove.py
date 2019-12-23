#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/19 12:10

# Django 数据迁移
# 本文主要讲数据库的迁移方法，包含不同数据库，如 SQLite3, MySQL, PostgreSQL 之间数据迁移方案，以及数据在不同机器上迁移方案
# 一，简单的数据导出与导入（简单的迁移）
# 1. django 项目提供了一个导出的方法 python manage.py dumpdata, 不指定 appname 时默认为导出所有的app
# python manage.py dumpdata [appname] > appname_data.json
# 比如我们有一个项目叫 mysite, 里面有一个 app 叫 blog ,我们想导出 blog 的所有数据
# python manage.py dumpdata blog > blog_dump.json
# 2. 数据导入,不需要指定 appname
# python manage.py loaddata blog_dump.json
# 备注：一些常用的
# python manage.py dumpdata auth > auth.json # 导出用户数据
# 优点：可以兼容各种支持的数据库，也就是说，以前用的是 SQLite3，可以导出后，用这种方法导入到 MySQL, PostgreSQL等数据库，反过来也可以。
# 缺点：数据量大的时候，速度相对较慢，表的关系比较复杂的时候可以导入不成功。

# 二，数据库的迁移
# 2.1.  用 Django 自带的命令
# 比如早期我们为了开发方便，用的sqlite3数据库，后来发现网站数据太多，sqlite3性能有点跟不上了，想换成postgreSQL,或者 MySQL的时候。
# 如果还我还使用上面的命令，如果你运气好的话，也许会导入成功，流程如下：
# 2.1.1. 从原来的整个数据库导出所有数据
# python manage.py dumpdata > mysite_all_data.json
# 2.1.2. 将mysite_all_data.json传送到另一个服务器或电脑上导入
# python manage.py loaddata mysite_all_data.json
# 如果你运气好的话可能会导入完成，但是往往不那么顺利，原因如下：
# a) 我们在写models的时候如果用到CharField,就一定要写max_length,在sqlite3中是不检查这个最大长度的，你写最大允许长度为100，
# 你往数据库放10000个，sqlite3都不报错，而且不截断数据的长度，这似乎是slite3的优点，但是也给从sqlite3导入其它数据库带来了困难,
# 因为MySQL和PostgreSQL数据库都会检查最大长度，超出时就报错！
# b) Django 自带的contentType会导致出现一些问题
# 用上面的方法只迁移一个app应该问题不大，但是如果有用户，用户组挂钩，事情往往变得糟糕！如果导入后没有对数据进行修改，你可以考虑重新导入，
# 可能还要快一些，如果是手动在后台输入或者修改过，这种方法就不适用了

# 2.2, 用数据库自带的导出导入命令
# 预备知识：
# 先输入 mysql (比如 mysql -u root -p) 进入数据库 shell

# 创建 GBK 格式的数据库 zqxt
# create database `zqxt` DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci;

# 创建 UTF8 格式的数据库 zqxt
# CREATE DATABASE `zqxt` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

# 赋予数据库（zqxt）权限给某用户，可以是已经存在的用户或新用户名
# GRANT ALL PRIVILEGES ON zqxt.* TO "任意用户名"@"localhost" IDENTIFIED BY "新密码";

# 刷新权限
# FLUSH PRIVILEGES;

# 退出数据库shell
# EXIT;

# 假定 Django 用的数据库名称为 zqxt
# 2.2.1 在 PostgreSQL 中：
# 导出数据库 zqxt 到 zqxt.sql 文件中
# pg_dump zqxt > zqxt.sql

# 导入数据库到 新的服务器
# psql zqxt - f zqxt.sql

# 注意：数据导入导出可能需要数据库超级权限,用 sudo su postgres 切换到数据库超级用户 postgres

# 2.2.2 在MySQL 中：
# 使用网页工具，比如phpMyAdmin 导入导出很简单，这里就不说了，主要说一下命令行如何操作：
# 导出数据库 zqxt 到 zqxt.sql 文件中
# mysqldump -u username -p --database zqxt > zqxt.sql

# 导入数据库到 新的服务器 (假设数据库已经创建好）
# cat /path/to/zqxt.sql | mysql -u username -p zqxt
# 或
# mysql -u username -p zqxt < /path/to/zqxt.sql
# 或
# mysql -u username -p zqxt 进入mysql shell 后，执行source/path/to/zqxt.sql
# 输入密码开始导入数据

# 总结：其它的数据库，请自行搜索如何导入导出，整个数据库导出的好处就是对数据之间的关系处理比较省事，比如自强学堂里面的很多教程，
# 上一篇和下一篇是一个一对一的关系，这样的话用 python manage.py dumpdata 无法导出教程与教程的关系，但是数据库整个导出就没有任何问题，
# 当然也可以写一个脚本去导出关系再导入。Django 自带的 python manage.py dumpdata 和 python manage.py loaddata 最大的好处就是可以跨数据库进行导入导出。