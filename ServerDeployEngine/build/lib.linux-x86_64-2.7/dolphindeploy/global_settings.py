'''
Default settings of Dolphin Server deploy.

Created on Dec 12, 2011

@author: chzhong
'''
import os
import tempfile

PROJECT_NAME = None
APP_DIR = '/var/app'

TEMP_DIR = tempfile.gettempdir()
BUILD_TEMP = os.path.join(TEMP_DIR, 'build')
DIST_TEMP = os.path.join(TEMP_DIR, 'dist')

CONF_ROOT = os.path.join(os.getcwd(), 'conf')
DEFAULT_CONF_DIR = os.path.join(CONF_ROOT, 'default')

VERSION_CONTROL = 'dolphindeploy.svn'

DEFAULT_CONF_EXT_PATTERN = (
    '.conf',
    '.cfg',
    '.xml',
    '.csv',
    '.crt',
    '.key',
    '.pem',
    '.pub',
    '.nginx',
    '.logrotate',
    '.cron',
    '.mysql',
)

EXTRA_EXT_PATTERN = ()

DEFAULT_CONF_NAME_PATTERN = (
    'settings2.py',
    'version',
    'files',
    'passwd',
    's3cfg'
)

EXTRA_CONF_NAME_PATTERN = ()

CONF_EXT_PATTERN = DEFAULT_CONF_EXT_PATTERN + EXTRA_EXT_PATTERN
CONF_NAME_PATTERN = DEFAULT_CONF_NAME_PATTERN + EXTRA_CONF_NAME_PATTERN

HERE = os.path.abspath(os.path.dirname(__file__))

GC_LIB_PATH = os.path.join(HERE, '../libs/compiler.jar')
YUI_LIB_PATH = os.path.join(HERE, '../libs/yuicompressor.jar')

BUILD_HANDLER_CONFIG = (
    'dolphindeploy.handlers.ConfigurationFileHandler',
    'dolphindeploy.handlers.GoogleClosureJavaScriptCompiler'
)

ROLE_APPS_TABLE = None
ROLE_ALIAS = None

