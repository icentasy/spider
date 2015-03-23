# -*- coding: utf-8 -*-
"""
    Simple demo for multalisk
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Http Request:
        http://x.x.x.x:5000/multalisk/report?app=1001&x_dimension=date&y_dimension=[{"name":"sum_uv","value":{"name":"uv","func":"sum"}}]&q={"filters":[{"name":"date","val":"2014-12-01","op":">="},{"name":"date","op":"<=","val":"2014-12-08"}]}

"""

import multalisk
from multalisk.model import orm
from multalisk.core.feature import ChartType


DEBUG = True
APP_CONF = {
    'model': [{"model_id": "1001", "db_conn": "mysql://xshu:Baina-shuxiang@172.16.77.4:3306/app_id146?charset=utf8"}],
    'view': {
        'news001': {
            'charts': [
                {
                    'model_id': '1001',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {"name": "uv_by_version", "value": {"field": "uv", "func": "sum_groupby", "groupby": "version"}},
                        {"name": "uv_by_action", "value": {"field": "uv", "func": "sum_groupby", "groupby": "action"}},
                    ],
                    'default_q': {"filters": [{"name": "date", "op": "eq", "val": "2014-12-01"}]},
                    'chart_type': ChartType.Pie
                }
            ],
            'filters': {
                'cascade': {
                    'model_id': '1001',
                    'name': 'location',
                    'children': {
                        'name': 'version'
                    }
                },
                'multi': [
                    {
                        'model_id': '1001',
                        'name': 'action'
                    }
                ]
            }
        }
    }
}


app = multalisk.Multalisk(__name__)
app.init_conf(APP_CONF, debug=DEBUG)


class Provision(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1001"
    __tablename__ = "preload_data_view"
    date = orm.Column(orm.Date, primary_key=True)
    network = orm.Column(orm.VARCHAR(50), primary_key=True)
    location = orm.Column(orm.VARCHAR(50), primary_key=True)
    version = orm.Column(orm.VARCHAR(50), primary_key=True)
    action = orm.Column(orm.VARCHAR(50), primary_key=True)
    label = orm.Column(orm.VARCHAR(255), primary_key=True)
    uv = orm.Column(orm.Integer)


app.run(host='0.0.0.0')
