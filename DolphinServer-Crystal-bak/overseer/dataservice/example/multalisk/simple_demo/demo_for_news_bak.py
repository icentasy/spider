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


DEBUG = True
APP_CONF = {
    'model': [{"model_id": "1001", "db_conn": "mysql://root:123456@127.0.0.1:3306/stat_EN?charset=utf8"}],
    'view': {
        'news001': {
            'charts': [
                {
                    'model_id': '1001',
                    'x_dimension': 'priority',
                    'y_dimension': [
                        {"name": "recommend_contribute_by_priority", "value": {"field_group": "recommend_click/recommend_show", "func": "multi_sum"}},
                    ],
                    'default_q': {"filters": [{"name": "recommend_show", "op": "!=", "val": "0"}]},
                    'chart_type': ChartType.Pie
                },
                {
                    'model_id': '1001',
                    'x_dimension': 'priority',
                    'y_dimension': [
                        {
                            "name": "recommend_contribute_by_category_priority",
                            "value": {
                                "field_group": "recommend_click/recommend_show",
                                "func": "multi_sum_groupby",
                                "groupby": "category"
                            }
                        },
                    ],
                    'default_q': {"filters": [{"name": "recommend_show", "op": "!=", "val": "0"}]},
                    'chart_type': ChartType.Bar
                },
                {
                    'model_id': '1001',
                    'x_dimension': 'priority',
                    'y_dimension': [
                        {
                            "name": "recommend_contribute_by_source_priority",
                            "value": {
                                "field_group": "recommend_click/recommend_show",
                                "func": "multi_sum_groupby",
                                "groupby": "source"
                            }
                        },
                    ],
                    'default_q': {"filters": [{"name": "recommend_show", "op": "!=", "val": "0"}]},
                    'chart_type': ChartType.Bar
                }
            ],
            'filters': {
                'multi': [
                    {
                        'model_id': '1001',
                        'name': 'priority'
                    },
                    {
                        'model_id': '1001',
                        'name': 'category'
                    },
                    {
                        'model_id': '1001',
                        'name': 'source'
                    },
                ]
            }
        },
        'news002': {
            'charts': [
                {
                    'model_id': '1001',
                    'x_dimension': 'source',
                    'y_dimension': [
                        {
                            "name": "recommend_contribute_by_source_category_priority",
                            "value": {
                                "field_group": "recommend_click/recommend_show",
                                "func": "multi_sum_groupby",
                                "groupby": "source"
                            }
                        },
                    ],
                    'default_q': {"filters": [
                        {"name": "recommend_show", "op": "!=", "val": "0"},
                        {"name": "priority", "op": "==", "val": 8},
                        {"name": "category", "op": "==", "val": "6"},
                    ]},
                    'chart_type': ChartType.Pie
                }
            ],
            'filters': {
                'multi': [
                    {
                        'model_id': '1001',
                        'name': 'priority'
                    },
                    {
                        'model_id': '1001',
                        'name': 'category'
                    },
                    {
                        'model_id': '1001',
                        'name': 'source'
                    },
                ]
            }
        }
    }
}


app = multalisk.Multalisk(__name__)
app.init_conf(APP_CONF, debug=DEBUG)


class News_Report_ru(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1001"
    __tablename__ = "report_test_ru_ru"
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


app.run(host='0.0.0.0')
