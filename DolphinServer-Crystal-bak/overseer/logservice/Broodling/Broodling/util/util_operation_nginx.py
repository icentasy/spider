#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import MySQLdb
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
from util_mysql import MySql_Conn
from util_common import get_table_name, get_date_str, get_yesterday
from util_log import logger
from util_html import get_operation_nginx_table_str, get_image_tag
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


def get_operation_nginx(date):
    date_str = get_date_str(date)
    table_name = get_table_name('DolphinOPService_nginx', date)
    data_sql_str = "select locale from %s where api_name='/api/2/provision.json'" % table_name
    datas = _db_conn.query_sql(data_sql_str)
    items = json.loads(datas[0][0])
    data_list = []
    for item in items:
        data_dict = {}
        count = items[item].get("count")
        srv_err_count = items[item].get("srv_err_count")
        ill_count = items[item].get("ill_count")
        bad_count = items[item].get("bad_count")
        data_dict["country"] = item
        data_dict["count"] = count
        data_dict["srv_err_count"] = srv_err_count
        data_dict["cli_err_count"] = items[item].get("cli_err_count")
        data_dict["good_count"] = items[item].get("good_count")
        data_dict["ill_count"] = ill_count
        data_dict["bad_count"] = bad_count
        data_dict["avr_time"] = round((float(items[item].get("total_time")) / count), 3)
        data_dict["max_time"] = items[item].get("max_time")
        data_dict["total_time"] = items[item].get("total_time")
        data_dict["nginx_avr_time"] = round((float(items[item].get("nginx_total_time", 0)) / count), 3)
        data_dict["health_degree"] = round(((count - srv_err_count * 1 - bad_count *
                                             0.8 - ill_count * 0.2) / count * 100), 3)
        data_list.append(data_dict)
    data_list = sorted(data_list, key=lambda x: x['avr_time'], reverse=True)
    return data_list


def get_operation_nginx_html(date):
    html_str = ""
    date_str = get_date_str(date)
    datas = get_operation_nginx(date)
    html_str += get_operation_nginx_table_str(datas, date_str)
    return html_str

if __name__ == "__main__":
        # result = (datetime.now()-timedelta(3))
    html = get_operation_nginx_html(datetime.now())
    print html
