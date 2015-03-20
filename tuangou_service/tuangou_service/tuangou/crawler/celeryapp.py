from __future__ import absolute_import

import logging
from datetime import timedelta
from celery import Celery, platforms
from kombu import Queue, Exchange

from dolphin_weather.settings import CELERY_BROKER

_LOGGER = logging.getLogger(__name__)

WEATHER_CRAWL_INTERVAL = 30 * 60
ALERT_WEATHER_INTERVAL = 10 * 60


class MyRouter(object):

    '''router for tasks using wildcard'''

    def route_for_task(self, task, *args, **kwargs):
        if task == 'crawler.crawl.crawl_hot_city_weather':
            return {'queue': 'hot_city', 'routing_key': 'hot_city'}
        elif task == 'crawler.crawl.crawl_alert_weather':
            return {'queue': 'alert_weather', 'routing_key': 'alert_weather'}
        elif task == 'crawler.crawl.common_city_alert_weather':
            return {'queue': 'common_city_alert_weather', 'routing_key': 'common_city_alert_weather'}
        else:
            return {'queue': 'default', 'routing_key': 'default'}


QUEUES = (
    Queue('hot_city', Exchange('hot_city'),
          routing_key='hot_city'),
    Queue('alert_weather', Exchange('alert_weather'),
          routing_key='alert_weather'),
    Queue('common_city_alert_weather', Exchange('common_city_alert_weather'),
          routing_key='common_city_alert_weather'),
    Queue('default', Exchange('default'), routing_key='default'),
)


app = Celery('crawler',
             broker=CELERY_BROKER,
             include=['crawler.crawl'])

platforms.C_FORCE_ROOT = True

app.conf.update(
    CELERYBEAT_SCHEDULE={
        "crawl-weather-30-mintues": {
            "task": "crawler.crawl.crawl_hot_city_weather",
            "schedule": timedelta(seconds=WEATHER_CRAWL_INTERVAL),
            "args": (),
        },
        "crawl-alert-weather-5-mintues": {
            "task": "crawler.crawl.crawl_alert_weather",
            "schedule": timedelta(seconds=ALERT_WEATHER_INTERVAL),
            "args": (),
        }
    },
    CELERY_QUEUES=QUEUES,
    CELERY_ROUTES=(MyRouter(),),
)

if __name__ == '__main__':
    app.start()
