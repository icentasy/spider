# -*- coding: utf-8 -*-
import time
import platform
from selenium import webdriver
from bs4 import BeautifulSoup

import sys
sys.path.append("../")

from spider.model.base import City, Deal

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
	return webdriver.PhantomJS(executable_path=PhantomJS_PATH)


def driver_quit(driver):
	driver.quit()
	

def download_source(driver, url):
	driver.get(url)
	return driver.page_source


def save2mysql():
	pass


def get_city_list(source):
	soup = BeautifulSoup(source)
	lists = soup.find('div', attrs={'class': 'tuan_City'}).findAll('dl')
	res_list = []
	citys = {}
	for dl in lists:
		first_char = dl.find('span').text
		cities[first_char] = []
		for city in dl.findAll('a'):
			cities[first_char].append((city.attrs['city'], city.text))
			res_list.append(city.attrs['city'])
	return res_list


def get_out_link(source):
	soup = BeautifulSoup(source)
	return soup.find('noframes').find('a').attrs['href']


def get_content(source, city, _type, driver):
	time.sleep(3)
	res = []
	soup = BeautifulSoup(source)
	big_div = soup.find('div', attrs={'class': 'deal_980 l bigdeal'})
	deal_divs = big_div.findAll('div', attrs={'class': 'deal dealbig deal_h'})
	deal_divs.extend(big_div.findAll('div', attrs={'class': 'deal dealbig'}))
	for deal_div in deal_divs:
		try:
			deal_dic = {}
			deal_dic['image'] = deal_div.find('img').attrs['src']
			deal_dic['title'] = deal_div.find('div', attrs={'class': 'sitetpy'}).find('a').text
			info = deal_div.find('div', attrs={'class': 'info info2'})
			if not info:
				info = deal_div.find('div', attrs={'class': 'info'})
			deal_dic['source'] = info.find('h4').text
			out_link = info.find('a', attrs={'rel': 'nofollow'})
			deal_dic['detail'] = out_link.text
			deal_dic['out_link'] = out_link.attrs['href']
			deal_dic['new_price'] = deal_div.find('h5').find('b').text
			deal_dic['old_price'] = deal_div.find('h5').find('em').text
			deal_dic['location'] = deal_div.find('h6').text
			deal_dic['city'] = city
			deal_dic['type'] = _type
			res.append(deal_dic)
		except Exception as e:
			print e
			print "info:%s" % info
			print "res:%s" % deal_dic
	#save2mysql(res)

	page_list = soup.find('div', attrs={'class': 'list_page l'})
	if not page_list:
		return False
	if page_list.findAll('span')[-1].text == u'下页':
		return False
	elif page_list.findAll('a')[-1].text == u'下页':
		return True
	else:
		print page_list
		print 'unknown next page'
		return False
		

def main():
	driver = init_driver()
	city_list = get_city_list(download_source(city_list_url))
	for city in city_list:
		for _type in TYPE_LIST:
			i = 1
			while True:
				source = download_source(driver, crawl_url % (city, _type, i))
				isContinue = get_content(source, city, _type, driver)
				if isContinue:
					i += 1
					continue
				else:
					break


if __name__ == '__main__':
	driver = init_driver()
	start = time.time()
	isContinue = get_content(download_source(driver, crawl_url % ('wuhan', 'meishitianxia', 1)), 'wuhan', 'meishitianxia', driver)
	end = time.time()
	print round(end - start, 4)
	driver_quit(driver)