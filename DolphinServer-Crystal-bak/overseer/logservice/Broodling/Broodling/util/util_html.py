# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from util.util_common import cal_avr_health_degree

TABLE_FIRST = '<table border="1" style="padding: 5px 15px 5px 5px;text-align: center; border-collapse: collapse; font-family: Arial,Helvetica,sans-serif;">'
TABLE_LAST = '</table>'

TR_TITLE_FIRST = '<tr style="background-color: #CCCCCC;">'
TR_CONTENT_FIRST = '<tr>'
TR_LAST = '</tr>'

TD_FIRST = '<td>'
TD_FIRST_RED = "<td style='color: red'>"
TD_LAST = '</td>'

BR_LINE = '</br>'

P_FIRST = '<p>'

P_LAST = '</p>'

API_NAME = 'API名称'

HIT_COUNT = '被调用次数'

ERR_COUNT = '错误次数'

ERR_CLIENT_COUNT = '客户端错误次数'

ERR_500_COUNT = '500错误次数'

ERR_502_COUNT = '502错误次数'

ERR_504_COUNT = '504错误次数'

HEALTH_DEGREE = '健康度'

AVR_HEL_DEGREE = '项目平均健康度：'

ILL_COUNT = '大于1s小于4s次数'

SICK_COUNT = '大于4s小于10s次数'

BAD_COUNT = '大于10s次数'

AVR_EXEC_TIME = '平均执行耗时(s)'

LONGEST_EXEC_TIME = '最长执行耗时(s)'

LONGEST_EXEC_TIME_NGINX = '最长完成请求耗时(s)'

TOTAL_EXEC_TIME = '总耗时(s)'

GOOGLE = 'Google'

FACEBOOK = 'Facebook'

DOLPHIN = 'Dolphin'

TOTAL = '总数'

DATE = '日期'

NEW_USER = '新增用户表'

PUSH_COUNT = 'push总数'

USER_COUNT = '用户总数'

DEVICE_COUNT = '设备总数'

ACTIVE_USER_COUNT = '活跃用户数'

OFFLINE_PUSH_COUNT = '离线push数'

AVG_DEVICE_COUNT = '用户平均设备数'

BOOKMARK_COUNT = '书签同步总数'

AVG_BOOKMARK_COUNT = '单个用户书签同步数'

MEDIAN_BOOKMARK_COUNT = '书签同步中位数'

TAB_COUNT = '标签同步总数'

AVG_TAB_COUNT = '单个用户标签同步数'

MEDIAN_TAB_COUNT = '标签同步中位数'

HISTORY_COUNT = '历史同步总数'

AVG_HISTORY_COUNT = '单个用户历史同步数'

MEDIAN_HISTORY_COUNT = '历史同步中位数'

DESKTOP_COUNT = '桌面插件同步总数'

AVG_DESKTOP_COUNT = '单个用户桌面插件同步数'

MEDIAN_DESKTOP_COUNT = '桌面插件同步中位数'

URL_NAME = "网站地址"

VIEW_COUNT = "访问次数"

CHANNEL = "Channel地址"

SUCCESS_COUNT = "成功次数"

TIMEOUT_COUNT = "超时次数"

EXCEPTION_COUNT = "异常次数"

AVR_EXEC_TIME_TRACK = '平均执行耗时(ms)'

LONGEST_EXEC_TIME_TRACK = '最长执行耗时(ms)'

CLIENT_TYPE = '客户端类型'

HOUR_RANGE = '时间范围'

HARAKIRI_COUNT = '切腹次数'

COMETD_GOOD_COUNT = '小于30ms次数'

COMETD_OK_COUNT = '大于30ms小于100ms次数'

COMETD_ILL_COUNT = '大于100ms小于300ms次数'

COMETD_SICK_COUNT = '大于300ms小于1000ms次数'

COMETD_BAD_COUNT = '大于1000ms次数'

COMETD_AVR_TIME = '平均执行耗时(ms)'

COMETD_LONGEST_TIME = '最长执行耗时(ms)'

OP_GOOD_COUNT = '小于500ms次数'

OP_ILL_COUNT = '大于500ms小于5000ms次数'

OP_BAD_COUNT = '大于5000ms次数'

COUNTRY = '国家代号'

NGINX_TIME = '后端平均耗时'

MISS_MATCH = '异常次数'

