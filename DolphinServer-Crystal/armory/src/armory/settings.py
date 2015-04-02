import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DEBUG = True
LOG_ROOT = os.path.join(ROOT_PATH, 'log')
LOG_FILE = os.path.join(LOG_ROOT, 'info.log')
LOG_ERR_FILE = os.path.join(LOG_ROOT, 'error.log')

LOGGING = {
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
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'formatter': 'simple',
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
        'armory': {
            'handlers': ['console', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
