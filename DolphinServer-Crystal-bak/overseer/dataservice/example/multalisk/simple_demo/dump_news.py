# -*- coding: utf-8 -*-
"""
    database transformation for news project used by multliask/adapter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import MySQLdb
import pymongo
import time
from functools import wraps
from datetime import date, timedelta

from multalisk.ext.adapter import init_adapter, register_adapter, run_adapter

LOCALE_DCT = {'tr-tr': pymongo.Connection('54.93.65.152', 27017),
              'ru-ru': pymongo.Connection('54.93.65.152', 27017),
              'ja-jp': pymongo.Connection('10.132.11.144', 27017),
              'ar-sa': pymongo.Connection('10.132.11.144', 27017)}
MONGO_PORT = 27017


def mysql_retry(times=3):
    def wrapper(func):
        @wraps(func)
        def real_wrapper(*args, **kwargs):
            attempts = 0
            while attempts < times:
                try:
                    return func(*args, **kwargs)
                except (MySQLdb.Error, pymongo.errors.AutoReconnect) as e:
                    init_db()
                    attempts += 1
                    print 'MySQL Error:%s' % e
        return real_wrapper
    return wrapper

mysql_con = local_con = cur = cur_w = None


def init_db():
    global mysql_con, local_con, cur, cur_w
    mysql_con = MySQLdb.connect(
        host='107.20.255.185', db='stat_EN', user='dolphin', passwd='dolphin_stat@logsvr')
    local_con = MySQLdb.connect(
        host='127.0.0.1', db='news_report', user='root', passwd='P@55word')
    mysql_con.set_character_set('utf8')
    local_con.set_character_set('utf8')
    cur = mysql_con.cursor()
    cur_w = local_con.cursor()


@mysql_retry()
def check_table(locale):
    origin_table_name = "report_origin_%s" % locale.replace('-', '_')
    type_sum_table_name = "report_type_sum_%s" % locale.replace('-', '_')
    category_sum_table_name = "report_category_sum_%s" % locale.replace(
        '-', '_')
    priority_sum_table_name = "report_priority_sum_%s" % locale.replace(
        '-', '_')
    source_sum_table_name = "report_source_sum_%s" % locale.replace('-', '_')
    news_sum_table_name = "report_news_sum_%s" % locale.replace('-', '_')

    try:
        sql_str = "create table if not exists %s (`news_id` bigint(20) unsigned NOT NULL,\
                                                  `category` smallint(5) NOT NULL,\
                                                  `priority` smallint(5) NOT NULL,\
                                                  `source` varchar(128) NOT NULL,\
                                                  `top_click` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_click` int(11) NOT NULL DEFAULT '0',\
                                                  `home_click` int(11) NOT NULL DEFAULT '0',\
                                                  `push_click` int(11) NOT NULL DEFAULT '0',\
                                                  `top_show` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_show` int(11) NOT NULL DEFAULT '0',\
                                                  `home_show` int(11) NOT NULL DEFAULT '0',\
                                                  `push_show` int(11) NOT NULL DEFAULT '0',\
                                                  `date` varchar(30) NOT NULL,\
                                                  PRIMARY KEY (`news_id`, `date`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % origin_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (`type` varchar(32) NOT NULL,\
                                                  `click` int(11) NOT NULL DEFAULT '0',\
                                                  `show` int(11) NOT NULL DEFAULT '0',\
                                                  `date` varchar(30) NOT NULL,\
                                                  PRIMARY KEY (`type`,`date`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % type_sum_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (`category` smallint(5) NOT NULL,\
                                                  `top_click` int(11) NOT NULL DEFAULT '0',\
                                                  `top_show` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_click` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_show` int(11) NOT NULL DEFAULT '0',\
                                                  `home_click` int(11) NOT NULL DEFAULT '0',\
                                                  `home_show` int(11) NOT NULL DEFAULT '0',\
                                                  `push_click` int(11) NOT NULL DEFAULT '0',\
                                                  `push_show` int(11) NOT NULL DEFAULT '0',\
                                                  `date` varchar(30) NOT NULL,\
                                                  PRIMARY KEY (`category`,`date`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % category_sum_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (`priority` smallint(5) NOT NULL,\
                                                  `top_click` int(11) NOT NULL DEFAULT '0',\
                                                  `top_show` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_click` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_show` int(11) NOT NULL DEFAULT '0',\
                                                  `home_click` int(11) NOT NULL DEFAULT '0',\
                                                  `home_show` int(11) NOT NULL DEFAULT '0',\
                                                  `push_click` int(11) NOT NULL DEFAULT '0',\
                                                  `push_show` int(11) NOT NULL DEFAULT '0',\
                                                  `date` varchar(30) NOT NULL,\
                                                  PRIMARY KEY (`priority`,`date`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % priority_sum_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (`source` varchar(128) NOT NULL,\
                                                  `category` smallint(5) NOT NULL,\
                                                  `top_click` int(11) NOT NULL DEFAULT '0',\
                                                  `top_show` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_click` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_show` int(11) NOT NULL DEFAULT '0',\
                                                  `home_click` int(11) NOT NULL DEFAULT '0',\
                                                  `home_show` int(11) NOT NULL DEFAULT '0',\
                                                  `push_click` int(11) NOT NULL DEFAULT '0',\
                                                  `push_show` int(11) NOT NULL DEFAULT '0',\
                                                  `date` varchar(30) NOT NULL,\
                                                  PRIMARY KEY (`source`,`date`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % source_sum_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (`news_id` bigint(20) unsigned NOT NULL,\
                                                  `category` smallint(5) NOT NULL,\
                                                  `priority` smallint(5) NOT NULL,\
                                                  `source` varchar(128) NOT NULL,\
                                                  `top_click` int(11) NOT NULL DEFAULT '0',\
                                                  `top_show` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_click` int(11) NOT NULL DEFAULT '0',\
                                                  `recommend_show` int(11) NOT NULL DEFAULT '0',\
                                                  `home_click` int(11) NOT NULL DEFAULT '0',\
                                                  `home_show` int(11) NOT NULL DEFAULT '0',\
                                                  `push_click` int(11) NOT NULL DEFAULT '0',\
                                                  `push_show` int(11) NOT NULL DEFAULT '0',\
                                                  `total_click` int(11) NOT NULL DEFAULT '0',\
                                                  `total_show` int(11) NOT NULL DEFAULT '0',\
                                                  `date` varchar(30) NOT NULL,\
                                                  PRIMARY KEY (`news_id`,`date`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % news_sum_table_name
        cur_w.execute(sql_str)

        local_con.commit()
    except Exception as e:
        print 'check table error:%s' % e


@mysql_retry()
def fill_data(news_id_list, infos, field_str, date_str, locale):
    table_name = "report_origin_%s" % locale.replace('-', '_')
    type_sum_table_name = "report_type_sum_%s" % locale.replace('-', '_')
    category_sum_table_name = "report_category_sum_%s" % locale.replace(
        '-', '_')
    priority_sum_table_name = "report_priority_sum_%s" % locale.replace(
        '-', '_')
    source_sum_table_name = "report_source_sum_%s" % locale.replace('-', '_')
    news_sum_table_name = "report_news_sum_%s" % locale.replace('-', '_')
    for news_id_start in range(len(news_id_list))[::10000]:
        news_ids = news_id_list[news_id_start:news_id_start + 10000]
        mongo_time = time.time()
        mongo_res = infos.find(
            {'_id': {'$in': news_ids}}, {'category': 1, 'status': 1, 'news.linksources': 1})
        print 'query mongo time is %s' % (time.time() - mongo_time)
        result_to_write = [row for row in mongo_res]
        result_to_write.sort(key=lambda item: int(item['_id']))
        [row.update({'source': row['news']['linksources'][0]['blockId']})
         for row in result_to_write]
        sql_str = "select wid, count from Classify_show_%s where wid in %s and source = 'home' order by wid" % (
            date_str, str(tuple(news_ids)))
        query_mysql_time = time.time()
        try:
            cur.execute(sql_str)
        except Exception as e:
            print e
            print sql_str
        home_show_tuple = cur.fetchall()
        home_show_list = [row for row in home_show_tuple]
        home_show_list.sort(key=lambda item: int(item[0]))
        for show_row in home_show_list:
            for row in result_to_write:
                if int(row['_id']) == int(show_row[0]):
                    row.update({'home_show': show_row[1]})
                    break
        cur.execute("select wid, count from Classify_show_%s where wid in %s and source = 'top' order by wid" % (
            date_str, str(tuple(news_ids))))
        top_show_tuple = cur.fetchall()
        top_show_list = [row for row in top_show_tuple]
        top_show_list.sort(key=lambda item: int(item[0]))
        for show_row in top_show_list:
            for row in result_to_write:
                if int(row['_id']) == int(show_row[0]):
                    row.update({'top_show': show_row[1]})
                    break
        cur.execute("select wid, count from Classify_show_%s where wid in %s and source = 'push' order by wid" % (
            date_str, str(tuple(news_ids))))
        push_show_tuple = cur.fetchall()
        push_show_list = [row for row in push_show_tuple]
        push_show_list.sort(key=lambda item: int(item[0]))
        for show_row in push_show_list:
            for row in result_to_write:
                if int(row['_id']) == int(show_row[0]):
                    row.update({'push_show': show_row[1]})
                    break
        cur.execute("select wid, count from Classify_weibo_%s where wid in %s and source = 'home' order by wid" % (
            date_str, str(tuple(news_ids))))
        click_tuple = cur.fetchall()
        click_list = [row for row in click_tuple]
        click_list.sort(key=lambda item: int(item[0]))
        for click_row in click_list:
            for row in result_to_write:
                if int(row['_id']) == int(click_row[0]):
                    row.update({'home_click': click_row[1]})
                    break
        cur.execute("select wid, count from Classify_weibo_%s where wid in %s and source = 'top' order by wid" % (
            date_str, str(tuple(news_ids))))
        click_tuple = cur.fetchall()
        click_list = [row for row in click_tuple]
        click_list.sort(key=lambda item: int(item[0]))
        for click_row in click_list:
            for row in result_to_write:
                if int(row['_id']) == int(click_row[0]):
                    row.update({'top_click': click_row[1]})
                    break
        cur.execute("select wid, count from Classify_weibo_%s where wid in %s and source = 'push' order by wid" % (
            date_str, str(tuple(news_ids))))
        click_tuple = cur.fetchall()
        click_list = [row for row in click_tuple]
        click_list.sort(key=lambda item: int(item[0]))
        for click_row in click_list:
            for row in result_to_write:
                if int(row['_id']) == int(click_row[0]):
                    row.update({'push_click': click_row[1]})
                    break
        cur.execute("select wid, count from P_1_show_%s where wid in %s order by wid" % (
            date_str, str(tuple(news_ids))))
        show_tuple = cur.fetchall()
        show_list = [row for row in show_tuple]
        show_list.sort(key=lambda item: int(item[0]))
        for show_row in show_list:
            for row in result_to_write:
                if int(row['_id']) == int(show_row[0]):
                    row.update({'recommend_show': show_row[1]})
                    break
        cur.execute("select wid, count from P_1_weibo_%s where wid in %s order by wid" % (
            date_str, str(tuple(news_ids))))
        click_tuple = cur.fetchall()
        click_list = [row for row in click_tuple]
        click_list.sort(key=lambda item: int(item[0]))
        for click_row in click_list:
            for row in result_to_write:
                if int(row['_id']) == int(click_row[0]):
                    row.update({'recommend_click': click_row[1]})
                    break
        print 'query mysql time is %s' % (time.time() - query_mysql_time)
        start_time = time.time()
        for result in result_to_write:
            try:
                # insert into origin table
                cur_w.execute("insert into %s (news_id, category, priority, source, top_click, recommend_click, home_click, push_click, top_show, recommend_show, home_show, push_show, date) values(%s,%s,%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,'%s')" %
                              (table_name, result['_id'], result.get('category', 0), result['status'] if result['status'] else -100, result.get('source', ''), result.get('top_click', 0), result.get('recommend_click', 0), result.get('home_click', 0),
                               result.get('push_click', 0), result.get('top_show', 0), result.get('recommend_show', 0), result.get('home_show', 0), result.get('push_show', 0), field_str))
                # insert into type_sum table
                sql_str = "insert into %s (type, click, `show`, date) values('%s',%s,%s,'%s')" % (
                    type_sum_table_name, 'top', result.get('top_click', 0), result.get('top_show', 0), field_str)
                sql_str += "on duplicate key update click=click+%s,`show`=`show`+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0))
                cur_w.execute(sql_str)
                sql_str = "insert into %s (type, click, `show`, date) values('%s',%s,%s,'%s')" % (
                    type_sum_table_name, 'recommend', result.get('recommend_click', 0), result.get('recommend_show', 0), field_str)
                sql_str += "on duplicate key update click=click+%s,`show`=`show`+%s" % (
                    result.get('recommend_click', 0), result.get('recommend_show', 0))
                cur_w.execute(sql_str)
                sql_str = "insert into %s (type, click, `show`, date) values('%s',%s,%s,'%s')" % (
                    type_sum_table_name, 'home', result.get('home_click', 0), result.get('home_show', 0), field_str)
                sql_str += "on duplicate key update click=click+%s,`show`=`show`+%s" % (
                    result.get('home_click', 0), result.get('home_show', 0))
                cur_w.execute(sql_str)
                sql_str = "insert into %s (type, click, `show`, date) values('%s',%s,%s,'%s')" % (
                    type_sum_table_name, 'push', result.get('push_click', 0), result.get('push_show', 0), field_str)
                sql_str += "on duplicate key update click=click+%s,`show`=`show`+%s" % (
                    result.get('push_click', 0), result.get('push_show', 0))
                cur_w.execute(sql_str)
                # insert into category_sum table
                sql_str = "insert into %s (category, top_click, top_show, recommend_click, recommend_show, home_click, home_show, push_click, push_show, date) values(%s, %s, %s, %s, %s, %s,%s, %s, %s, '%s')" % (category_sum_table_name, result.get('category', 0), result.get(
                    'top_click', 0), result.get('top_show', 0), result.get('recommend_click', 0), result.get('recommend_show', 0), result.get('home_click', 0), result.get('home_show', 0), result.get('push_click', 0), result.get('push_show', 0), field_str)
                sql_str += "on duplicate key update top_click=top_click+%s,top_show=top_show+%s,recommend_click=recommend_click+%s,recommend_show=recommend_show+%s,home_click=home_click+%s,home_show=home_show+%s,push_click=push_click+%s,push_show=push_show+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0), result.get('recommend_click', 0), result.get('recommend_show', 0), result.get('home_click', 0), result.get('home_show', 0), result.get('push_click', 0), result.get('push_show', 0))
                cur_w.execute(sql_str)
                # insert into priority_sum table
                sql_str = "insert into %s (priority, top_click, top_show, recommend_click, recommend_show, home_click, home_show, push_click, push_show, date) values(%s, %s, %s, %s, %s, %s,%s, %s, %s, '%s')" % (priority_sum_table_name, result['status'] if result[
                    'status'] else -100, result.get('top_click', 0), result.get('top_show', 0), result.get('recommend_click', 0), result.get('recommend_show', 0), result.get('home_click', 0), result.get('home_show', 0), result.get('push_click', 0), result.get('push_show', 0), field_str)
                sql_str += "on duplicate key update top_click=top_click+%s,top_show=top_show+%s,recommend_click=recommend_click+%s,recommend_show=recommend_show+%s,home_click=home_click+%s,home_show=home_show+%s,push_click=push_click+%s,push_show=push_show+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0), result.get('recommend_click', 0), result.get('recommend_show', 0), result.get('home_click', 0), result.get('home_show', 0), result.get('push_click', 0), result.get('push_show', 0))
                cur_w.execute(sql_str)
                # insert into source_sum table
                sql_str = "insert into %s (source, category, top_click, top_show, recommend_click, recommend_show, home_click, home_show, push_click, push_show, date) values('%s', %s, %s, %s, %s, %s, %s,%s, %s, %s, '%s')" % (source_sum_table_name, result.get('source', ''), result.get(
                    'category', 0), result.get('top_click', 0), result.get('top_show', 0), result.get('recommend_click', 0), result.get('recommend_show', 0), result.get('home_click', 0), result.get('home_show', 0), result.get('push_click', 0), result.get('push_show', 0), field_str)
                sql_str += "on duplicate key update top_click=top_click+%s,top_show=top_show+%s,recommend_click=recommend_click+%s,recommend_show=recommend_show+%s,home_click=home_click+%s,home_show=home_show+%s,push_click=push_click+%s,push_show=push_show+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0), result.get('recommend_click', 0), result.get('recommend_show', 0), result.get('home_click', 0), result.get('home_show', 0), result.get('push_click', 0), result.get('push_show', 0))
                cur_w.execute(sql_str)
                # insert into news_sum table
                total_click = result.get(
                    'top_click', 0) + result.get('home_click', 0) + result.get('push_click', 0)
                total_show = result.get(
                    'top_show', 0) + result.get('home_show', 0) + result.get('push_show', 0)
                sql_str = "insert into %s (news_id, source, category, priority, top_click, top_show, recommend_click, recommend_show, home_click, home_show, push_click, push_show, total_click, total_show, date) values(%s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (news_sum_table_name, result['_id'], result.get('source', ''), result.get(
                    'category', 0), result['status'] if result['status'] else -100, result.get('top_click', 0), result.get('top_show', 0), result.get('recommend_click', 0), result.get('recommend_show', 0), result.get('home_click', 0), result.get('home_show', 0), result.get('push_click', 0), result.get('push_show', 0), total_click, total_show, field_str)
                sql_str += "on duplicate key update top_click=top_click+%s,top_show=top_show+%s,recommend_click=recommend_click+%s,recommend_show=recommend_show+%s,home_click=home_click+%s,home_show=home_show+%s,push_click=push_click+%s,push_show=push_show+%s,total_click=total_click+%s,total_show=total_show+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0), result.get('recommend_click', 0), result.get('recommend_show', 0), result.get('home_click', 0), result.get('home_show', 0), result.get('push_click', 0), result.get('push_show', 0), total_click, total_show)
                cur_w.execute(sql_str)

            except Exception as e:
                print e
                print result
        local_con.commit()
        print '10000 inserted, insert time is %s' % (time.time() - start_time)


@mysql_retry()
def run():
    init_db()
    date_ = date.today() - timedelta(days=1)
    date_str = date_.strftime('%Y%m%d')
    field_str = date_.strftime('%Y-%m-%d')
    for locale, mongo_con in LOCALE_DCT.iteritems():
        print 'current dump country is %s' % locale
        db_name = 'weibo' if locale == 'ja-jp' else 'weibo_%s' % locale.replace(
            '-', '_')
        infos = mongo_con[db_name]['infos']
        cur.execute("select wid from News_show_%s where country='%s' order by wid" % (
            date_str, locale))
        res = cur.fetchall()
        news_id_list = [int(res_tuple[0]) for res_tuple in res]
        check_table(locale)
        fill_data(news_id_list, infos, field_str, date_str, locale)
    print 'adapter done!'


if __name__ == "__main__":
    init_adapter()
    register_adapter(run, '0 1 * * *')
    run_adapter()
