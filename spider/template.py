# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from spider.model.deal import Deal
from spider.model.city import City

def get_city_list(source):
    soup = BeautifulSoup(source)
    lists = soup.find('div', attrs={'class': 'tuan_City'}).findAll('dl')
    citys = []
    for dl in lists:
        first_char = dl.find('span').text
        for city in dl.findAll('a'):
            res_city = City()
            res_city.first_char = first_char
            res_city.pinyin = city.attrs['city']
            res_city.name = city.text
            citys.append(res_city)
    return citys


def get_last_page(source):
    soup = BeautifulSoup(source)
    page_list = soup.find('div', attrs={'class': 'list_page l'})
    if not page_list:
        return 1
    tags = page_list.findAll('span')[-2: -1]
    tags.extend(page_list.findAll('a')[-2: -1])
    last_page = 1
    for tag in tags:
        try:
            temp_int = int(tag.text)
            if temp_int > last_page:
                last_page = temp_int
        except Exception:
            continue
    return last_page


def get_hotel(source, city, deal_type):
    res = []
    soup = BeautifulSoup(source)
    try:
        deal_div = soup.find('div', attrs={'class': 'dealhotel_980 l'})
        deal_divs = deal_div.findAll('div', attrs={'class': 'dealhotel dealhotel_h'})
        deal_divs.extend(deal_div.findAll('div', attrs={'class': 'dealhotel'}))
    except Exception as e:
        deal_divs = []
        print "get divs error, error: %s" % e
    for deal in deal_divs:
        try:
            res_deal = Deal()
            res_deal.id = deal.attrs['data-id']
            img = deal.find('h3').find('img').attrs
            if 'data-original' in img:
                res_deal.image = img['data-original']
            elif 'src' in img:
                res_deal.image = img['src']
            else:
                break
            res_deal.title = deal.find('h5').find('a').text
            res_deal.source = deal.find('div', attrs={'class': 'info'}).find('h4').find('a').text
            res_deal.detail = deal.find('div', attrs={'class': 'info'}).find('a', attrs={'rel': 'nofollow'}).attrs['title']
            res_deal.out_link = deal.find('h2').find('a').attrs['href']
            res_deal.new_price = deal.find('h2').find('span').find('em').find('b').text
            old_price = deal.find('h2').find('span').find('i').find('b').text
            res_deal.old_price = old_price[old_price.find(u'￥') + 1:]
            location = deal.find('h5').find('em')
            if location:
                res_deal.location = location.text
            res_deal.city = city
            res_deal.type = deal_type
            res.append(res_deal)
        except Exception as e:
            print "get dict error, error: %s" % e
    return res


def get_meishitianxia(source, city, deal_type):
    res = []
    soup = BeautifulSoup(source)
    try:
        big_div = soup.find('div', attrs={'class': 'deal_980 l bigdeal'})
        deal_divs = big_div.findAll('div', attrs={'class': 'deal dealbig deal_h'})
        deal_divs.extend(big_div.findAll('div', attrs={'class': 'deal dealbig'}))
    except Exception as e:
        deal_divs = []
        print "get divs error, error: %s" % e
    for deal_div in deal_divs:
        try:
            res_deal = Deal()
            res_deal.id = deal_div.attrs['info'].split(',')[1]
            res_deal.image = deal_div.find('img').attrs['data-original']
            res_deal.title = deal_div.find('div', attrs={'class': 'sitetpy'}).find('a').text
            info = deal_div.find('div', attrs={'class': 'info info2'})
            if not info:
                info = deal_div.find('div', attrs={'class': 'info'})
            res_deal.source = info.find('h4').find('a').text
            out_link = info.find('a', attrs={'rel': 'nofollow'})
            res_deal.detail = out_link.text
            res_deal.out_link = out_link.attrs['href']
            res_deal.new_price = deal_div.find('h5').find('b').text
            res_deal.old_price = deal_div.find('h5').find('em').text[3:]
            res_deal.location = deal_div.find('h6').text
            res_deal.city = city
            res_deal.type = deal_type
            res.append(res_deal)
            print "city is : %s" % city
        except Exception as e:
            print "get dict error, error: %s" % e
    return res


def get_out_link(source):
    soup = BeautifulSoup(source)
    out_link = soup.find('noframes').find('a').attrs['href']
    # print 'outlink:'+out_link
    return out_link


def get_nuomi_detail(source):
    res = {}
    soup = BeautifulSoup(source)
    invalid_time = soup.find('div',attrs={'class':'validdate-buycount-area static-hook-real static-hook-id-13'}).find('span',attrs={'class':'value'})
    res['invalid_time'] = invalid_time.text
    res['detail'] = soup.find('div',attrs={'class':'p-item-info'}).find('span',attrs={'class':'text-main'}).text
    return res


def get_meituan_detail(source):
    res = {}
    soup = BeautifulSoup(source)
    invalid_time = soup.find('span',attrs={'class':'deal-component-expiry-valid-through'}).text
    res['invalid_time'] = invalid_time[-10:].replace('.', '-')
    res['detail'] = soup.find('div',attrs={'class':'deal-component-description'}).text
    return res


def get_dazhongdianping_detail(source):
    res = {}
    soup = BeautifulSoup(source)
    invalid_time = soup.find('div', attrs={'class': 'validate-date'}).find('span').text
    res['invalid_time'] = invalid_time[5:]
    res['detail'] = soup.find('h2',attrs={'class':'sub-title'}).find('span').text
    return res

def get_wowotuan_detail(source):
    res = {}
    soup = BeautifulSoup(source)
    invalid_time = soup.find('div',attrs={'class':'wbase-item wvalidity'}).text.strip()
    res['invalid_time'] = invalid_time[-10:].replace('.', '-')
    res['detail'] = soup.find('h3',attrs={'class':'wbase-title details-h3'}).text
    return res

def get_lashouwang_detail(source):
    res = {}
    soup = BeautifulSoup(source)
    invalid_time = soup.find('div',attrs={'class':'otherinfo-content'}).find('span',attrs={'class':'text'}).text
    res['invalid_time'] = invalid_time
    res['detail'] = soup.find('div', attrs={'class': 'roduct-name'}).find('p').text
    return res

def get_pinzhituan_detail(source):
    res = {}
    soup = BeautifulSoup(source)
    invalid_time = soup.find('div',attrs={'class':'deal-component-date'}).find('span',attrs={'class':'date-rt'}).text
    res['invalid_time'] = invalid_time[-10:]
    detail = soup.find('h1',attrs={'class':'deal-head-tit'})
    detail.find('strong').hidden = True
    res['detail'] = detail.text
    return res