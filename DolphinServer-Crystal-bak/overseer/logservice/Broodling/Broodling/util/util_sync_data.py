#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
from util_mysql import MySql_Conn
from util_common import get_table_name, get_date_str, get_yesterday
from util_log import logger
from util_html import get_sync_table_str
from util_mail import initial_mail_info, send_email
import setting

result_map = {}

_sync_db_conn_test = MySql_Conn.new(
    'localhost', 'root', '123456', 'dolphin_stat', 3306)

_sync_db_conn = MySql_Conn.new(setting.MYSQL_SETTING['host'],
                               setting.MYSQL_SETTING['username'],
                               setting.MYSQL_SETTING['password'],
                               setting.MYSQL_SETTING['dbname'],
                               setting.MYSQL_SETTING['port'])


def get_sync_count_by_day(date):
    global result_map
    day_result = {"total_user": 0,
                  "bookmark": {"total": 0, "avg": 0.0, "median": 0},
                  "history": {"total": 0, "avg": 0.0, "median": 0},
                  "tab": {"total": 0, "avg": 0.0, "median": 0},
                  "desktop": {"total": 0, "avg": 0.0, "user": 0, "median": 0}}

    table_name = get_table_name("DolphinPushServer_core_push_sync", date)
    query_str = 'select push_type,count(distinct user_id),sum(times) from %s group by push_type' % table_name
    query_total_user = 'select count(distinct user_id) from %s' % table_name
    query_total_count = 'select count(*) from %s group by push_type order by push_type' % table_name

    if _sync_db_conn:
        query_result = _sync_db_conn.query_sql(query_str)
        total_count = _sync_db_conn.query_sql(query_total_count)
        if query_result:
            for item in query_result:
                if item[0] == 1:
                    day_result["bookmark"]["total"] = item[2]
                    day_result["bookmark"]["avg"] = round(
                        float(item[2]) / item[1], 3)
                    mid_count = int(total_count[0][0] - 1) / 2
                    query_median = 'select times from %s where push_type=1 order by times limit %d,1' % (
                        table_name, mid_count)
                    median = _sync_db_conn.query_sql(query_median)
                    day_result["bookmark"]["median"] = int(median[0][0])
                elif item[0] == 2:
                    day_result["tab"]["total"] = item[2]
                    day_result["tab"]["avg"] = round(
                        float(item[2]) / item[1], 3)
                    mid_count = int(total_count[1][0] - 1) / 2
                    query_median = 'select times from %s where push_type=2 order by times limit %d,1' % (
                        table_name, mid_count)
                    median = _sync_db_conn.query_sql(query_median)
                    day_result["tab"]["median"] = int(median[0][0])
                elif item[0] == 4:
                    day_result["history"]["total"] = item[2]
                    day_result["history"]["avg"] = round(
                        float(item[2]) / item[1], 3)
                    mid_count = int(total_count[2][0] - 1) / 2
                    query_median = 'select times from %s where push_type=4 order by times limit %d,1' % (
                        table_name, mid_count)
                    median = _sync_db_conn.query_sql(query_median)
                    day_result["history"]["median"] = int(median[0][0])
                elif item[0] == 64 or item[0] == 128:
                    day_result["desktop"]["total"] += item[2]
                    day_result["desktop"]["user"] += item[1]
                    mid_count = int(
                        total_count[3][0] + total_count[4][0] - 1) / 2
                    query_median = 'select times from %s where push_type=64 or push_type=128 order by times limit %d,1' % (
                        table_name, mid_count)
                    median = _sync_db_conn.query_sql(query_median)
                    day_result["desktop"]["median"] = int(median[0][0])
            if day_result["desktop"]["user"] != 0:
                day_result["desktop"]["avg"] = round(
                    float(day_result["desktop"]["total"]) / day_result["desktop"]["user"], 3)

            query_result = _sync_db_conn.query_sql(query_total_user)
            if query_result:
                day_result['total_user'] = query_result[0][0]

    # print day_result
    date_str = get_date_str(date)
    result_map[date_str] = day_result
    return day_result


def get_sync_data_by_month(date):
    temp_day = date
    global result_map
    for i in range(7):
        get_sync_count_by_day(temp_day)
        temp_day -= timedelta(1)
    items = result_map.items()
    items.sort(reverse=True)
    return items


def get_sync_data_html(datas):
    html = get_sync_table_str(datas, "Push_Sync数据表")
    return html


if __name__ == "__main__":
    datas = get_sync_data_by_month(datetime.now() - timedelta(12))
    # datas = list(datas)
    # print datas
    html = get_sync_data_html(datas)
    # for data in datas:
    #     print data[1].get("tab").get("total")
    print html
