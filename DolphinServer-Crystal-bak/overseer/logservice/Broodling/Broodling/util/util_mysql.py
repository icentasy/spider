import sys
import traceback
import MySQLdb
from datetime import datetime
from util_log import logger
from util_common import get_date_str, get_today, get_yesterday
from model import EventID, ApiType


class MySql_Conn(object):

    @classmethod
    def new(cls, host, user, passwd, dbname, port):
        # create mysql connection instance
        instance = cls()
        instance._host = host
        instance._user = user
        instance._passwd = passwd
        instance._port = port
        instance._dbname = dbname
        instance.__connect()
        # instance.check_db()

        return instance

    def __connect(self):
        try:
            self._conn = MySQLdb.connect(
                host=self._host, user=self._user, passwd=self._passwd, port=self._port)
            if not self._conn:
                logger.error("MySQL connecting failed!")
            else:
                logger.info("MySQL connecting succ.")
                self.execute_sql('set autocommit=0')
        except MySQLdb.Error, e:
            logger.error("MySQL error %d: %s" % (e.args[0], e.args[1]))
            self._conn = None

    def __disconnect(self):
        if self._conn:
            cur = self._conn.cursor()
            cur.close()
            self._conn.close()
            self._conn = None

    def __reset_connect(self):
        self.__disconnect()
        self.__connect()

    def check_db(self):
        sql_str = "create database if not exists dolphin_stat"
        self.execute_sql(sql_str)

    def get_table_name(self, event_id, date_str):
        table_name = None
        if event_id == EventID.API_stat:
            table_name = "API_stat_%s" % date_str
        if event_id == EventID.Nginx_access:
            table_name = "Nginx_access_%s" % date_str
        elif event_id == EventID.ID_ActiveUser:
            table_name = "DolphinID_active_%s" % date_str
        elif event_id == EventID.ID_NewUser:
            table_name = "DolphinID_new_%s" % date_str
        elif event_id == EventID.Sync_ActiveUser:
            table_name = "DolphinSync_active_%s" % date_str
        elif event_id == EventID.Push_Push:
            table_name = "DolphinPushServer_push_%s" % date_str
        elif event_id == EventID.Push_Sync:
            table_name = "DolphinPushServer_sync_%s" % date_str
        elif event_id == EventID.Push_Fail:
            table_name = "DolphinPushServer_fail_%s" % date_str
        elif event_id == EventID.Push_API_stat:
            table_name = "DolphinPushServer_API_%s" % date_str
        elif event_id == EventID.Push_Channel_stat:
            table_name = "DolphinPushServer_Channel_%s" % date_str
        elif event_id == EventID.Uwsgi_hariki:
            table_name = "Uwsgi_hariki_%s" % date_str
        elif event_id == EventID.Push_ActiveUser:
            table_name = "DolphinPushServer_active_%s" % date_str
        elif event_id == EventID.Push_Offline:
            table_name = "DolphinPushServer_offline_%s" % date_str
        elif event_id == EventID.Site_Statistics:
            table_name = "Site_Statistics_%s" % date_str
        elif event_id == EventID.Operation_nginx:
            table_name = "DolphinOPService_nginx_%s" % date_str
        elif event_id == EventID.Core_Push_Push:
            table_name = 'DolphinPushServer_core_push_push_%s' % date_str
        elif event_id == EventID.Core_Push_Sync:
            table_name = 'DolphinPushServer_core_push_sync_%s' % date_str
        elif event_id == EventID.Core_Push_Affirm:
            table_name = 'DolphinPushServer_core_push_affirm_%s' % date_str
        elif event_id == EventID.Core_Push_Offline:
            table_name = 'DolphinPushServer_core_push_offline_%s' % date_str
        elif event_id == EventID.Core_Handshake:
            table_name = 'DolphinPushServer_core_handshake_%s' % date_str
        elif event_id == EventID.Core_Auth:
            table_name = 'DolphinPushServer_core_auth_%s' % date_str
        elif event_id == EventID.Core_CometD:
            table_name = 'DolphinPushServer_core_cometd_%s' % date_str
        elif event_id == EventID.Provision_data:
            table_name = 'Provision_data_%s' % date_str
        elif event_id == EventID.Provision_locale:
            table_name = 'Provision_locale_%s' % date_str
        elif event_id == EventID.News_weibo:
            table_name = 'News_weibo_%s' % date_str
        elif event_id == EventID.News_show:
            table_name = 'News_show_%s' % date_str
        elif event_id == EventID.Top_weibo:
            table_name = 'Top_weibo_%s' % date_str
        elif event_id == EventID.Top_show:
            table_name = 'Top_show_%s' % date_str
        elif event_id == EventID.Classify_weibo:
            table_name = 'Classify_weibo_%s' % date_str
        elif event_id == EventID.Classify_show:
            table_name = 'Classify_show_%s' % date_str

        return table_name

    def check_table(self, event_id, date):
        date_str = get_date_str(date)
        table_name = self.get_table_name(event_id, date_str)
        sql_str = ""
        if event_id == EventID.API_stat:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `service_ip` varchar(16) NOT NULL,\
                                                      `api_name` varchar(128) NOT NULL,\
                                                      `api_type` tinyint(3) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      `err_count` int(11) unsigned NOT NULL,\
                                                      `ill_count` int(11) unsigned NOT NULL,\
                                                      `sick_count` int(11) unsigned NOT NULL,\
                                                      `bad_count` int(11) unsigned NOT NULL,\
                                                      `avr_exec_time` FLOAT(7,3) NOT NULL,\
                                                      `longest_exec_time` FLOAT(7,3) NOT NULL,\
                                                      `total_exec_time` FLOAT(10,3) NOT NULL,\
                                                      `health_degree` FLOAT(6,3) NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Nginx_access:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `api_name` varchar(128) NOT NULL,\
                                                      `api_type` tinyint(3) NOT NULL,\
                                                      `c_type` varchar(20) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      `err_count` int(11) unsigned NOT NULL,\
                                                      `err_client_count` int(11) unsigned NOT NULL,\
                                                      `err_500_count` int(11) unsigned NOT NULL,\
                                                      `err_502_count` int(11) unsigned NOT NULL,\
                                                      `err_504_count` int(11) unsigned NOT NULL,\
                                                      `ill_count` int(11) unsigned NOT NULL,\
                                                      `sick_count` int(11) unsigned NOT NULL,\
                                                      `bad_count` int(11) unsigned NOT NULL,\
                                                      `avr_exec_time` FLOAT(7,3) NOT NULL,\
                                                      `longest_exec_time` FLOAT(7,3) NOT NULL,\
                                                      `total_exec_time` FLOAT(10,3) NOT NULL,\
                                                      `health_degree` FLOAT(6,3) NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.ID_ActiveUser:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) unsigned NOT NULL,\
                                                      `auth_type` tinyint(1) unsigned NOT NULL DEFAULT '0',\
                                                      `login_type` tinyint(2) unsigned NOT NULL DEFAULT '0',\
                                                      `auth_times` int(11) DEFAULT '0',\
                                                      `last_time` datetime DEFAULT NULL,\
                                                      PRIMARY KEY (`id`),\
                                                      UNIQUE KEY (`user_id`,`auth_type`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.ID_NewUser:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) unsigned NOT NULL,\
                                                      `login_type` tinyint(2) unsigned NOT NULL DEFAULT '0',\
                                                      `create_time` datetime DEFAULT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Sync_ActiveUser:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) unsigned NOT NULL,\
                                                      `sync_type` tinyint(3) unsigned NOT NULL DEFAULT '0',\
                                                      `shard_index` tinyint(3) unsigned NOT NULL DEFAULT '0',\
                                                      `action` tinyint(1) unsigned NOT NULL DEFAULT '0',\
                                                      `times` int(11) DEFAULT '0',\
                                                      `last_time` datetime DEFAULT NULL,\
                                                      PRIMARY KEY (`id`),\
                                                      UNIQUE KEY (`user_id`,`sync_type`,`action`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name

        elif event_id == EventID.Push_Push:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) unsigned NOT NULL,\
                                                      `push_type` tinyint(3) unsigned NOT NULL DEFAULT '0',\
                                                      `src_did` varchar(128) NOT NULL,\
                                                      `dst_did` varchar(128) NOT NULL,\
                                                      `push_time` datetime DEFAULT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Push_Sync:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) unsigned NOT NULL,\
                                                      `push_type` tinyint(3) unsigned NOT NULL DEFAULT '0',\
                                                      `src_did` varchar(128) NOT NULL,\
                                                      `times` int(11) DEFAULT '0',\
                                                      `last_time` datetime DEFAULT NULL,\
                                                      PRIMARY KEY (`id`),\
                                                      UNIQUE KEY (`user_id`,`push_type`,`src_did`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Push_Fail:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) unsigned NOT NULL,\
                                                      `push_type` tinyint(3) unsigned NOT NULL DEFAULT '0',\
                                                      `src_did` varchar(128) NOT NULL,\
                                                      `dst_did` varchar(128) NOT NULL,\
                                                      `push_time` datetime DEFAULT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Push_API_stat:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `client_id` varchar(64) NOT NULL,\
                                                      `channel` varchar(64) NOT NULL,\
                                                      `msg_id` varchar(32) NOT NULL,\
                                                      `receive_time` varchar(64) DEFAULT NULL,\
                                                      `reply_time` varchar(64) DEFAULT NULL,\
                                                      PRIMARY KEY (`id`),\
                                                      UNIQUE KEY (`client_id`,`channel`,`msg_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Push_Channel_stat:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `channel` varchar(64) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      `fail_count` int(11) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Uwsgi_hariki:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `api_name` varchar(128) NOT NULL,\
                                                      `api_type` tinyint(3) NOT NULL,\
                                                      `hariki_time` varchar(128) NOT NULL,\
                                                      `service_ip` varchar(16) NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Push_ActiveUser:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `device_id` varchar(128) NOT NULL,\
                                                      `client_id` varchar(64) NOT NULL,\
                                                      `client_ip` varchar(64) NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Push_Offline:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) NOT NULL,\
                                                      `src_did` varchar(128) NOT NULL,\
                                                      `dst_did` varchar(128) NOT NULL,\
                                                      `push_type` tinyint(3) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Site_Statistics:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `site_url` varchar(128) NOT NULL,\
                                                      `count` int(11) NOT NULL,\
                                                      `api_type` tinyint(3) NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Operation_nginx:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `api_name` varchar(128) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      `cli_err_count` int(11) unsigned NOT NULL,\
                                                      `svr_err_count` int(11) unsigned NOT NULL,\
                                                      `locale` text NOT NULL DEFAULT '',\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Core_Push_Push:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) NOT NULL,\
                                                      `src_did` varchar(128) NOT NULL,\
                                                      `dst_did` varchar(128) NOT NULL,\
                                                      `push_type` tinyint(3) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Core_Push_Sync:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) NOT NULL,\
                                                      `src_did` varchar(128) NOT NULL,\
                                                      `dst_did` varchar(128) NOT NULL,\
                                                      `push_type` tinyint(3) unsigned NOT NULL,\
                                                      `times` int(11) DEFAULT '1',\
                                                       PRIMARY KEY (`id`), \
                                                       UNIQUE KEY (`user_id`,`push_type`,`src_did`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name

        elif event_id == EventID.Core_Push_Affirm:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `msgid` varchar(40) NOT NULL,\
                                                      `device_id` varchar(128) NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name

        elif event_id == EventID.Core_Push_Offline:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `user_id` int(11) NOT NULL,\
                                                      `src_did` varchar(128) NOT NULL,\
                                                      `dst_did` varchar(128) NOT NULL,\
                                                      `push_type` tinyint(3) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name

        elif event_id == EventID.Core_Handshake:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `result` tinyint(3) unsigned NOT NULL,\
                                                      `device_id` varchar(128) NOT NULL,\
                                                      `times` int(11) DEFAULT '1',\
                                                       PRIMARY KEY (`id`), \
                                                       UNIQUE KEY (`result`,`device_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name

        elif event_id == EventID.Core_Auth:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `device_id` varchar(128) NOT NULL,\
                                                      `result` tinyint(3) unsigned NOT NULL,\
                                                      `device_type` tinyint(3) unsigned NOT NULL,\
                                                      `times` int(11) DEFAULT '1',\
                                                       PRIMARY KEY (`id`), \
                                                       UNIQUE KEY (`device_id`,`result`,`device_type`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name

        elif event_id == EventID.Core_CometD:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `api_name` varchar(128) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      `longest_exec_time` int(11) NOT NULL,\
                                                      `avr_exec_time` FLOAT(7,3) NOT NULL,\
                                                      `total_exec_time` int(11) NOT NULL,\
                                                      `good_count` int(11) unsigned NOT NULL,\
                                                      `ok_count` int(11) unsigned NOT NULL,\
                                                      `ill_count` int(11) unsigned NOT NULL,\
                                                      `sick_count` int(11) unsigned NOT NULL,\
                                                      `bad_count` int(11) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name

        elif event_id == EventID.Provision_data:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `api_name` varchar(128) NOT NULL,\
                                                      `package_name` varchar(128) NOT NULL,\
                                                      `os` varchar(64) NOT NULL,\
                                                      `src` varchar(64) NOT NULL,\
                                                      `locale` varchar(64) NOT NULL,\
                                                      `version` varchar(64) NOT NULL,\
                                                      `status_code` varchar(64) NOT NULL,\
                                                      `exec_time` FLOAT(7,3) NOT NULL DEFAULT '0.0',\
                                                       PRIMARY KEY (`id`) \
                                                       ) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        
        elif event_id == EventID.Provision_locale:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `country` varchar(16) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      `miss_match` int(11) unsigned NOT NULL,\
                                                      `miss_match_cc` text NOT NULL DEFAULT '',\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.News_weibo:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `wid` varchar(20) NOT NULL,\
                                                      `country` varchar(16) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.News_show:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `wid` varchar(16) NOT NULL,\
                                                      `country` varchar(16) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Top_weibo:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `wid` varchar(20) NOT NULL,\
                                                      `country` varchar(16) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Top_show:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `wid` varchar(16) NOT NULL,\
                                                      `country` varchar(16) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Classify_weibo:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `wid` varchar(20) NOT NULL,\
                                                      `country` varchar(16) NOT NULL,\
                                                      `source` varchar(16) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
        elif event_id == EventID.Classify_show:
            sql_str = "create table if not exists %s (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,\
                                                      `wid` varchar(20) NOT NULL,\
                                                      `country` varchar(16) NOT NULL,\
                                                      `source` varchar(16) NOT NULL,\
                                                      `count` int(11) unsigned NOT NULL,\
                                                      PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name

        try_count = 0
        while try_count < 3:
            try:
                self._conn.select_db(self._dbname)

                self.execute_sql(sql_str)
                logger.info("create table %s succ!" % table_name)
                break
            except Exception, e:
                try_count += 1
                self.__reset_connect()
                logger.error("MySQL error! %s, try count:%d sql_str: %s" %
                             (e, try_count, sql_str))

    def execute_sql(self, sql_str):
        if self._conn:
            try_count = 0
            while try_count < 3:
                try:
                    cur = self._conn.cursor()
                    self._conn.select_db(self._dbname)
                    cur.execute(sql_str)
                    self._conn.commit()
                    break
                except MySQLdb.Error, e:
                    try_count += 1
                    self.__reset_connect()
                    logger.error(
                        "MySQL error! %d: %s, try count:%d sql_str: %s" %
                        (e.args[0], e.args[1], try_count, sql_str))

    def query_sql(self, sql_str):
        if self._conn:
            try_count = 0
            while try_count < 3:
                try:
                    cur = self._conn.cursor()
                    self._conn.select_db(self._dbname)
                    count = cur.execute(sql_str)
                    logger.debug("MySQL query %s rows record" % count)
                    results = cur.fetchall()
                    self._conn.commit()

                    return results
                except MySQLdb.Error, e:
                    try_count += 1
                    self.__reset_connect()
                    logger.error("MySQL error! %d: %s, try count:%d" %
                                 (e.args[0], e.args[1], try_count))

        return None

    def update_api(self, api_map, log_date, service_ip):
        table_name = self.get_table_name(EventID.API_stat, date_str=log_date)
        if table_name:
            sql_str = "insert into %s (service_ip,\
                                       api_name,\
                                       api_type,\
                                       count,\
                                       err_count,\
                                       ill_count,\
                                       sick_count,\
                                       bad_count,\
                                       avr_exec_time,\
                                       longest_exec_time,\
                                       total_exec_time,\
                                       health_degree) values" % table_name
            insert_count = 0
            for (api_name, api_info) in api_map.items():
                # skip the useless type
                if api_info.get('api_type') == ApiType.other:
                    continue

                if insert_count > 0:
                    sql_str += ","

                count = api_info.get('count')
                err_count = api_info.get('err_count')
                bad_count = api_info.get('bad_count')
                sick_count = api_info.get('sick_count')
                ill_count = api_info.get('ill_count')

                # calculate health degree
                health_degree = (count - err_count * 1 - bad_count *
                                 0.8 - sick_count * 0.6 - ill_count * 0.4) / count * 100
                health_degree = round(health_degree, 3)
                sql_str += "('%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" %\
                           (service_ip, api_name,
                            api_info.get('api_type'),
                            count,
                            err_count,
                            ill_count,
                            sick_count,
                            bad_count,
                            api_info.get('avr_exec_time'),
                            api_info.get('longest_exec_time'),
                            api_info.get('total_exec_time'),
                            health_degree)
                insert_count += 1
            logger.info("[API_stat]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def update_nginx_access(self, api_map, log_date, service_ip):
        table_name = self.get_table_name(
            EventID.Nginx_access, date_str=log_date)

        if table_name:
            sql_str = "insert into %s (api_name,\
                                       api_type,\
                                       c_type,\
                                       count,\
                                       err_count,\
                                       err_client_count,\
                                       err_500_count,\
                                       err_502_count,\
                                       err_504_count,\
                                       ill_count,\
                                       sick_count,\
                                       bad_count,\
                                       avr_exec_time,\
                                       longest_exec_time,\
                                       total_exec_time,\
                                       health_degree) values" % table_name
            insert_count = 0
            for (api_key, api_info) in api_map.items():
                # skip the useless type
                if api_info.get('api_type') == ApiType.other:
                    continue
                if insert_count > 0:
                    sql_str += ","
                count = api_info.get('count')
                err_client_count = api_info.get('err_client_count', 0)
                err_count = api_info.get('err_count', 0)
                bad_count = api_info.get('bad_count', 0)
                sick_count = api_info.get('sick_count', 0)
                ill_count = api_info.get('ill_count', 0)
                err_500_count = api_info.get('err_500_count', 0)
                err_502_count = api_info.get('err_502_count', 0)
                err_504_count = api_info.get('err_504_count', 0)
                # calculate health degree
                health_degree = (count - err_count * 1 - bad_count *
                                 0.8 - sick_count * 0.6 - ill_count * 0.4) / count * 100
                health_degree = round(health_degree, 3)
                sql_str += "('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" %\
                    (api_info.get('api_name'),
                     api_info.get('api_type'),
                     api_info.get('c_type'),
                     count,
                     api_info.get('err_count'),
                     err_client_count,
                     err_500_count,
                     err_502_count,
                     err_504_count,
                     ill_count,
                     sick_count,
                     bad_count,
                     api_info.get('avr_exec_time'),
                     api_info.get('longest_exec_time'),
                     api_info.get('total_exec_time'),
                     health_degree)
                insert_count += 1
            logger.info("[Nginx_access]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def update_operation_nginx(self, api_map, log_date, service_ip):
        table_name = self.get_table_name(
            EventID.Operation_nginx, date_str=log_date)

        if table_name:
            sql_str = "insert into %s (api_name,\
                                       count,\
                                       cli_err_count,\
                                       svr_err_count,\
                                       locale) values" % table_name

            insert_count = 0
            for (api_name, api_info) in api_map.items():
                if insert_count > 0:
                    sql_str += ","
                count = api_info.get('count')
                cli_err_count = api_info.get('cli_err_count', 0)
                svr_err_count = api_info.get('svr_err_count', 0)
                import simplejson
                locale_str = simplejson.dumps(api_info.get('locale'))
                sql_str += "('%s', %s, %s, %s, '%s')" %\
                    (api_name,
                     count,
                     cli_err_count,
                     svr_err_count,
                     locale_str)
                insert_count += 1
            logger.info("[Operation_nginx]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def update_operation_locale(self, country_map, log_date, service_ip):
        table_name = self.get_table_name(
            EventID.Provision_locale, date_str=log_date)

        if table_name:
            sql_str = "insert into %s (country,\
                                       count,\
                                       miss_match,\
                                       miss_match_cc) values" % table_name

            insert_count = 0
            for (country, country_info) in country_map.items():
                if insert_count > 0:
                    sql_str += ","
                count = country_info.get('count')
                miss_match = country_info.get('miss_match', 0)
                import simplejson
                miss_match_cc_str = simplejson.dumps(country_info.get('miss_match_cc'))
                sql_str += "('%s', %s, %s, '%s')" %\
                    (country,
                     count,
                     miss_match,
                     miss_match_cc_str)
                insert_count += 1
            logger.info("[Operation_locale]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_ID_active(self, log_date, active_list):
        table_name = self.get_table_name(EventID.ID_ActiveUser, log_date)

        if table_name:
            sql_str = "insert into %s (user_id,\
                                       auth_type,\
                                       login_type,\
                                       auth_times,\
                                       last_time) values" % table_name
            insert_count = 0
            for active_info in active_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "(%d, %d, %d, %d, '%s')" %\
                    (active_info['user_id'],
                     active_info['auth_type'],
                     active_info['login_type'],
                     1,
                     active_info['auth_time'])
                insert_count += 1
            #logger.debug("[ID_active]insert sql:%s" % sql_str)
            sql_str += " ON DUPLICATE KEY UPDATE login_type=VALUES(login_type),auth_times=auth_times+1,last_time=VALUES(last_time)"
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_ID_new(self, log_date, new_list):
        table_name = self.get_table_name(EventID.ID_NewUser, log_date)

        if table_name:
            sql_str = "insert into %s (user_id, login_type, create_time) values" % table_name
            insert_count = 0
            for new_info in new_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "(%d, %d, '%s')" % (new_info['user_id'],
                                               new_info['login_type'], new_info['create_time'])
                insert_count += 1
            #logger.debug("[ID_new]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_Sync_active(self, log_date, active_list):
        table_name = self.get_table_name(EventID.Sync_ActiveUser, log_date)

        if table_name:
            sql_str = "insert into %s (user_id, sync_type, action, shard_index, times, last_time) values" % table_name
            insert_count = 0
            for active_info in active_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "(%d, %d, %d, %d, %d, '%s')" % (active_info['user_id'],
                                                           active_info['sync_type'], active_info['action_type'], active_info['shard_index'], 1, active_info['sync_time'])
                insert_count += 1
            sql_str += " ON DUPLICATE KEY UPDATE times=times+1,last_time=VALUES(last_time)"
            #logger.debug("[Sync_active]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_Push(self, log_date, push_list, fail_list):
        if len(push_list) > 0:
            self.submit_Push_push(log_date, push_list)

        if len(fail_list) > 0:
            self.submit_Push_fail(log_date, fail_list)

    def submit_Push_push(self, log_date, push_list):
        table_name = self.get_table_name(EventID.Push_Push, log_date)

        if table_name:
            sql_str = "insert into %s (user_id, push_type, src_did, dst_did, push_time) values" % table_name
            insert_count = 0
            for push_info in push_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "(%d, %d, '%s', '%s', '%s')" % (push_info['user_id'],
                                                           push_info['push_type'], push_info[
                                                               'src_did'], push_info['dst_did'],
                                                           push_info['push_time'])
                insert_count += 1
            #logger.debug("[Push_push]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_Push_sync(self, log_date, push_list):
        table_name = self.get_table_name(EventID.Push_Sync, log_date)

        if table_name:
            sql_str = "insert into %s (user_id, push_type, src_did, times, last_time) values" % table_name
            insert_count = 0
            for push_info in push_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "(%d, %d, '%s', %d, '%s')" % (push_info['user_id'],
                                                         push_info['push_type'], push_info['src_did'], 1, push_info['push_time'])
                insert_count += 1
            sql_str += " ON DUPLICATE KEY UPDATE times=times+1,last_time=VALUES(last_time)"
            #logger.debug("[Push_sync]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_Push_fail(self, log_date, push_list):
        table_name = self.get_table_name(EventID.Push_Fail, log_date)

        if table_name:
            sql_str = "insert into %s (user_id, push_type, src_did, dst_did, push_time) values" % table_name
            insert_count = 0
            for push_info in push_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "(%d, %d, '%s', '%s', '%s')" % (push_info['user_id'],
                                                           push_info['push_type'], push_info[
                                                               'src_did'], push_info['dst_did'],
                                                           push_info['push_time'])
                insert_count += 1
            #logger.debug("[Push_fail]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_Uwsgi_hariki(self, log_date, hariki_list):
        table_name = self.get_table_name(
            EventID.Uwsgi_hariki, date_str=log_date)

        if table_name:
            sql_str = "insert into %s (api_name, api_type, hariki_time, service_ip) values" % table_name
            insert_count = 0
            for hariki_info in hariki_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "('%s', %s, '%s', '%s')" %\
                    (hariki_info['api_name'],
                     hariki_info['api_type'],
                     hariki_info['hariki_time'],
                     hariki_info['service_ip'])
                insert_count += 1
            logger.info("[Uwsgi_hariki]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_Push_API_stat(self, log_date, api_list):
        table_name = self.get_table_name(
            EventID.Push_API_stat, date_str=log_date)

        if table_name:
            sql_str = "insert into %s (client_id, channel, msg_id, receive_time, reply_time) values" % table_name
            insert_count = 0
            for api_info in api_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "('%s', '%s', '%s', '%s', '%s')" %\
                    (api_info['client_id'],
                     api_info['channel'],
                     api_info['msg_id'],
                     api_info['receive_time'],
                     api_info['reply_time'])
                insert_count += 1
                if insert_count > 10000:
                    sql_str += " ON DUPLICATE KEY UPDATE reply_time=VALUES(reply_time)"
                    self.execute_sql(sql_str)
                    self.execute_sql('commit')
                    sql_str = "insert into %s (client_id, channel, msg_id, receive_time, reply_time) values" % table_name
                    insert_count = 0

            if insert_count > 0:
                sql_str += " ON DUPLICATE KEY UPDATE reply_time=VALUES(reply_time)"
                self.execute_sql(sql_str)
                self.execute_sql('commit')

    def submit_Push_Channel_stat(self, log_date, channel_map):
        table_name = self.get_table_name(
            EventID.Push_Channel_stat, date_str=log_date)

        if table_name:
            sql_str = "insert into %s (channel,\
                                       count,\
                                       fail_count) values" % table_name
            insert_count = 0
            for (channel_name, channel_info) in channel_map.items():
                if insert_count > 0:
                    sql_str += ","

                total_count = channel_info.get(
                    'count') if channel_info.has_key('count') else 0
                fail_count = channel_info.get(
                    'fail_count') if channel_info.has_key('fail_count') else 0
                sql_str += "('%s', %s, %s)" % (channel_name,
                                               total_count, fail_count)
                insert_count += 1
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_Push_active(self, log_date, active_list):
        table_name = self.get_table_name(EventID.Push_ActiveUser, log_date)

        if table_name:
            sql_str = "insert into %s (device_id,\
                                       client_id,\
                                       client_ip) values" % table_name
            insert_count = 0
            for active_info in active_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "('%s', '%s', '%s')" %\
                    (active_info['device_id'],
                     active_info['client_id'],
                     active_info['client_ip'])
                insert_count += 1
            #logger.debug("[ID_active]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def submit_Push_offline(self, log_date, data_list):
        table_name = self.get_table_name(EventID.Push_Offline, log_date)

        if table_name:
            sql_str = "insert into %s (user_id,\
                                       src_did,\
                                       dst_did,\
                                       push_type) values" % table_name
            insert_count = 0
            for data_info in data_list:
                if insert_count > 0:
                    sql_str += ","
                sql_str += "(%d, '%s', '%s', %d)" %\
                    (data_info['user_id'],
                     data_info['src_did'],
                     data_info['dst_did'],
                     data_info['push_type'])
                insert_count += 1
            #logger.debug("[ID_active]insert sql:%s" % sql_str)
            self.execute_sql(sql_str)
            self.execute_sql('commit')

    def update_site_statistics(self, log_date, data_map, api_type):
        table_name = self.get_table_name(EventID.Site_Statistics, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (site_url,\
                                           count,\
                                           api_type) values" % table_name
                insert_count = 0
                for (key, value) in data_map.items():
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "('%s', %d, %d)" %\
                        (key,
                         value,
                         api_type)
                    insert_count += 1
                logger.info("[Site_Statistics]insert sql:%s" % sql_str)
                self.execute_sql(sql_str)
                self.execute_sql('commit')
                print "Done"
        except Exception, e:
            logger.error("error in update site :%s" % e)
            print e

    def submit_Core_Push_Push(self, log_date, track_list):
        table_name = self.get_table_name(EventID.Core_Push_Push, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (user_id,\
                                           src_did,dst_did,push_type) values" % table_name
                insert_count = 0
                for track_info in track_list:
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "(%d, '%s', '%s', %d)" %\
                        (track_info['user_id'],
                         track_info['src_did'],
                         track_info['dst_did'],
                         track_info['push_type'])
                    insert_count += 1
                #logger.debug("[ID_active]insert sql:%s" % sql_str)
                self.execute_sql(sql_str)
                self.execute_sql('commit')
        except Exception, e:
            logger.error(
                "error in submit pushservice track, db sql:%s,error info:%s" %
                (sql_str, e))

    def submit_Core_Push_Sync(self, log_date, track_list):
        table_name = self.get_table_name(EventID.Core_Push_Sync, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (user_id,\
                                           src_did,dst_did,push_type) values" % table_name
                insert_count = 0
                for track_info in track_list:
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "(%d, '%s', '%s', %d)" %\
                        (track_info['user_id'],
                         track_info['src_did'],
                         track_info['dst_did'],
                         track_info['push_type'])
                    insert_count += 1
                #logger.debug("[ID_active]insert sql:%s" % sql_str)
                sql_str += " ON DUPLICATE KEY UPDATE times=times+1"
                self.execute_sql(sql_str)
                self.execute_sql('commit')
        except Exception, e:
            logger.error(
                "error in submit pushservice track, db sql:%s,error info:%s" %
                (sql_str, e))

    def submit_Core_Push_Affirm(self, log_date, track_list):
        table_name = self.get_table_name(EventID.Core_Push_Affirm, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (msgid,\
                                           device_id) values" % table_name
                insert_count = 0
                for track_info in track_list:
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "('%s', '%s')" %\
                        (track_info['msgid'],
                         track_info['device_id'])
                    insert_count += 1
                #logger.debug("[ID_active]insert sql:%s" % sql_str)
                self.execute_sql(sql_str)
                self.execute_sql('commit')
        except Exception, e:
            logger.error(
                "error in submit pushservice track, db sql:%s,error info:%s" %
                (sql_str, e))

    def submit_Core_Push_Offline(self, log_date, track_list):
        table_name = self.get_table_name(EventID.Core_Push_Offline, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (user_id,\
                                           src_did,dst_did,push_type) values" % table_name
                insert_count = 0
                for track_info in track_list:
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "(%d, '%s', '%s', %d)" %\
                        (track_info['user_id'],
                         track_info['src_did'],
                         track_info['dst_did'],
                         track_info['push_type'])
                    insert_count += 1
                #logger.debug("[ID_active]insert sql:%s" % sql_str)
                self.execute_sql(sql_str)
                self.execute_sql('commit')
        except Exception, e:
            logger.error(
                "error in submit pushservice track, db sql:%s,error info:%s" %
                (sql_str, e))

    def submit_Core_Handshake(self, log_date, track_list):
        table_name = self.get_table_name(EventID.Core_Handshake, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (result,\
                                           device_id) values" % table_name
                insert_count = 0
                for track_info in track_list:
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "(%d, '%s')" %\
                        (track_info['result'],
                         track_info['device_id'])
                    insert_count += 1
                #logger.debug("[ID_active]insert sql:%s" % sql_str)
                sql_str += " ON DUPLICATE KEY UPDATE times=times+1"
                self.execute_sql(sql_str)
                self.execute_sql('commit')
        except Exception, e:
            logger.error(
                "error in submit pushservice track, db sql:%s,error info:%s" %
                (sql_str, e))

    def submit_Core_Auth(self, log_date, track_list):
        table_name = self.get_table_name(EventID.Core_Auth, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (device_id,\
                                           result,device_type) values" % table_name
                insert_count = 0
                for track_info in track_list:
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "('%s', %d, %d)" %\
                        (track_info['device_id'],
                         track_info['result'],
                         track_info['device_type'])
                    insert_count += 1
                #logger.debug("[ID_active]insert sql:%s" % sql_str)
                sql_str += " ON DUPLICATE KEY UPDATE times=times+1"
                self.execute_sql(sql_str)
                self.execute_sql('commit')
        except Exception, e:
            logger.error(
                "error in submit pushservice track, db sql:%s,error info:%s" %
                (sql_str, e))

    def update_Core_CometD(self, api_map, log_date):
        table_name = self.get_table_name(EventID.Core_CometD, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (api_name,\
                                       count,\
                                       longest_exec_time,\
                                       avr_exec_time,\
                                       total_exec_time,\
                                       good_count,\
                                       ok_count,\
                                       ill_count,\
                                       sick_count,\
                                       bad_count) values" % table_name
                insert_count = 0
                for (api_name, api_info) in api_map.items():
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "('%s', %s, %s, %s, %s, %s, %s, %s, %s, %s)" %\
                        (api_name,
                         api_info.get('count'),
                         api_info.get('longest_exec_time'),
                         api_info.get('avr_exec_time'),
                         api_info.get('total_exec_time'),
                         api_info.get('good_count'),
                         api_info.get('ok_count'),
                         api_info.get('ill_count'),
                         api_info.get('sick_count'),
                         api_info.get('bad_count'))
                    insert_count += 1
                logger.info("[Core_CometD]insert sql:%s" % sql_str)
                self.execute_sql(sql_str)
                self.execute_sql('commit')
        except Exception, e:
            logger.error(
                "error in submit pushservice track, db sql:%s,error info:%s" %
                (sql_str, e))

    def update_provision_data(self, log_date, provision_list):
        table_name = self.get_table_name(
            EventID.Provision_data, get_date_str(log_date))
        try:
            if table_name:
                sql_str = "insert into %s (api_name,package_name,os,src,locale,version,status_code,exec_time) values" % table_name
                insert_count = 0
                for provision_data in provision_list:
                    if insert_count > 0:
                        sql_str += ","
                    sql_str += "('%s','%s','%s','%s','%s','%s','%s',%s)" % \
                        (provision_data["api_name"],
                         provision_data["package_name"],
                         provision_data["os"],
                         provision_data["src"],
                         provision_data["locale"],
                         provision_data["version"],
                         provision_data["status_code"],
                         provision_data["exec_time"])
                    insert_count += 1
                self.execute_sql(sql_str)
                self.execute_sql("commit")
        except Exception, e:
            logger.error(
                "error in submit provision_data track, db sql:%s,error info:%s" %
                (sql_str, e))

    def submit_weibo_data(self, log_date, weiboinfo):
        table_name = self.get_table_name(
            EventID.News_weibo, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (wid,country,count) values" % table_name
                insert_count = 0
                for country in weiboinfo.keys():
                    for wid in weiboinfo[country].keys():
                        if insert_count > 0:
                            sql_str += ","
                        sql_str += "('%s','%s',%s)" % \
                        (wid,country,weiboinfo[country][wid])
                        insert_count += 1
                self.execute_sql(sql_str)
                self.execute_sql("commit")
        except Exception, e:
            logger.error(
                "error in submit News_weibo track, db sql:%s,error info:%s" ,
                sql_str, e)

    def submit_show_data(self, log_date, showinfo):
        table_name = self.get_table_name(
            EventID.News_show, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (wid,country,count) values" % table_name
                insert_count = 0
                for country in showinfo.keys():
                    for wid in showinfo[country].keys():
                        if insert_count > 0:
                            sql_str += ","
                        sql_str += "('%s','%s',%s)" % \
                        (wid,country,showinfo[country][wid])
                        insert_count += 1
                self.execute_sql(sql_str)
                self.execute_sql("commit")
        except Exception, e:
            logger.error(
                "error in submit News_show track, db sql:%s,error info:%s" ,
                sql_str, e)

    def submit_topweibo_data(self, log_date, weiboinfo):
        table_name = self.get_table_name(
            EventID.Top_weibo, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (wid,country,count) values" % table_name
                insert_count = 0
                for country in weiboinfo.keys():
                    for wid in weiboinfo[country].keys():
                        if insert_count > 0:
                            sql_str += ","
                        sql_str += "('%s','%s',%s)" % \
                        (wid,country,weiboinfo[country][wid])
                        insert_count += 1
                self.execute_sql(sql_str)
                self.execute_sql("commit")
        except Exception, e:
            logger.error(
                "error in submit Top_weibo track, db sql:%s,error info:%s" ,
                sql_str, e)

    def submit_classifyweibo_data(self, log_date, weiboinfo):
        table_name = self.get_table_name(
            EventID.Classify_weibo, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (wid,country,source,count) values" % table_name
                insert_count = 0
                for country in weiboinfo.keys():
                    for source in weiboinfo[country].keys():
                        for wid,wid_count in weiboinfo[country][source].items():
                            if insert_count > 0:
                                sql_str += ","
                            sql_str += "('%s','%s','%s',%s)" % \
                            (wid,country,source,wid_count)
                        insert_count += 1
                self.execute_sql(sql_str)
                self.execute_sql("commit")
        except Exception, e:
            logger.error(
                "error in submit Classify_weibo track, db sql:%s,error info:%s" ,
                sql_str, e)


    def submit_topshow_data(self, log_date, showinfo):
        table_name = self.get_table_name(
            EventID.Top_show, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (wid,country,count) values" % table_name
                insert_count = 0
                for country in showinfo.keys():
                    for wid in showinfo[country].keys():
                        if insert_count > 0:
                            sql_str += ","
                        sql_str += "('%s','%s',%s)" % \
                        (wid,country,showinfo[country][wid])
                        insert_count += 1
                self.execute_sql(sql_str)
                self.execute_sql("commit")
        except Exception, e:
            logger.error(
                "error in submit Top_show track, db sql:%s,error info:%s" ,
                sql_str, e)

    def submit_classifyshow_data(self, log_date, showinfo):
        table_name = self.get_table_name(
            EventID.Classify_show, log_date)
        try:
            if table_name:
                sql_str = "insert into %s (wid,country,source,count) values" % table_name
                insert_count = 0
                for country in showinfo.keys():
                    for source in showinfo[country].keys():
                        for wid,wid_count in showinfo[country][source].items():
                            if insert_count > 0:
                                sql_str += ","
                            sql_str += "('%s','%s','%s',%s)" % \
                            (wid,country,source,wid_count)
                            insert_count += 1
                self.execute_sql(sql_str)
                self.execute_sql("commit")
        except Exception, e:
            logger.error(
                "error in submit Classify_show track, db sql:%s,error info:%s" ,
                sql_str, e)


if __name__ == "__main__":
    mysql_conn = MySql_Conn.new(
        '127.0.0.1', 'root', '123456', 'dolphin_stat', 3306)
    # mysql_conn.check_table(EventID.Core_CometD,get_yesterday())
    data_map = {"www.baidu.com": 99}
    date_str = get_date_str(get_today())
    mysql_conn.update_site_statistics(date_str, data_map, 1)
    print "ok"
