# -*- coding:utf-8 -*-
import logging
import json

from rule_console.settings import MONGO_CONFIG
from rule_console.api import request, app
from rule_console.view.refered_info import (
    add_refered_info, delete_refered_info)
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import (
    PARAM_REQUIRED, METHOD_ERROR, PARAM_ERROR)
from rule_console.decorator import exception_handler, access_control


_LOGGER = logging.getLogger(__name__)


API_ADD_REFER = '/<appname>/rule/v1/referInfo/add'
API_DELETE_REFER = '/<appname>/rule/v1/referInfo/delete'


@app.route(API_ADD_REFER, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def refer_info_add(appname):
    '''
        create api to add refered info.
        Request URL:  /appname/rule/referInfo/add
        Http Method: POST
        Parameters :
        {
           "target_field": "rule",
           "target_id": 1,
           "refered_data":{
                "modelName" : "category",
                "id" : 1,
                "modelField" : "rule"
            }
        }
        Return :
        {
            "status":0
            "data":{}
        }

    '''
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # check request json format
    try:
        refered_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("add refer info para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check required args
    required_list = ['target_field', 'target_id', 'refered_data']
    for arg in required_list:
        if arg not in refered_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # get required args
    target_field = refered_obj.get("target_field")
    target_id = int(refered_obj.get("target_id"))
    refered_data = refered_obj.get("refered_data")
    old_id = refered_obj.get("old_target_id")

    # add logic
    add_refered_info(
        appname, target_field, target_id, refered_data, old_id)

    return json_response_ok({}, msg="add refered info  success")


@app.route(API_DELETE_REFER, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def refer_info_delete(appname):
    '''
        this api is used to de refered info,
        Request URL:  /appname/rule/referInfo/delete
        HTTP Method: POST
        Parameters:
        {
           "target_field": "rule",
           "target_id": 1,
           "unrefered_data":{
                "modelName" : "category",
                "id" : 1,
                "modelField" : "rule"
            }
        }
        Return:
            {
                "status": 0,
                "msg": "de refered info success",
                "data": {}
    '''
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # check request json format
    try:
        refered_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("delete refer para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check required args
    required_list = ['target_field', 'target_id', 'unrefered_data']
    for arg in required_list:
        if arg not in refered_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)
    target_field = refered_obj.get("target_field")
    target_id = int(refered_obj.get("target_id"))
    unrefered_data = refered_obj.get("unrefered_data")

    delete_refered_info(appname, target_field, target_id, unrefered_data)
    return json_response_ok({})
