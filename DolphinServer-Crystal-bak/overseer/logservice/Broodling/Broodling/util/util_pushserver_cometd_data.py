#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
from util_mysql import MySql_Conn
from util_common import get_table_name, get_date_str, get_yesterday
from util_log import logger
from util_html import get_pushserver_cometd_table_str
import setting

user_device_count = {}
result_table = {}

_db_conn_test = MySql_Conn.new(
    'localhost', 'root', '123456', 'dolphin_stat', 3306)

_db_conn = MySql_Conn.new(setting.MYSQL_SETTING['host'],
                          setting.MYSQL_SETTING['username'],
                          setting.MYSQL_SETTING['password'],
                          setting.MYSQL_SETTING['dbname'],
                          setting.MYSQL_SETTING['port'])


def get_pushserver_cometd(date):
    date_str = get_date_str(date)
    table_name = get_table_name('DolphinPushServer_core_cometd', date)
    sql_str = "select api_name, count, good_count, ok_count, ill_count, sick_count, bad_count,\
    longest_exec_time, avr_exec_time from %s order by api_name" % table_name
    datas = _db_conn.query_sql(sql_str)
    return datas


def get_pushserver_cometd_html(date):
    html_str = ""
    date_str = get_date_str(date)
    datas = get_pushserver_cometd(date)
    html_str += get_pushserver_cometd_table_str(datas, date_str)
    return html_str

if __name__ == "__main__":
        # result = (datetime.now()-timedelta(3))
    html = get_pushserver_cometd_html(datetime.now())
    print html
