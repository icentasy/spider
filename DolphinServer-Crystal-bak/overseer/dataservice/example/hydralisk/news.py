import os
import logging.config

from hydralisk.app import Hydralisk
from multalisk.core.feature import ChartType
from multalisk.model import orm
from multalisk.utils.custom_filter import n_days_ago
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
        "model_id": "1006",
        "db_conn": "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"
    }, {
        "model_id": "2006",
        "db_conn": "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"
    }, {
        "model_id": "3006",
        "db_conn": "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"
    }, {
        "model_id": "4006",
        "db_conn": "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"
    }, {
        "model_id": "1003",
        "db_conn": "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"
    }, {
        "model_id": "2003",
        "db_conn": "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"
    }, {
        "model_id": "3003",
        "db_conn": "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"
    }, {
        "model_id": "4003",
        "db_conn": "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"
    }],
    'view': {
        'click_top100': {
            'charts': [{
                'model_id': '1006',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '2006',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '3006',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }, {
                'model_id': '4006',
                'x_dimension': 'news_id',
                'y_dimension': [{
                    "name": "total_click",
                    "value": {
                        "field": "total_click",
                        "func": "no_func"
                    }
                }, {
                    "name": "category",
                    "value": {
                        "field": "category",
                        "func": "no_func"
                    }
                }, {
                    "name": "priority",
                    "value": {
                        "field": "priority",
                        "func": "no_func"
                    }
                }],
                'order_by': ('total_click', True),
                'default_q': {
                    "filters": [{
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [1, '%Y-%m-%d'])
                    }],
                    "order_by": [
                        {"field": "total_click", "direction": "desc"}
                    ],
                    "limit": 100
                },
                'chart_type': ChartType.Table,
            }],
            'schedule': '40 2 * * *',
            'template': os.path.join(CUR_DIR, 'click_top100.html'),
            'mail_to': ['tryao@bainainfo.com', 'xshu@bainainfo.com']
        },
        'category_click_rate': {
            'charts': [{
                'model_id': '1003',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '2003',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '3003',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '4003',
                'x_dimension': 'category',
                'y_dimension': [{
                    'name': 'category_click_rate',
                    'value': {
                        'field_group': 'top_click+home_click+push_click',
                        'func': 'sum_ratio'
                    },
                }],
                'default_q': {
                    'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]
                },
                'chart_type': ChartType.Pie
            }],
            'schedule': '40 2 * * *',
            'template': os.path.join(CUR_DIR,
                                     'category_click_rate.html'),
            'mail_to': ['tryao@bainainfo.com', 'xshu@bainainfo.com']
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


class News_report_origin_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1001"
    __tablename__ = "report_origin_tr_tr"
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
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1002"
    __tablename__ = "report_type_sum_tr_tr"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1003"
    __tablename__ = "report_category_sum_tr_tr"
    category = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2003"
    __tablename__ = "report_category_sum_ru_ru"
    category = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_jp(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3003"
    __tablename__ = "report_category_sum_ja_jp"
    category = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ar(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4003"
    __tablename__ = "report_category_sum_ar_sa"
    category = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1004"
    __tablename__ = "report_priority_sum_tr_tr"
    priority = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1005"
    __tablename__ = "report_source_sum_tr_tr"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_tr(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1006"
    __tablename__ = "report_news_sum_tr_tr"
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
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "2006"
    __tablename__ = "report_news_sum_ru_ru"
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
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_jp(object):
    __metaclass__ = MetaSQL
    __modelid__ = "3006"
    __tablename__ = "report_news_sum_ja_jp"
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
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ar(object):
    __metaclass__ = MetaSQL
    __modelid__ = "4006"
    __tablename__ = "report_news_sum_ar_sa"
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
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)

app.run(worker_num=1)
