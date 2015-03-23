# -*- coding:utf-8 -*-
import os
import re
import logging.config

from armory.marine.json import ArmoryJson
from armory.marine.parser import FreeConfigParser


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


# firstly, load config file to initialize constant
SECTION = 'resource-console-service'
cp = FreeConfigParser()
cp.read([os.path.join(SITE_ROOT, "conf/online.cfg")])

DEBUG = cp.getboolean(SECTION, 'debug', default=True)
EXCEPTION_DEBUG = cp.getboolean(SECTION, 'exception_debug', default=False)
MONGO_CONFIG = cp.get(SECTION, 'mongo_config', default=None)
LOG_ROOT = cp.get(SECTION, 'log_root', default='/tmp')
LOG_FILE = os.path.join(LOG_ROOT, 'online_admin.log')
LOG_ERR_FILE = os.path.join(LOG_ROOT, 'online_admin.err')
PAGE_LIMIT = int(cp.get(SECTION, 'page_limit', default=10))
HTTP_PORT = cp.get(SECTION, 'http_port', default=5000)
HOST = cp.get(SECTION, 'host')
production = cp.getboolean(SECTION, 'admin_production')
envs = ('ec2', 'local') if production else ('local', )
REMOTEDB_SETTINGS = {}
for env in envs:
    conf_parts = re.split(r'[:/]', cp.get(SECTION, 'db_conn_%s' % env))
    conf_statics = cp.get(SECTION, 'web_env_%s' % env).split(',')
    conf_domain = cp.get(SECTION, 'domain_env_%s' % env)
    conf_s3 = cp.get(SECTION, 's3_env_%s' % env)
    REMOTEDB_SETTINGS[env] = {
        'host': conf_parts[0],
        'name': conf_parts[2],
        'port': int(conf_parts[1]),
        'statics': conf_statics,
        'domain': conf_domain,
        's3_remote': conf_s3
    }

API_PREF = '/square_console'
MEDIA_ROOT = '/var/app/data/resource_console_service'
S3_DOMAIN = 'http://opsen-static.dolphin-browser.com/resources'

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
        'resource_console': {
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
        'resource_console': {
            'handlers': ['resource_console', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# lastly, config logging
logging.config.dictConfig(LOGGING_DICT)
