# -*- coding:utf-8 -*-
"""
    multalisk.api.statistic
    ~~~~~~~~~~~~~~~~~~~~~~~

    Provide report api function

"""
from pylon.frame import request
from multalisk.view.report import fetch_report
from multalisk.utils.common import get_valid_params
from multalisk.utils.constant import REPORT_PARAM
from multalisk.utils.http_json import json_response_ok
from multalisk.decorator import (check_session, exception_handler,
                                 perf_logging, access_control)


@exception_handler
@access_control
@perf_logging
@check_session
def report():
    """report API.
    This API is used for fetch report data from multiple database,
    including mysql/hive/mongo.

    Request URL: api/mutalisk/report

    HTTP Method: GET

    Parameter:
        - app: app id, eg:1001  app id will be defined by different bussiness
                                one app id is related to one Data Model
        - q: query string, eg:
             {"filters":[{"name":"user_name","val":"xshu","op":"like"}]}
        - x_dimension: x dimension,a string field, eg: date
        - y_dimension: y dimension,a json dict defines the output feature
        - order: 1:ASC, -1:DESC
        - type: output type, 1:json 2:excel 3:csv

    Return:
        {
            "status": 0,
            "msg": "",
            "data":{
                "filters": {},
                "items": [
                    {
                        "x_val": "20140101",
                        "y_val": {
                            "US": 80,
                            "CN": 20
                        }
                    },
                    {
                        ...
                    }
                    ...
                ]
            }
        }
    """
    # check args
    args = get_valid_params(request.args, REPORT_PARAM)
    # view logic
    feature_list = fetch_report(args['app'], args['x_dimension'],
                                args['y_dimension'], args['q'])
    return json_response_ok(feature_list)
