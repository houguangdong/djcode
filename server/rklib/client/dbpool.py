#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/30 10:24

"""
* dbapi ：数据库接口
* mincached ：启动时开启的空连接数量
* maxcached ：连接池最大可用连接数量
* maxshared ：连接池最大可共享连接数量
* maxconnections ：最大允许连接数量
* blocking ：达到最大数量时是否阻塞
* maxusage ：单个连接最大复用次数
* setsession ：用于传递到数据库的准备会话，如 [”set name UTF-8″] 。
"""

try:
    import pymysql as MySQLdb
    _pymysql = True
except ImportError, e:
    import MySQLdb
    _pymysql = False

# from DBUtils.PooledDB import PooledDB
from DBUtils.PersistentDB import PersistentDB

DBCS = {'mysql': MySQLdb}


class DBPool(object):
    """数据库连接池
    """

    def __init__(self):
        self._pymysql = _pymysql

    def initPool(self, **kw):
        '''
        根据连接配置初始化连接池配置信息.
        aa = {'host':"localhost",'user':'root','passwd':'111','db':'test','port':3306,'charset':'utf8'}
        dbpool.initPool(**aa)
        :param kw:
        :return:
        '''
        self.config = kw
        creator = DBCS.get(kw.get('engine', 'mysql'), MySQLdb)
        # self.pool = PooledDB(creator, mincached=1, maxcached=10, maxshared=15, maxconnections=20, **kw)
        self.pool = PersistentDB(creator, **kw)

    def connection(self):
        return self.pool.connection()


# dbpool = DBPool()

dbpools = {}