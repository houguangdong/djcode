# -*- encoding: utf-8 -*-

# pip install Django

# tar -xvf django-1.11.8.tar.gz
# cd django-1.11.8
# (sudo) python setup.py install

# 检查是否安装成功
import django
print django.VERSION
print django.get_version()

# 四. 搭建多个互不干扰的开发环境（可选）
# 4.1 虚拟环境依赖安装
# 开发会用 virtualenv 来管理多个开发环境
# Linux/MacOS 下
# virtualenvwrapper 使得virtualenv变得更好用，所以我们一起安装了
# pip install virtualenv virtualenvwrapper
# 修改~/.bash_profile或其它环境变量相关文件(如 .bashrc 或用 ZSH 之后的 .zshrc)，添加以下语句
# export WORKON_HOME=$HOME/.virtualenvs
# export PROJECT_HOME=$HOME/svn
# source /usr/local/bin/virtualenvwrapper.sh
# 修改后使之立即生效(也可以重启终端使之生效)：
# source ~/.bash_profile

# 4.2 虚拟环境使用方法：
# mkvirtualenv zqxt：创建运行环境zqxt
# workon zqxt: 工作在 zqxt 环境 或 从其它环境切换到 zqxt 环境
# deactivate: 退出终端环境

# 其它的：
# rmvirtualenv ENV：删除运行环境ENV
# mkproject mic：创建mic项目和运行环境mic
# mktmpenv：创建临时运行环境
# lsvirtualenv: 列出可用的运行环境
# lssitepackages: 列出当前环境安装了的包
# 创建的环境是独立的，互不干扰，无需sudo权限即可使用 pip 来进行包的管理。

