# -*- coding:utf-8 -*-
import os
import logging.config

from tuangou.utils.parser import FreeConfigParser


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


# firstly, load config file to initialize constant
SECTION = 'tuangou_service'
cp = FreeConfigParser()
cp.read([os.path.join(SITE_ROOT, "conf/online.cfg")])

DEBUG = cp.getboolean(SECTION, 'debug', default=True)
EXCEPTION_DEBUG = cp.getboolean(SECTION, 'exception_debug', default=False)
MYSQL_CONFIG = cp.get(SECTION, 'mysql_config', default=None)
MONGO_CONFIG = cp.get(SECTION, 'mongo_config', default=None)
LOG_ROOT = cp.get(SECTION, 'log_root', default='/tmp')
LOG_FILE = os.path.join(LOG_ROOT, 'online_admin.log')
LOG_ERR_FILE = os.path.join(LOG_ROOT, 'online_admin.err')
PAGE_LIMIT = cp.get(SECTION, 'page_limit', default=10)
HTTP_PORT = cp.get(SECTION, 'http_port', default=5000)
REDIS_HOST = cp.get(SECTION, 'redis_host', default='localhost')
REDIS_PORT = cp.get(SECTION, 'redis_port', default=6379)
CELERY_BROKER = cp.get(SECTION, 'celery_broker', default='redis://localhost:6379/1')

API_PREF = '/tuangou'

# secondly, construct logging config dict
LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(process)d %(levelname)s %(asctime)s %(message)s'
        },
        'detail': {
            'format': '%(process)d %(levelname)s %(asctime)s '
            '[%(module)s.%(funcName)s line:%(lineno)d] %(message)s',
        },
    },
    'handlers': {
        'dolphin_weather': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_FILE,
        },
        'err_file': {
            'level': 'WARN',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_ERR_FILE,
        },
    },
    'loggers': {
        'dolphin_weather': {
            'handlers': ['dolphin_weather', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# lastly, config logging
logging.config.dictConfig(LOGGING_DICT)
