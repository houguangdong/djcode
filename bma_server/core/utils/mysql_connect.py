# -*- coding:utf-8 -*-
import pymysql


def get_mysql_conn(mysql_conn_info, server_id):
    """
    数据库链接
    """
    if not mysql_conn_info.get(server_id, None):
        return None
    try:
        mysql_conn = pymysql.connect(**mysql_conn_info[server_id]["mysql"])
    except pymysql.OperationalError as e:
        return None
    return mysql_conn.cursor()