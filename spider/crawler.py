# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import time
import requests
import urllib2
import traceback
from bs4 import BeautifulSoup

from spider.model.city import City
from spider.model.deal import Deal
from spider.model.base import save_list, get_city_from_mysql, insert, update
from spider.queue import RedisQueue
from spider.template import *
from spider.mongo.base import *

from spider import mmseg
from spider.settings import CRAWLER_LEVEL

mmseg.dict_load_defaults()

crawl_url = 'http://www.tuan800.com/%s/%s/page/%i'
new_crawl_url = 'http://%s.tuan800.com/%s/page/%i'
city_list_url = 'http://www.tuan800.com/cities'
CITY_LIST = ['wuhan']
TYPE_LIST = ['jiudian', 'meishitianxia', 'shenghuoyule', 'shenghuo']

def get_source(url, rsp_obj=False):
    res = None
    for i in xrange(3):
        try:
            res = requests.get(url, timeout=5*(i+1))
            break
        except Exception as e:
            print 'time out:' + url
    if rsp_obj:
        return res
    else:
        try:
            return res.text
        except Exception as e:
            return None
        

def save_city_list():
    res = get_city_list(get_source(city_list_url))
    save_list(res)


def return_city_list():
    res_list = []
    res = get_city_list(get_source(city_list_url))
    for city in res:
        res_list.append(city.pinyin)
    return res_list


def begin_from_to(items, from_city, to_city='zz'):
    res = []
    for item in items:
        if item.pinyin < from_city:
            continue
        if item.pinyin > to_city:
            break
        res.append(item)
    return res


def push_url_to_queue(from_city, to_city):
    q = RedisQueue('common')

    city_list = get_city_from_mysql()
    if not city_list:
        save_city_list()
        city_list = get_city_from_mysql()
    for city_dic in begin_from_to(city_list, from_city, to_city):
        pinyin = city_dic.pinyin
        for item in TYPE_LIST:
            url = crawl_url % (pinyin, item, 1)
            res = get_source(url, rsp_obj=True)
            last_page = get_last_page(res.text)
            current_url = res.url
            if url ==  current_url:
                for i in xrange(last_page):
                    q.put(crawl_url % (pinyin, item, i + 1))
            else:
                for i in xrange(last_page):
                    q.put(new_crawl_url % (pinyin, item, i + 1))


def update_outlink(outlink):
    source = get_source(outlink)
    new_outlink = get_out_link(source)
    data = {"out_link": new_outlink}
    deal = Deal()
    deal.out_link = outlink
    update(deal, data, "out_link")
    q = RedisQueue('detail')
    q.put(new_outlink)


def update_detail(url):
    source = get_source(url)
    http, rest = urllib2.splittype(url)
    domain, rest = urllib2.splithost(rest)
    try:
        if domain.find('nuomi') >= 0:
            res = get_nuomi_detail(source)
        elif domain.find('meituan') >= 0:
            res = get_meituan_detail(source)
        elif domain.find('dianping') >= 0:
            res = get_dazhongdianping_detail(source)
        elif domain.find('55tuan') >= 0:
            res = get_wowotuan_detail(source)
        elif domain.find('lashou') >= 0:
            res = get_lashouwang_detail(source)
        else:
            return
        deal = Deal()
        deal.out_link = url
        id = update(deal, res, "out_link")
        update_index(id, res.get("detail"))
    except Exception as e:
        print traceback.format_exc()
        print 'get tuangou detail error, error: %s' % e


def update_index(id, detail):
    if id and detail:
        algor = mmseg.Algorithm(detail.encode('utf8'))
        for tok in algor:
            # print tok.text
            if is_exists("index", {"key": tok.text}):
                mongo_update("index", {"key": tok.text}, {"arrays": id})
            else:
                add("index", {"key": tok.text, "arrays": [id]})


def start_crawl(from_city, to_city):
    q_common = RedisQueue('common')
    q_outlink = RedisQueue('outlink')
    q_detail = RedisQueue('detail')
    if q_common.empty():
        push_url_to_queue(from_city, to_city)
    while True:
        if not q_outlink.empty():
            update_outlink(q_outlink.get())
            continue
        if not q_detail.empty():
            update_detail(q_detail.get())
            continue
        url = q_common.get()
        if not url:
            break
        source = get_source(url)
        split_res = url.split('/')
        deal_type = split_res[-3]
        pinyin = split_res[-4].split('.')[0]
        # print deal_type
        # print pinyin
        if deal_type in ['meishitianxia', 'shenghuoyule', 'shenghuo']:
            res = get_meishitianxia(source, pinyin, deal_type)
        elif deal_type in ['jiudian']:
            res = get_hotel(source, pinyin, deal_type)
        else:
            res = []
        if res:
            save_list(res)
            for item in res:
                if item.out_link:
                    q_outlink.put(item.out_link)
        else:
            print 'fail'


def manage_crawler():
    if CRAWLER_LEVEL == 0:
        pass


if __name__ == '__main__':
    #push_url_to_queue('a', 'ac')
    start_crawl('a','ac')
    #save_list(Deal, [{'title': 'a', 'image': 'http://example.com'}])
    #update_deal(Deal.title, 'a', {Deal.title: 'b'})
    #sql = 'update deal set is_show=0'
    #excute_sql(sql)