PERCENTAGE = '百分比(%)'


def get_api_table_str(log_type, datas):
    html_str = _get_title_text(log_type)
    html_str += TABLE_FIRST
    html_str += _get_api_table_title()
    for data in datas:
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1]) + TD_LAST +\
            TD_FIRST + str(data[2]) + TD_LAST +\
            TD_FIRST + str(data[3]) + TD_LAST +\
            TD_FIRST + str(data[4]) + TD_LAST +\
            TD_FIRST + str(data[5]) + TD_LAST +\
            TD_FIRST + str(data[6]) + TD_LAST +\
            TD_FIRST + str(data[7]) + TD_LAST +\
            TD_FIRST + str(data[8]) + TD_LAST +\
            TD_FIRST + str(data[9]) + TD_LAST
        html_str += TR_LAST

    html_str += TABLE_LAST
    html_str += P_FIRST + AVR_HEL_DEGREE + \
        str(cal_avr_health_degree(datas)) + P_LAST
    html_str += BR_LINE
    return html_str


def get_nginx_access_table_str(log_type, datas):
    html_str = _get_title_text(log_type)
    html_str += TABLE_FIRST
    html_str += _get_nginx_access_table_title()
    for data in datas:
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1]) + TD_LAST +\
            TD_FIRST + str(data[2]) + TD_LAST +\
            TD_FIRST + str(data[3]) + TD_LAST +\
            TD_FIRST + str(data[4]) + TD_LAST +\
            TD_FIRST + str(data[5]) + TD_LAST +\
            TD_FIRST + str(data[6]) + TD_LAST +\
            TD_FIRST + str(data[7]) + TD_LAST +\
            TD_FIRST + str(data[8]) + TD_LAST +\
            TD_FIRST + str(data[9]) + TD_LAST +\
            TD_FIRST + str(data[10]) + TD_LAST +\
            TD_FIRST + str(data[11]) + TD_LAST +\
            TD_FIRST + str(data[12]) + TD_LAST +\
            TD_FIRST + str(data[13]) + TD_LAST +\
            TD_FIRST + str(data[14]) + TD_LAST
        html_str += TR_LAST

    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_api_table_title():
    return TR_TITLE_FIRST + TD_FIRST + API_NAME + TD_LAST +\
        TD_FIRST + HIT_COUNT + TD_LAST +\
        TD_FIRST + ERR_COUNT + TD_LAST +\
        TD_FIRST + ILL_COUNT + TD_LAST +\
        TD_FIRST + SICK_COUNT + TD_LAST +\
        TD_FIRST + BAD_COUNT + TD_LAST +\
        TD_FIRST + AVR_EXEC_TIME + TD_LAST +\
        TD_FIRST + LONGEST_EXEC_TIME + TD_LAST +\
        TD_FIRST + TOTAL_EXEC_TIME + TD_LAST +\
        TD_FIRST + HEALTH_DEGREE + TD_LAST + TR_LAST


def _get_nginx_access_table_title():
    return TR_TITLE_FIRST + TD_FIRST + API_NAME + TD_LAST +\
        TD_FIRST + CLIENT_TYPE + TD_LAST +\
        TD_FIRST + HIT_COUNT + TD_LAST +\
        TD_FIRST + ERR_COUNT + TD_LAST +\
        TD_FIRST + ERR_CLIENT_COUNT + TD_LAST +\
        TD_FIRST + ERR_500_COUNT + TD_LAST +\
        TD_FIRST + ERR_502_COUNT + TD_LAST +\
        TD_FIRST + ERR_504_COUNT + TD_LAST + \
        TD_FIRST + ILL_COUNT + TD_LAST +\
        TD_FIRST + SICK_COUNT + TD_LAST +\
        TD_FIRST + BAD_COUNT + TD_LAST +\
        TD_FIRST + AVR_EXEC_TIME + TD_LAST +\
        TD_FIRST + LONGEST_EXEC_TIME_NGINX + TD_LAST +\
        TD_FIRST + TOTAL_EXEC_TIME + TD_LAST +\
        TD_FIRST + HEALTH_DEGREE + TD_LAST + TR_LAST


