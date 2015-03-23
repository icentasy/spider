# encoding=utf-8
import datetime
from util_mysql import MySql_Conn
import setting
from util_common import get_table_name, get_date_str, get_yesterday
from util_log import logger
from util_html import get_user_id_table_str, get_sync_site_statistics_table_str
from util_mail import initial_mail_info, send_email
import pymongo
# from pymongo.read_preferences import ReadPreference


class KPIData(object):

    @classmethod
    def new(cls):
        instance = cls()
        instance._mysql_conn = MySql_Conn.new(setting.MYSQL_SETTING['host'],
                                              setting.MYSQL_SETTING[
                                                  'username'],
                                              setting.MYSQL_SETTING[
                                                  'password'],
                                              setting.MYSQL_SETTING['dbname'],
                                              setting.MYSQL_SETTING['port'])

        return instance

    def get_new_user_id_by_day(self, date, exist_tables):

        new_id_map = {'google': 0, 'facebook': 0, 'dolphin': 0, 'total': 0}
        date_str = get_date_str(date)
        table_name = get_table_name('DolphinID_new', date)

        if table_name in exist_tables:
            select_str = 'select user_id,login_type from %s' % table_name

            datas = self._mysql_conn.query_sql(select_str)
        else:
            datas = None
            logger.info("the table %s do not exist" % table_name)

        if datas:
            for item in datas:
                if item[1] == 11:
                    new_id_map['facebook'] += 1
                elif item[1] == 10:
                    new_id_map['google'] += 1
                elif item[1] == 0:
                    new_id_map['dolphin'] += 1
                else:
                    print "not found the info %s" % item[1]
                    logger.info("not found the info %s" % item[1])
            new_id_map['total'] = len(datas)
        else:
            new_id_map = {'google': 0, 'facebook': 0, 'dolphin': 0, 'total': 0}

        return new_id_map

    def get_user_id_by_month(self, date):
        month_new_id_map = {}
        temp_date = date

        exist_tables = self.get_exist_tables()

        for i in range(28):
            date_str = get_date_str(temp_date)
            day_map = self.get_new_user_id_by_day(temp_date, exist_tables)
            month_new_id_map[date_str] = day_map
            temp_date = temp_date - datetime.timedelta(1)
        items = month_new_id_map.items()
        items.sort(reverse=True)

        return items

    def get_user_id_html(self, month_datas, table_name):
        html_str = ""
        html_str += get_user_id_table_str(month_datas, table_name)

        return html_str

    def get_exist_tables(self):
        exist_tables = self._mysql_conn.query_sql("show tables")
        return [i[0] for i in list(exist_tables)]

    def get_sync_site_statistics(self, date):
        exist_tables = self.get_exist_tables()
        table_name = get_table_name('Site_Statistics_', date)
        if table_name in exist_tables:
            select_str = 'select site_url,count from %s where api_type=1' % table_name
            datas = self._mysql_conn.query_sql(select_str)
            return datas
        else:
            logger.info("the table %s do not exist" % table_name)
            datas = [["no data", 0]]
            return datas

    def get_sync_site_html(self, datas, table_name):
        html_str = ""
        html_str += get_sync_site_statistics_table_str(datas, table_name)

        return html_str

    # def get_active_user_by_day(self, date, exist_tables):
        # count_map = {'google': 0, 'facebook': 0, 'dolphin': 0, 'total': 0}

        # date_str = get_date_str(date)
        # table_name = get_table_name('DolphinSync_active', date)

        # try:
        #     if table_name in exist_tables:
        #         select_str = 'select distinct(user_id) from %s' % table_name
        #         datas = self._mysql_conn.query_sql(select_str)
        #     else:
        #         datas = None
        # find the user where it comes from
        #     HOST = "mongodb://10.120.203.9,10.124.221.81"
        #     DB = "user"
        #     mongo_connect = pymongo.Connection(host=HOST)[DB]
        #     for data in datas:
        #         user_id = long(data[0])
        #         d = mongo_connect.user_login.find_one(
        #             {"user_id": user_id}, read_preference=ReadPreference.SECONDARY)
        #         if d:
        #             if d['login_type'] == '10':
        #                 count_map['google'] += 1
        #             elif d['login_type'] == '11':
        #                 count_map['facebook'] += 1
        #             elif d['login_type'] == '0':
        #                 count_map['dolphin'] += 1
        #             else:
        #                 logger.info('other login type:%s user_id:%s' % (d['login_type'], user_id))
        #             count_map['total'] += 1
        #         else:
        #             logger.info("can't find the user,user_id:%s" % user_id)
        #     mongo_connect.close()
        #     return count_map

        # except Exception, e:
        #     print e
        #     logger.error("wrong in get_active_user_by_day:%s" % e)

    # def get_active_user_by_month(self, date):
        # month_new_id_map = {}
        # temp_date = get_yesterday()

        # exist_tables = self.get_exist_tables()

        # for i in range(28):
        #     date_str = get_date_str(temp_date)
        #     day_map = self.get_active_user_by_day(temp_date, exist_tables)
        #     month_new_id_map[date_str] = day_map
        #     temp_date = temp_date - datetime.timedelta(1)
        # items = month_new_id_map.items()
        # items.sort(reverse=True)

        # return items


if __name__ == "__main__":
    import sys
    test_type = str(sys.argv[1])
    kpi_data = KPIData.new()
    req_date = get_yesterday()
    if test_type == "new_id":
        new_id_map_by_month = kpi_data.get_user_id_by_month(
            datetime.datetime.now() - datetime.timedelta(1))

        html_str = kpi_data.get_user_id_html(new_id_map_by_month, "新增用户表")
        print html_str

        initial_mail_info(setting.MAIL_SERVER, setting.MAIL_USER,
                          setting.MAIL_PASSWORD, setting.MAIL_FROM, ["hrwang@bainainfo.com"])
        send_email('[Dolphin Service] API stat Statistics(%s)[%s-%s-%s]'
                   % (setting.SERVICE_IP, req_date.year, req_date.month, req_date.day), html_str, to_list=["hrwang@bainainfo.com"], is_picture=False)
        print "send email succ"

    elif test_type == "active_id":
        pass
        # active_id_map_by_month = kpi_data.get_active_user_by_month(
        #     datetime.datetime.now() - datetime.timedelta(1))

        # html_str = kpi_data.get_user_id_html(new_id_map_by_month, "活跃用户表")
        # print html_str

        # initial_mail_info(setting.MAIL_SERVER, setting.MAIL_USER,
        #               setting.MAIL_PASSWORD, setting.MAIL_FROM, ["hrwang@bainainfo.com"])
        # send_email('[Dolphin Service] API stat Statistics(%s)[%s-%s-%s]'
        #             % (setting.SERVICE_IP, req_date.year, req_date.month, req_date.day), html_str, to_list=["hrwang@bainainfo.com"], is_picture=False)
    elif test_type == "syncsite":
        site_data = kpi_data.get_sync_site_statistics(
            datetime.datetime.now() - datetime.timedelta(1))
        html = kpi_data.get_sync_site_html(site_data, "Sync Site Statistics")
        print html
    print "Done"
