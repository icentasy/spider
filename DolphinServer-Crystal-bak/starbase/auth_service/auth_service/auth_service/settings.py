# -*- coding:utf-8 -*-
import os
import logging.config

from armory.marine.parser import FreeConfigParser
from armory.marine.json import ArmoryJson


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


# firstly, load config file to initialize constant
SECTION = 'auth-service'
cp = FreeConfigParser()
cp.read([os.path.join(SITE_ROOT, "conf/online.cfg")])

DEBUG = cp.getboolean(SECTION, 'debug', default=True)
EXCEPTION_DEBUG = cp.getboolean(SECTION, 'exception_debug', default=False)
MONGO_CONFIG = cp.get(SECTION, 'mongo_config', default=None)
LOG_ROOT = cp.get(SECTION, 'log_root', default='/tmp')
LOG_FILE = os.path.join(LOG_ROOT, 'online_admin.log')
LOG_ERR_FILE = os.path.join(LOG_ROOT, 'online_admin.err')
PAGE_LIMIT = int(cp.get(SECTION, 'page_limit', default=10))
HTTP_PORT = cp.get(SECTION, 'http_port', default=6000)

API_PREF = '/auth'

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
        'auth_service': {
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
        'auth_service': {
            'handlers': ['auth_service', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'armory': {
            'handlers': ['auth_service', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

NAV_DICT = {
    'square_console': "环信",
    'provision_services': "预置数据",
    'auth': "用户管理",
}

# lastly, config logging
logging.config.dictConfig(LOGGING_DICT)
