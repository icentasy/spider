#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import MySQLdb
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
from util_mysql import MySql_Conn
from util_common import get_table_name, get_date_str, get_yesterday
from util_log import logger
from util_html import get_uwsgi_hariki_table_str
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


def get_uwsgi_hariki(date):
    date_str = get_date_str(date)
    table_name = get_table_name('Uwsgi_hariki', date)
    data_sql_str = "select api_name, hariki_time from %s order by hariki_time, api_name" % table_name
    count_sql_str = "select count(*) from %s" % table_name
    datas = _db_conn.query_sql(data_sql_str)
    count = _db_conn.query_sql(count_sql_str)
    data_map = {}
    for name, time in datas:
        time_list = re.split('[: ]', time)
        if time_list[2]:
            hour = time_list[3]
        else:
            hour = time_list[4]
        if data_map.has_key(hour):
            if data_map[hour].has_key(name):
                data_map[hour][name] += 1
            else:
                data_map[hour][name] = 1
        else:
            data_map[hour] = {}
            data_map[hour][name] = 1
    return data_map, count[0][0]


def get_uwsgi_hariki_html(date):
    html_str = ""
    date_str = get_date_str(date)
    data_map, count = get_uwsgi_hariki(date)
    html_str += get_uwsgi_hariki_table_str(data_map, date_str, count)
    return html_str

if __name__ == "__main__":
        # result = (datetime.now()-timedelta(3))
    html = get_uwsgi_hariki_html(datetime.now())
    print html
