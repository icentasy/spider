# -*- coding:utf-8 -*-
import os
import json
import logging.config

from multalisk.utils.parser import FreeConfigParser


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


# firstly, load config file to initialize constant
SECTION = 'multalisk-service'
cp = FreeConfigParser()
cp.read([os.path.join(SITE_ROOT, "conf/online.cfg")])

DEBUG = cp.getboolean(SECTION, 'debug', default=True)
EXCEPTION_DEBUG = cp.getboolean(SECTION, 'exception_debug', default=False)
LOG_ROOT = cp.get(SECTION, 'log_root', default='/tmp')
LOG_FILE = os.path.join(LOG_ROOT, 'online.log')
LOG_ERR_FILE = os.path.join(LOG_ROOT, 'online.err')


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
        'multalisk': {
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
        'demo': {
            'handlers': ['multalisk', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'multalisk': {
            'handlers': ['multalisk', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'armory': {
            'handlers': ['multalisk', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# lastly, config logging
logging.config.dictConfig(LOGGING_DICT)
