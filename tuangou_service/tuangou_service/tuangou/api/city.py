# -*- coding:utf-8 -*-
import logging

from armory.marine.json import ArmoryJson
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import CONTENT_NOT_FOUND, PARAM_ERROR

from tuangou.api import request, app
from tuangou.view.city import get_city_list
from tuangou.utils.common import get_valid_params
from tuangou.decorator import exception_handler, perf_logging, access_control
from tuangou.settings import API_PREF


_LOGGER = logging.getLogger(__name__)

API_HOT_CITY = API_PREF + '/city'


@app.route(API_HOT_CITY, methods=['GET', ])
@access_control
@exception_handler
@perf_logging
def hot_city():
    city_obj = get_city_list()
    if city_obj:
        return json_response_ok(city_obj)
    else:
        return json_response_error(CONTENT_NOT_FOUND, {}, msg='empty res list')
