#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
from util_mysql import MySql_Conn
from util_common import get_table_name, get_date_str, get_yesterday
from util_log import logger
from util_html import get_push_server_table_str
from util_mail import initial_mail_info, send_email
import setting

user_device_count = {}
result_table = {}

_push_db_conn_test = MySql_Conn.new(
    'localhost', 'root', '123456', 'dolphin_stat', 3306)

_push_db_conn = MySql_Conn.new(setting.MYSQL_SETTING['host'],
                               setting.MYSQL_SETTING['username'],
                               setting.MYSQL_SETTING['password'],
                               setting.MYSQL_SETTING['dbname'],
                               setting.MYSQL_SETTING['port'])


def get_push_statistics(date):

    date_suffix = get_date_str(date)
    table_name = "DolphinPushServer_core_push_push_" + date_suffix
    query_user_count = "select count(distinct user_id) from %s where src_did not like 'TRY%%'" % table_name
    query_push_count = "select count(*) from %s where src_did not like 'TRY%%'" % table_name
    query_userids = "select distinct user_id from %s where src_did not like 'TRY%%'" % table_name
    global result_table
    if _push_db_conn:
        try:
            user_count = _push_db_conn.query_sql(query_user_count)[0][0]
            push_count = _push_db_conn.query_sql(query_push_count)[0][0]
        except Exception, e:
            user_count = 0
            push_count = 0
        result_table.setdefault(date_suffix, {})["user_count"] = user_count
        current_table = result_table[date_suffix]

        current_table["push_count"] = push_count

        device_count = 0
        user_ids = _push_db_conn.query_sql(query_userids)
        try:
            for user_id in user_ids:
                device_count += get_user_device_count(user_id[0])
        except Exception, e:
            print e
            pass
        current_table["device_count"] = device_count
        try:
            if user_count > 0:
                current_table["avg_device_count"] = round(
                    float(device_count) / user_count, 3)
        except Exception, e:
            logger.error("wrong in avg_device_count %s" % e)
            print e
        current_table["active_user_count"] = get_push_active_count(date)
        current_table["offline_push_count"] = get_offline_push_count(date)


def get_push_data_by_month(date):
    temp_day = date
    global reuslt_table
    for i in range(7):
        get_push_statistics(temp_day)
        temp_day -= timedelta(1)
    items = result_table.items()
    items.sort(reverse=True)
    return items


def get_user_device_count(user_id):
    global user_device_count
    if user_id in user_device_count:
        return user_device_count[user_id]

    _device_db = MySql_Conn.new(
        "10.159.9.221", "push", "P@55word", "push", 3306)
    query_device_count = "select count(did) from device where uid=%s" % str(
        user_id)
    # print query_device_count
    try:
        device_count = _device_db.query_sql(query_device_count)[0][0]
    except Exception, e:
        device_count = 0
    user_device_count[user_id] = device_count

    return device_count


def get_push_active_count(date):
    date_suffix = get_date_str(date)
    table_name = "DolphinPushServer_core_handshake_" + date_suffix
    query_count = " select count(distinct device_id) from %s" % table_name

    if _push_db_conn:
        try:
            active_user_count = _push_db_conn.query_sql(query_count)[0][0]
        except Exception, e:
            active_user_count = "暂无数据"
    return active_user_count


def get_offline_push_count(date):
    date_suffix = get_date_str(date)
    table_name = "DolphinPushServer_core_push_offline_" + date_suffix
    query_count = " select count(*) from %s" % table_name

    if _push_db_conn:
        try:
            offline_push_count = _push_db_conn.query_sql(query_count)[0][0]
        except Exception, e:
            offline_push_count = "暂无数据"
    return offline_push_count


def get_push_data_html(datas):
    html = get_push_server_table_str(datas, "PushServer数据表")
    return html

if __name__ == "__main__":
    result = get_push_data_by_month(datetime.now() - timedelta(3))
    html = get_push_data_html(result)
    print html
