# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import time
import requests
import platform
from selenium import webdriver
from bs4 import BeautifulSoup

from spider.model.base import City, Deal, save_list, get_city_from_mysql
from spider.template import get_meishitianxia

if platform.system() == 'Windows':
	PhantomJS_PATH = r'C:\Users\Administrator\Desktop\phantomjs-2.0.0-windows\bin\phantomjs'
else:
	PhantomJS_PATH = '/usr/local/bin/phantomjs'
LOG_PATH = r'C:\Users\Administrator\Desktop\phantomjs.log'
crawl_url = 'http://www.tuan800.com/%s/%s/page/%i'
city_list_url = 'http://www.tuan800.com/cities'
CITY_LIST = ['wuhan']
TYPE_LIST = ['meishitianxia']

def init_driver():
	client =  webdriver.PhantomJS(executable_path=PhantomJS_PATH)
	client.set_page_load_timeout(60)
	return client

def driver_quit(driver):
	driver.quit()	

def download_source(url, driver=None, is_JS=True):
	if is_JS:
		print 'use phantomjs'
		if not driver:
			driver = init_driver()
		while True:
			try:
				driver.get(url)
				break
			except Exception:
				print 'time out'
			return driver.page_source
	else:
		print 'not use phantomjs'
		res = None
		while True:
			try:
				res = requests.get(url, timeout=5)
				break
			except Exception:
				print 'time out'
		return res.text


def get_city_list(source):
	soup = BeautifulSoup(source)
	lists = soup.find('div', attrs={'class': 'tuan_City'}).findAll('dl')
	res_list = []
	citys = []
	for dl in lists:
		first_char = dl.find('span').text
		for city in dl.findAll('a'):
			citys.append({'first_char': first_char, 'pinyin': city.attrs['city'], 'name': city.text})
			res_list.append(city.attrs['city'])
	save_list(City, citys)
	return res_list


def get_out_link(url):
	res = requests.get(url, timeout=5)
	soup = BeautifulSoup(res.text)
	return soup.find('noframes').find('a').attrs['href']


def get_content(source, city, _type):
	res = []
	try:
		soup = BeautifulSoup(source)
		big_div = soup.find('div', attrs={'class': 'deal_980 l bigdeal'})
		deal_divs = big_div.findAll('div', attrs={'class': 'deal dealbig deal_h'})
		deal_divs.extend(big_div.findAll('div', attrs={'class': 'deal dealbig'}))
		for deal_div in deal_divs:
			try:
				deal_dic = {}
				deal_dic['image'] = deal_div.find('img').attrs['data-original']
				deal_dic['title'] = deal_div.find('div', attrs={'class': 'sitetpy'}).find('a').text
				info = deal_div.find('div', attrs={'class': 'info info2'})
				if not info:
					info = deal_div.find('div', attrs={'class': 'info'})
				deal_dic['source'] = info.find('h4').text
				out_link = info.find('a', attrs={'rel': 'nofollow'})
				deal_dic['detail'] = out_link.text
				deal_dic['out_link'] = get_out_link(out_link.attrs['href'])
				deal_dic['new_price'] = deal_div.find('h5').find('b').text
				deal_dic['old_price'] = deal_div.find('h5').find('em').text[3:]
				deal_dic['location'] = deal_div.find('h6').text
				deal_dic['city'] = city
				deal_dic['type'] = _type
				res.append(deal_dic)
			except Exception as e:
				print "info:%s" % info
				print "res:%s" % deal_dic
				return [], 0
	except Exception as e:
		return [], 0

	page_list = soup.find('div', attrs={'class': 'list_page l'})
	if not page_list:
		return res, 0
	tags = page_list.findAll('span')[-2: -1]
	tags.extend(page_list.findAll('a')[-2: -1])
	last_page = 0
	for tag in tags:
		try:
			temp_int = int(tag.text)
			if temp_int > last_page:
				last_page = temp_int
		except Exception:
			continue
	return res, last_page


def begin_from_to(items, from_city, to_city='zz'):
	res = []
	for item in items:
		if item.pinyin < from_city:
			continue
		if item.pinyin > to_city:
			break
		res.append(item)
	return res


if __name__ == '__main__':
	args = sys.argv
	print len(args)
	if len(args) >=2:
		if args[1] == 'phantomjs':
			is_JS = True
		else:
			is_JS = False
	else:
		is_JS = False

	last_request = 0
	
	for city_dic in begin_from_to(get_city_from_mysql(), 'anshan', 'aomen'):
		pinyin = city_dic.pinyin
		print pinyin
		if pinyin:
			for _type in ['shenghuoyule']:
				i = 1
				while True:
					temp_time = time.time() - last_request
					if temp_time < 5:
						time.sleep(5 - temp_time)

					source = download_source(crawl_url % (pinyin, _type, i), is_JS=is_JS)
					print crawl_url % (pinyin, _type, i)
					last_request = time.time()
					res, last_page = get_content(source, pinyin, _type)
					if res:
						save_list(Deal, res)
					else:
						print 'fail'

					if i >= last_page:
						break
					else:
						i += 1
						continue
	
	#get_city_list(download_source(driver, city_list_url))
	#res, last_page = get_content(download_source(driver, crawl_url % ('anqing', 'meishitianxia', 29)), 'anqing', 'meishitianxia', driver)
	#print last_page
	driver_quit(driver)