def _get_user_id_table_title():
    return TR_TITLE_FIRST + TD_FIRST + DATE + TD_LAST +\
        TD_FIRST + GOOGLE + TD_LAST +\
        TD_FIRST + FACEBOOK + TD_LAST +\
        TD_FIRST + DOLPHIN + TD_LAST +\
        TD_FIRST + TOTAL + TD_LAST + TR_LAST


def get_user_id_table_str(datas, table_name):
    html_str = _get_title_text(table_name)
    html_str += TABLE_FIRST
    html_str += _get_user_id_table_title()
    for data in datas:
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1].get("google")) + TD_LAST +\
            TD_FIRST + str(data[1].get("facebook")) + TD_LAST +\
            TD_FIRST + str(data[1].get("dolphin")) + TD_LAST +\
            TD_FIRST + str(data[1].get("total")) + TD_LAST
        html_str += TR_LAST
    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_push_server_table_title():
    return TR_TITLE_FIRST + TD_FIRST + DATE + TD_LAST +\
        TD_FIRST + PUSH_COUNT + TD_LAST +\
        TD_FIRST + USER_COUNT + TD_LAST +\
        TD_FIRST + DEVICE_COUNT + TD_LAST +\
        TD_FIRST + AVG_DEVICE_COUNT + TD_LAST +\
        TD_FIRST + OFFLINE_PUSH_COUNT + TD_LAST +\
        TD_FIRST + ACTIVE_USER_COUNT + TD_LAST + TR_LAST


def get_push_server_table_str(datas, table_name):
    html_str = _get_title_text(table_name)
    html_str += TABLE_FIRST
    html_str += _get_push_server_table_title()
    for data in datas:
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1].get("push_count")) + TD_LAST +\
            TD_FIRST + str(data[1].get("user_count")) + TD_LAST +\
            TD_FIRST + str(data[1].get("device_count")) + TD_LAST +\
            TD_FIRST + str(data[1].get("avg_device_count")) + TD_LAST +\
            TD_FIRST + str(data[1].get("offline_push_count")) + TD_LAST +\
            TD_FIRST + str(data[1].get("active_user_count")) + TD_LAST
        html_str += TR_LAST
    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_sync_table_title():
    return TR_TITLE_FIRST + TD_FIRST + DATE + TD_LAST +\
        TD_FIRST + USER_COUNT + TD_LAST +\
        TD_FIRST + BOOKMARK_COUNT + TD_LAST +\
        TD_FIRST + AVG_BOOKMARK_COUNT + TD_LAST +\
        TD_FIRST + MEDIAN_BOOKMARK_COUNT + TD_LAST +\
        TD_FIRST + TAB_COUNT + TD_LAST +\
        TD_FIRST + AVG_TAB_COUNT + TD_LAST +\
        TD_FIRST + MEDIAN_TAB_COUNT + TD_LAST +\
        TD_FIRST + HISTORY_COUNT + TD_LAST +\
        TD_FIRST + AVG_HISTORY_COUNT + TD_LAST +\
        TD_FIRST + MEDIAN_HISTORY_COUNT + TD_LAST +\
        TD_FIRST + DESKTOP_COUNT + TD_LAST +\
        TD_FIRST + AVG_DESKTOP_COUNT + TD_LAST +\
        TD_FIRST + MEDIAN_DESKTOP_COUNT + TD_LAST + TR_LAST


def get_sync_table_str(datas, table_name):
    html_str = _get_title_text(table_name)
    html_str += TABLE_FIRST
    html_str += _get_sync_table_title()
    for data in datas:
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1].get("total_user")) + TD_LAST +\
            TD_FIRST + str(data[1].get("bookmark").get("total")) + TD_LAST +\
            TD_FIRST + str(data[1].get("bookmark").get("avg")) + TD_LAST +\
            TD_FIRST + str(data[1].get("bookmark").get("median")) + TD_LAST +\
            TD_FIRST + str(data[1].get("tab").get("total")) + TD_LAST +\
            TD_FIRST + str(data[1].get("tab").get("avg")) + TD_LAST +\
            TD_FIRST + str(data[1].get("tab").get("median")) + TD_LAST +\
            TD_FIRST + str(data[1].get("history").get("total")) + TD_LAST +\
            TD_FIRST + str(data[1].get("history").get("avg")) + TD_LAST +\
            TD_FIRST + str(data[1].get("history").get("median")) + TD_LAST +\
            TD_FIRST + str(data[1].get("desktop").get("total")) + TD_LAST +\
            TD_FIRST + str(data[1].get("desktop").get("avg")) + TD_LAST +\
            TD_FIRST + str(data[1].get("desktop").get("median")) + TD_LAST
        html_str += TR_LAST
    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_sync_site_statistics_title():
    return TR_TITLE_FIRST + TD_FIRST + URL_NAME + TD_LAST +\
        TD_FIRST + VIEW_COUNT + TD_LAST + TR_LAST


