# -*- coding:utf-8 -*-
import logging
import json
import time
import os

from dolphin_weather.crawler.celeryapp import app
from dolphin_weather.model.city import City
from dolphin_weather.cache.city import save_city_to_cache, del_city_from_cache
from dolphin_weather.cache.weather import save_weather_to_cache
from dolphin_weather.cache.alert import (save_alert_weather_to_cache, get_alert_weather_from_cache,
                                         get_alert_weather_number_from_cache)
from dolphin_weather.utils.accuweather import get_weather_from_api, get_alert_from_api, push_alert_weather
from dolphin_weather.utils.common import schema_mapping

_LOGGER = logging.getLogger("dolphin_weather")

_EXPIRE_TIME = 5
_ALERT_NUMBER = 1


def crawl_hot_city():
    try:
        del_city_from_cache()
        query = City.query.filter(City.capital > 0)
        items = query.all()
        for item in items:
            item_dic = item.__dict__
            country = item_dic.get('country')
            capital = item_dic.get('capital')
            city_obj = schema_mapping(item_dic)
            city_obj = json.dumps(city_obj, ensure_ascii=False)
            save_city_to_cache(country, city_obj, capital)
    except Exception as e:
        _LOGGER.exception('crawl error when save hot city, error: %s' % e)


@app.task(expires=_EXPIRE_TIME)
def crawl_hot_city_weather():
    try:
        query = City.query.filter(City.capital != 0)
        items = query.all()
        for item in items:
            item_dic = item.__dict__
            city_key = item_dic.get('key')
            language = item_dic.get('language')
            weather_obj = get_weather_from_api(city_key, language)
            weather_obj = json.dumps(weather_obj, ensure_ascii=False)
            save_weather_to_cache(city_key, language, weather_obj)
    except Exception as e:
        _LOGGER.exception('crawl error when save hot city weather, error: %s' % e)


@app.task(expires=_EXPIRE_TIME)
def crawl_alert_weather():
    try:
        query = City.query.filter(City.capital != 0)
        items = query.all()
        for item in items:
            item_dic = item.__dict__
            city_key = item_dic.get('key')
            language = item_dic.get('language')
            country = item_dic.get('country')
            lc = language[:2].lower() + '_' + country.upper()
            alert_infos = get_alert_from_api(city_key, language)
            push_and_refresh_alert_weather(alert_infos, city_key, lc)
    except Exception as e:
        _LOGGER.exception('crawl error when crawl alert weather, error: %s' % e)


@app.task(name='crawler.crawl.common_city_alert_weather', expires=_EXPIRE_TIME)
def common_city_alert_weather(city_key, language, weather_obj, lc):
    try:
        alert_infos = get_alert_from_api(city_key, language)
        push_and_refresh_alert_weather(alert_infos, city_key, lc)
    except Exception as e:
        _LOGGER.exception('push error when push common alert weather, error: %s' % e)


def push_and_refresh_alert_weather(alert_infos, city_key, lc=None):
    try:
        for alert_info in alert_infos:
            alertId = alert_info.get('alertId')
            if get_alert_weather_number_from_cache(city_key, lc) >= _ALERT_NUMBER:
                break
            if get_alert_weather_from_cache(city_key, alertId, lc):
                continue
            lc = (lc[:2].lower() + '_' + lc[-2:].upper()) if lc else None
            push_alert_weather(city_key, alert_info, lc)
            expire_time = alert_info.get('endTime') - int(time.time())
            expire_time = expire_time if expire_time < 3600 else 3600
            weather_obj = json.dumps(alert_info, ensure_ascii=False)
            save_alert_weather_to_cache(city_key, alertId, weather_obj, expire_time, lc)
    except Exception as e:
        _LOGGER.exception('push and refresh alert weather error, error: %s' % e)


if __name__ == '__main__':
    crawl_hot_city()
