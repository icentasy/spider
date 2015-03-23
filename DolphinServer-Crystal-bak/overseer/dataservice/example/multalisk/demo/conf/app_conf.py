# -*- coding: utf-8 -*-
from multalisk.core.feature import ChartType
from multalisk.utils.custom_filter import n_days_ago


APP_CONF = {
    'model': [{
        "model_id": "1001",
        "db_conn": "mysql://root:123456@127.0.0.1:3306/stat_EN?charset=utf8"
    }],
    'view': {
        'news_tr': {
            'charts': [{
                'model_id': '1001',
                'x_dimension': 'priority',
                'y_dimension': [{
                    "name": "recommend contribute by priority",
                    "value": {
                        "field_group": "recommend_click/recommend_show",
                        "func": "multi_sum_ratio"
                    }
                }, {
                    "name": "home contribute by priority",
                    "value": {
                        "field_group": "home_click/home_show",
                        "func": "multi_sum_ratio",
                    }
                }],
                'default_q': {
                    "filters": [{
                        "name": "recommend_show",
                        "op": "!=",
                        "val": "0"
                    }, {
                        "name": "home_show",
                        "op": "!=",
                        "val": "0"
                    }, {
                        "name": "date",
                        "op": "==",
                        "val": (n_days_ago, [15, '%Y%m%d']),
                    }],
                },
                'chart_type': ChartType.Pie
            }, {
                'model_id': '1001',
                'x_dimension': 'date',
                'y_dimension': [{
                    "name": "recommend click count",
                    "value": {
                        "field": "recommend_click",
                        "func": "sum"
                    },
                }, {
                    "name": "top click count",
                    "value": {
                        "field": "top_click",
                        "func": "sum",
                    }
                }],
                'default_q': {
                    "filters": []
                },
                'chart_type': ChartType.Bar
            }],
            'filters': {
                'multi': [{
                    'model_id': '1001',
                    'name': 'priority'
                }, {
                    'model_id': '1001',
                    'name': 'category'
                }, {
                    'model_id': '1001',
                    'name': 'source'
                }]
            }
        }
    }
}