def get_sync_site_statistics_table_str(datas, table_name):
    html_str = _get_title_text(table_name)
    html_str += TABLE_FIRST
    html_str += _get_sync_site_statistics_title()
    for data in datas:
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1]) + TD_LAST
        html_str += TR_LAST
    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_uwsgi_hariki_title():
    return TR_TITLE_FIRST + TD_FIRST + HOUR_RANGE + TD_LAST +\
        TD_FIRST + API_NAME + TD_LAST +\
        TD_FIRST + HARAKIRI_COUNT + TD_LAST + TR_LAST


def get_uwsgi_hariki_table_str(data_map, date_str, count):
    html_str = _get_title_text('UWSGI_HARAKIRI ' + date_str)
    html_str += TABLE_FIRST
    html_str += _get_uwsgi_hariki_title()
    item = data_map.keys()
    item.sort()
    for hour in item:
        for name in data_map[hour]:
            html_str += TR_CONTENT_FIRST
            html_str += TD_FIRST + hour + ':00:00-' + hour + ':59:59' + TD_LAST +\
                TD_FIRST + name + TD_LAST +\
                TD_FIRST + str(data_map[hour][name]) + TD_LAST
            html_str += TR_LAST
    html_str += TR_CONTENT_FIRST
    html_str += TD_FIRST + '00:00:00-23:59:59' + TD_LAST +\
        TD_FIRST + '总计' + TD_LAST +\
        TD_FIRST + str(count) + TD_LAST
    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_operation_nginx_title():
    return TR_TITLE_FIRST + TD_FIRST + COUNTRY + TD_LAST +\
        TD_FIRST + HIT_COUNT + TD_LAST +\
        TD_FIRST + ERR_COUNT + TD_LAST +\
        TD_FIRST + ERR_CLIENT_COUNT + TD_LAST +\
        TD_FIRST + OP_GOOD_COUNT + TD_LAST +\
        TD_FIRST + OP_ILL_COUNT + TD_LAST +\
        TD_FIRST + OP_BAD_COUNT + TD_LAST +\
        TD_FIRST + AVR_EXEC_TIME + TD_LAST +\
        TD_FIRST + LONGEST_EXEC_TIME + TD_LAST +\
        TD_FIRST + TOTAL_EXEC_TIME + TD_LAST +\
        TD_FIRST + NGINX_TIME + TD_LAST +\
        TD_FIRST + HEALTH_DEGREE + TD_LAST + TR_LAST


