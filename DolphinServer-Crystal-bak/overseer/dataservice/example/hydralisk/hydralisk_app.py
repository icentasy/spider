import os
import logging.config

from hydralisk.app import Hydralisk
from multalisk.core.feature import ChartType
from multalisk.model import orm
from multalisk.model.base import MetaSQL


DEBUG = True
LOG_FILE = '/tmp/hydralisk.log'
LOG_ERR_FILE = '/tmp/hydralisk.err'
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

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
        'overseer': {
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
            'handlers': ['overseer', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'multalisk': {
            'handlers': ['overseer', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'hydralisk': {
            'handlers': ['overseer', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'armory': {
            'handlers': ['overseer', 'file', 'err_file'
                         ] if DEBUG else ['file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# lastly, config logging
logging.config.dictConfig(LOGGING_DICT)

APP_CONF = {
    'model': [{
        "model_id": "1001",
        "db_conn": "mysql://root:123456@127.0.0.1:3306/stat_EN?charset=utf8"
    }],
    'view': {
        'news_ru': {
            'charts': [{
                'model_id': '1001',
                'x_dimension': 'category',
                'y_dimension': [{
                    "name": "recommend_click_by_category",
                    "value": {
                        "field_group": "recommend_click",
                        "func": "sum"
                    }
                }],
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": "20150225"
                    }]
                },
                'chart_type': ChartType.Line,
            }, {
                'model_id': '1001',
                'x_dimension': 'category',
                'y_dimension': [{
                    "name": "recommend_click_by_category",
                    "value": {
                        "field_group": "recommend_click",
                        "func": "sum"
                    }
                }],
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "<=",
                        "val": "20150227"
                    }]
                },
                'chart_type': ChartType.Table | ChartType.Csv

            }],
            'schedule': 60,
            'template': os.path.join(CUR_DIR, 'mail_template.html'),
            'mail_to': ['tryao@bainainfo.com']
        }
    },
    'mail': {
        'server': 'smtp.gmail.com:587',
        'user': 'backend.service.alert',
        'passwd': 'backend.P@55word',
        'from': 'Dolphin Service Statistics<backend.service.alert@gmail.com>',
        'to': ['xshu@bainainfo.com']
    },
    'render': {
        'server': 'http://127.0.0.1:3005',
        'upload': False,
    }
}


app = Hydralisk('test')
app.init_conf(APP_CONF)


class News_Report_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1001"
    __tablename__ = "report_test_tr_tr"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30))


app.run(worker_num=1)
