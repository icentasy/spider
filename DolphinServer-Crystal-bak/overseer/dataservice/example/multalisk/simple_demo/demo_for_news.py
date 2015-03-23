# -*- coding: utf-8 -*-
"""
    Simple demo for multalisk
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Http Request:
        http://x.x.x.x:5000/multalisk/report/news001?q={}

"""

import multalisk
from multalisk.model import orm
from multalisk.core.feature import ChartType
from multalisk.cache import init_cache
from multalisk.utils.custom_filter import n_days_ago


DEBUG = True
APP_CONF = {
    'model': [{
        "model_id": "1001",
        "db_conn": "mysql://root:123456@127.0.0.1:3306/stat_EN?charset=utf8"
    }],
    'view': {
        'recommend_view_01': {
            'charts': [
                {
                    'model_id': '1001',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "recommend_click",
                            "value": {
                                "field": "recommend_click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y%m%d', 'Asia/Shanghai']),
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        },
        'recommend_view_02': {
            'charts': [
                {
                    'model_id': '1001',
                    'x_dimension': 'priority',
                    'y_dimension': [
                        {
                            'name': 'recommend_click_by_priority',
                            'value': {
                                'field': 'recommend_click',
                                'func': 'sum'
                            }
                        },
                        {
                            'name': 'ctr_by_priority',
                            'value': {
                                'field_group': 'recommend_click/recommend_show',
                                'func': 'multi_sum'
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'recommend_show',
                        'op': '!=',
                        'value': 0,
                    }, {
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y%m%d', 'Asia/Shanghai']),
                    }]},
                    'chart_type': ChartType.Pie
                },
                {
                    'model_id': '1001',
                    'x_dimension': 'category',
                    'y_dimension': [
                        {
                            'name': 'recommend_click_by_category',
                            'value': {
                                'field': 'recommend_click',
                                'func': 'sum'
                            }
                        },
                        {
                            'name': 'ctr_by_category',
                            'value': {
                                'field_group': 'recommend_click/recommend_show',
                                'func': 'multi_sum'
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'recommend_show',
                        'op': '!=',
                        'value': 0,
                    }, {
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y%m%d', 'Asia/Shanghai']),
                    }
                    ]},
                    'chart_type': ChartType.Pie
                },
                {
                    'model_id': '1001',
                    'x_dimension': 'source',
                    'y_dimension': [
                        {
                            'name': 'recommend_click_by_source',
                            'value': {
                                'field': 'recommend_click',
                                'func': 'sum'
                            }
                        },
                        {
                            'name': 'ctr_by_source',
                            'value': {
                                'field_group': 'recommend_click/recommend_show',
                                'func': 'multi_sum'
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'recommend_show',
                        'op': '!=',
                        'value': 0,
                    }, {
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y%m%d', 'Asia/Shanghai']),
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }
            ],
            'filters': {}
        },
        'top_view': {
            'charts': [
                {
                    'model_id': '1001',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {"name": "total_click", "value": {
                            "field_group": "top_click+home_click+push_click", "func": "sum"}},
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '==',
                        'val': '20150225',
                    }, ]},
                    'chart_type': ChartType.Table
                }
            ],
            'filters': {}
        }
    }
}


app = multalisk.Multalisk(__name__)
app.init_conf(APP_CONF, debug=DEBUG)


class News_Report_ru(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1001"
    __tablename__ = "report_test_tr_tr"
    id = orm.Column(orm.Integer, primary_key=True)
    news_id = orm.Column(orm.Integer)
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

objs = News_Report_ru.query
print objs

init_cache(host='127.0.0.1', port=6379)

app.run(host='0.0.0.0', port=5002)