def get_operation_nginx_table_str(datas, date_str):
    html_str = _get_title_text(
        'OPERATION_NGINX /api/2/provision.json ' + date_str)
    html_str += TABLE_FIRST
    html_str += _get_operation_nginx_title()
    vip_list = ["BR", "AE", "RU", "IN", "ID", "CN", "TW", "HK",
                "EG", "SA", "AR", "MX", "TR", "VN", "MY", "PH", "TH"]
    for data in datas:
        country = data.get("country")
        if country[-2:] in vip_list:
            html_str += TR_CONTENT_FIRST
            html_str += TD_FIRST_RED + str(data.get("country")) + TD_LAST +\
                TD_FIRST + str(data.get("count")) + TD_LAST +\
                TD_FIRST + str(data.get("srv_err_count")) + TD_LAST +\
                TD_FIRST + str(data.get("cli_err_count")) + TD_LAST +\
                TD_FIRST + str(data.get("good_count")) + TD_LAST +\
                TD_FIRST + str(data.get("ill_count")) + TD_LAST +\
                TD_FIRST + str(data.get("bad_count")) + TD_LAST +\
                TD_FIRST + str(data.get("avr_time")) + TD_LAST +\
                TD_FIRST + str(data.get("max_time")) + TD_LAST +\
                TD_FIRST + str(data.get("total_time")) + TD_LAST +\
                TD_FIRST + str(data.get("nginx_avr_time")) + TD_LAST +\
                TD_FIRST + str(data.get("health_degree")) + TD_LAST
            html_str += TR_LAST
    for data in datas:
        country = data.get("country")
        if country[-2:] not in vip_list:
            html_str += TR_CONTENT_FIRST
            html_str += TD_FIRST + str(data.get("country")) + TD_LAST +\
                TD_FIRST + str(data.get("count")) + TD_LAST +\
                TD_FIRST + str(data.get("srv_err_count")) + TD_LAST +\
                TD_FIRST + str(data.get("cli_err_count")) + TD_LAST +\
                TD_FIRST + str(data.get("good_count")) + TD_LAST +\
                TD_FIRST + str(data.get("ill_count")) + TD_LAST +\
                TD_FIRST + str(data.get("bad_count")) + TD_LAST +\
                TD_FIRST + str(data.get("avr_time")) + TD_LAST +\
                TD_FIRST + str(data.get("max_time")) + TD_LAST +\
                TD_FIRST + str(data.get("total_time")) + TD_LAST +\
                TD_FIRST + str(data.get("nginx_avr_time")) + TD_LAST +\
                TD_FIRST + str(data.get("health_degree")) + TD_LAST
            html_str += TR_LAST
    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_pushserver_cometd_title():
    return TR_TITLE_FIRST + TD_FIRST + API_NAME + TD_LAST +\
        TD_FIRST + HIT_COUNT + TD_LAST +\
        TD_FIRST + COMETD_GOOD_COUNT + TD_LAST +\
        TD_FIRST + COMETD_OK_COUNT + TD_LAST +\
        TD_FIRST + COMETD_ILL_COUNT + TD_LAST +\
        TD_FIRST + COMETD_SICK_COUNT + TD_LAST +\
        TD_FIRST + COMETD_BAD_COUNT + TD_LAST +\
        TD_FIRST + COMETD_LONGEST_TIME + TD_LAST +\
        TD_FIRST + COMETD_AVR_TIME + TD_LAST +\
        TD_FIRST + HEALTH_DEGREE + TD_LAST + TR_LAST


def get_pushserver_cometd_table_str(datas, date_str):
    html_str = _get_title_text('PUSHSERVER_COMETD ' + date_str)
    html_str += TABLE_FIRST
    html_str += _get_pushserver_cometd_title()
    for data in datas:
        count = data[1]
        ok_count = data[3]
        ill_count = data[4]
        sick_count = data[5]
        bad_count = data[6]
        health_degree = round(((count - bad_count * 0.8 - sick_count * 0.6 -
                                ill_count * 0.4 - ok_count * 0.2) / count * 100), 3)
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1]) + TD_LAST +\
            TD_FIRST + str(data[2]) + TD_LAST +\
            TD_FIRST + str(data[3]) + TD_LAST +\
            TD_FIRST + str(data[4]) + TD_LAST +\
            TD_FIRST + str(data[5]) + TD_LAST +\
            TD_FIRST + str(data[6]) + TD_LAST +\
            TD_FIRST + str(data[7]) + TD_LAST +\
            TD_FIRST + str(data[8]) + TD_LAST +\
            TD_FIRST + str(health_degree) + TD_LAST
        html_str += TR_LAST

    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_provision_missmatch_title():
    return TR_TITLE_FIRST + TD_FIRST + COUNTRY + TD_LAST +\
        TD_FIRST + TOTAL + TD_LAST +\
        TD_FIRST + MISS_MATCH + TD_LAST +\
        TD_FIRST + PERCENTAGE + TD_LAST + TR_LAST


def get_provision_missmatch_table_str(datas, date_str):
    html_str = _get_title_text('PROVISION_MISSMATCH ' + date_str)
    html_str += TABLE_FIRST
    html_str += _get_provision_missmatch_title()
    for data in datas:
        count = data[1]
        miss_count = data[2]
        percent = round((float(miss_count) / count * 100), 3)
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1]) + TD_LAST +\
            TD_FIRST + str(data[2]) + TD_LAST +\
            TD_FIRST + str(percent) + TD_LAST
        html_str += TR_LAST

    html_str += TABLE_LAST
    html_str += BR_LINE
    return html_str


def _get_title_text(title):
    return '<h2>%s</h2>' % title


def get_image_tag(image_name):
    return '<img src="cid:image_%s" />' % image_name
