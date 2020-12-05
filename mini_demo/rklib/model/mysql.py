#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/29 11:16

import hashlib
import sys
import datetime
import pymysql

# import MySQLdb

escape_string = pymysql.converters.escape_string

# escape_string = MySQLdb.escape_string

from rklib.model.engine import StorageEngine
from rklib.utils.encoding import force_str
from rklib.client.mysql import Connection


def _smart(v):
    t = type(v)
    if t == str:
        return v
    elif t == unicode:
        return force_str(v)
    elif (t == int) or (t == long) or (t == float):
        return str(v)
    elif t == datetime.datetime:
        return v.strftime("%Y-%m-%d %H:%M:%S")
    return str(v)


def _pairtext(k, v):
    if v is None:
        return "%s=null" % k
    return "%s='%s'" % (k, escape_string(_smart(v)))


def _sqltext(data, delimiter=","):
    sql = delimiter.join([_pairtext(k[0], k[1]) for k in data.items()])
    return sql


class MysqlEngine(StorageEngine):

    def __init__(self):
        self.servers = None
        self.table = {}
        self.sharding = None
        self.debug = False

    def configure(self, cfg_value):
        StorageEngine.configure(self, cfg_value)
        self.servers = cfg_value["servers"]
        self.sharding = {}
        for i_range in cfg_value["sharding"]:
            server_index = cfg_value["sharding"][i_range]
            for i in range(i_range[0], i_range[1] + 1):
                self.sharding[hex(i)[2:].zfill(2)] = server_index

        self.table = {}
        for i_range in cfg_value["table"]:
            table_index = cfg_value["table"][i_range]
            for i in range(i_range[0], i_range[1] + 1):
                self.table[hex(i)[2:].zfill(1)] = table_index

        self.debug = cfg_value.get("debug", False)

        # print self.sharding, self.table, self.debug, '111111111'

        from rklib.client.dbpool import DBPool
        from rklib.client.dbpool import dbpools

        db_names = list(set(self.sharding.values()))
        db_names.append('master')

        print db_names
        for i in db_names:
            host, user, passwd, database = self.servers.get(i)
            print host, user, passwd, database
            kwargs = {
                'host': host.split(":")[0],
                'port': int(host.split(":")[1]),
                'user': user,
                'passwd': passwd,
                'db': database,
                'setsession': ['SET AUTOCOMMIT = 1'],
                'charset': 'utf8mb4'
            }

            dbpool = DBPool()
            dbpool.initPool(**kwargs)
            dbpools[i] = dbpool

    def get_data(self, model_cls, pkey):
        return self._select(model_cls, pkey)

    def put_data(self, model_cls, pkey, data, create_new):
        if create_new:
            self._insert(model_cls, pkey, data)
        else:
            self._update(model_cls, pkey, data)

    def delete_data(self, model_cls, pkey):
        self._delete(model_cls, pkey)

    def _insert(self, model_cls, pkey, data):
        conn, table = self._get_connection_info(model_cls, pkey)
        try:
            import binascii
            sql = "INSERT INTO %s SET %s" % (table, _sqltext(data, ","))
            if self.debug:
                print >> sys.stderr, "[DEBUG]", "host:", conn._db_args["host"], \
                    "port:", conn._db_args["port"], "db:", conn._db_args["db"]
                print >> sys.stderr, "[DEBUG]", sql
            last_id = conn.execute(sql)
            return last_id
        except Exception, e:
            import traceback
            traceback.print_exc()
        finally:
            conn.close()

    def _update(self, model_cls, pkey, data):
        conn, table = self._get_connection_info(model_cls, pkey)
        try:
            import time
            start = time.time()
            sql = "UPDATE %s SET %s WHERE %s='%s'" % (table, _sqltext(data, ","), model_cls.pkey_field, escape_string(_smart(pkey)))
            if self.debug:
                print >> sys.stderr, "[DEBUG]", "host:", conn._db_args["host"], \
                    "port:", conn._db_args["port"], "db:", conn._db_args["db"]
                print >> sys.stderr, "[DEBUG]", sql
            conn.execute(sql)
            print((time.time() - start) * 1000, "update mysql time", table)
        finally:
            conn.close()

    def _select(self, model_cls, pkey):
        conn, table = self._get_connection_info(model_cls, pkey)
        try:
            sql = "SELECT * FROM %s WHERE %s='%s'" % (table, model_cls.pkey_field, escape_string(_smart(pkey)))
            if self.debug:
                print >> sys.stderr, "[DEBUG]", "host:", conn._db_args["host"], \
                    "port:", conn._db_args["port"], "db:", conn._db_args["db"]
                print >> sys.stderr, "[DEBUG]", sql
            return conn.get(sql)
        finally:
            conn.close()

    def _delete(self, model_cls, pkey):
        conn, table = self._get_connection_info(model_cls, pkey)
        try:
            sql = "DELETE FROM %s WHERE %s='%s'" % (table, model_cls.pkey_field, escape_string(_smart(pkey)))
            if self.debug:
                print >> sys.stderr, "[DEBUG]", "host:", conn._db_args["host"], \
                    "port:", conn._db_args["port"], "db:", conn._db_args["db"]
                print >> sys.stderr, "[DEBUG]", sql
            conn.execute(sql)
        finally:
            conn.close()

    def _get_connection_info(self, model_cls, pkey):
        if not model_cls.is_multi:      # 单表
            host, user, passwd, database = self.servers.get("master")
            table = model_cls.table
            db_name = 'master'
        else:
            shard_index, table_index = self._get_shard_info(pkey)
            host, user, passwd, database = self.servers.get(self.sharding[shard_index])
            table = "%s_%s" % (model_cls.table, self.table[table_index])
            db_name = self.sharding[shard_index]

        return Connection(host, database, user, passwd, db_name), table

    def _get_shard_info(self, shard_key):
        m = hashlib.md5()
        m.update(force_str(shard_key))
        digest = m.hexdigest()
        return digest[:2], digest[-1]

    def _get_master_connection(self):
        """获得主库的Connection实例"""
        host, user, passwd, database = self.servers.get("master")
        return Connection(host, database, user, passwd, "master")

    def master_query(self, query, *parameters):
        """主库query"""
        conn = self._get_master_connection()
        try:
            return conn.query(query, *parameters)
        finally:
            conn.close()

    def master_get(self, query, *parameters):
        """主库get"""
        conn = self._get_master_connection()
        try:
            return conn.get(query, *parameters)
        finally:
            conn.close()

    def master_execute(self, query, *parameters):
        """主库execute"""
        conn = self._get_master_connection()
        try:
            return conn.execute(query, *parameters)
        finally:
            conn.close()