# -*- coding:utf-8 -*-
import logging

from armory.marine.json import ArmoryJson
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import CONTENT_NOT_FOUND, PARAM_ERROR

from tuangou.api import request, app
from tuangou.view.deal import get_deal_list
from tuangou.utils.common import get_valid_params
from tuangou.utils.constant import DEAL_PARAM
from tuangou.decorator import exception_handler, perf_logging, access_control
from tuangou.settings import API_PREF


_LOGGER = logging.getLogger(__name__)

API_DEAL = API_PREF + '/deal/<city>/<dealtype>'


@app.route(API_DEAL, methods=['GET', ])
@access_control
@exception_handler
@perf_logging
def deal_info(city, dealtype):
    # check args
    args = get_valid_params(request.args, DEAL_PARAM)
    # view logic
    deal_obj = get_deal_list(city, dealtype, args)
    if deal_obj:
        return json_response_ok(deal_obj)
    else:
        return json_response_error(CONTENT_NOT_FOUND, {}, msg='empty res list')
