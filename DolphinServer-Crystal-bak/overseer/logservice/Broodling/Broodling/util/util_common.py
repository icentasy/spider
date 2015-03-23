import datetime
import time
import os
from util.util_log import logger

today = datetime.datetime.utcnow()
last_update = int(time.time())


def init_time():
    global today, last_update
    today = datetime.datetime.now()
    last_update = int(time.time())


def get_table_name(prefix, date):
    date_str = get_date_str(date)
    return "%s_%s" % (prefix, date_str)


def get_nginx_access_table_name(date):
    date_str = get_date_str(date)
    return "Nginx_access_%s" % date_str


def get_today():
    global today
    today = datetime.datetime.now()
    return today


def get_date_str(date):
    year = str(date.year)
    month = str(date.month) if date.month > 9 else "0" + str(date.month)
    day = str(date.day) if date.day > 9 else "0" + str(date.day)
    date_str = ('%s-%s-%s' % (year, month, day)).replace('-', '')
    return date_str


def get_date_str_ex(date):
    year = str(date.year)
    month = str(date.month) if date.month > 9 else "0" + str(date.month)
    day = str(date.day) if date.day > 9 else "0" + str(date.day)
    date_str = '%s-%s-%s' % (year, month, day)
    return date_str


def get_yesterday():
    today = get_today()
    return today - datetime.timedelta(days=1)


def compare_date(now_date, old_date):
    if now_date.year > old_date.year or (now_date.year == old_date.year and now_date.month > old_date.month)\
            or (now_date.year == old_date.year and now_date.month == old_date.month and now_date.day > old_date.day):
        return True
    return False


def is_update_time():
    global last_update
    now_time = int(time.time())
    if (now_time - last_update) >= 60:
        logger.debug("update record time comes!")
        last_update = now_time
        return True
    return False


def is_submit_time(submit_flag=[True]):
    now_date = datetime.datetime.now()
    if submit_flag[0] and now_date.hour == 0 and now_date.minute == 0:
        logger.debug("is submit time!")
        submit_flag[0] = False
        return True
    elif now_date.hour !=  0 or now_date.minute != 0:
        submit_flag[0] = True

    return False


def is_mail_time(mail_flag=[True]):
    now_date = datetime.datetime.utcnow()
    if mail_flag[0] and now_date.hour == 2 and now_date.minute == 0:
        logger.debug("is mail time!")
        mail_flag[0] = False
        return True
    elif now_date.hour != 2 or now_date.minute != 0:
        mail_flag[0] = True

    return False


def is_file(file_path):
    return os.path.isfile(file_path)


def cal_avr_health_degree(datas):
    # the health_degree is the last item of each data accroding the poll_data
    # func
    try:
        if datas[0]:
            total_count = sum(data[1] for data in datas)
            avr_health_degree = sum(
                float(data[-1] * data[1]) / total_count for data in datas if data[-1])
            return round(avr_health_degree, 3)
        else:
            return 0.000
    except Exception, e:
        logger.error("wrong when cal avg health degree %s" % e)
        print e


def cal_avr_health_degree_of_provision(datas):
    # the health_degree is the last item of each data accroding the poll_data
    # func
    try:
        if datas:
            total_count = sum(data["count"] for data in datas)
            avr_health_degree = sum(
                float(data["health_degree"] * data["count"]) / total_count for data in datas if data["health_degree"])
            return round(avr_health_degree, 3)
        else:
            return 0.000
    except Exception, e:
        logger.error("wrong when cal avg health degree %s" % e)
        print e


def get_some_days_ago(date, somedays=28):
    some_days_ago = date - datetime.timedelta(days=somedays)
    return some_days_ago
