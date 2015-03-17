# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

PhantomJS_PATH = r'C:\Users\Administrator\Desktop\phantomjs-2.0.0-windows\bin\phantomjs'
crawl_url = 'http://www.tuan800.com/%s/%s/%i'
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


def get_content(source):
	soup = BeautifulSoup(source)
	big_div = soup.find('div', attrs={'class': 'deal_980 l bigdeal'})
	deal_divs = big_div.findAll('div', attrs={'class': 'deal dealbig deal_h'})
	deal_divs.extend(big_div.findAll('div', attrs={'class': 'deal dealbig'}))
	for deal_div in deal_divs:
		imag = deal_div.find('img').attrs['src']
	save2mysql()
	return
		

def main():
	driver = init_driver()
	for city in CITY_LIST:
		for _type in TYPE_LIST:
			i = 1
			while True:
				source = download_source(driver, crawl_url % (city, _type, i))
				isContinue = get_content(source)
				if isContinue:
					i += 1
					continue
				else:
					break
