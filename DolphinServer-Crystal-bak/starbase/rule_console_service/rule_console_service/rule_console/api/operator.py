# -*- coding:utf-8 -*-
import logging
import json


from rule_console.settings import MONGO_CONFIG
from rule_console.model.operator import Operator
from rule_console.api import request, app
from rule_console.view.operator import (
    save_operator_info, operator_info_list, get_operator_by_id,
    update_operator_info, delete_operator_info)
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_REQUIRED, PARAM_ERROR
from rule_console.decorator import exception_handler, access_control
from rule_console.utils.common import search_cond
from rule_console.utils.respcode import (
    DATA_RELETED_BY_OTHER, DUPLICATE_FIELD)


_LOGGER = logging.getLogger(__name__)

API_GET_OPERATOR = '/<appname>/rule/v1/operator/list'
API_ADD_OPERATOR = '/<appname>/rule/v1/operator/add'
API_EDIT_OPERATOR = '/<appname>/rule/v1/operator/edit'
API_UPDATE_OPERATOR = '/<appname>/rule/v1/operator/update'
API_DELETE_OPERATOR = '/<appname>/rule/v1/operator/delete'


@app.route(API_GET_OPERATOR, methods=['GET', ])
@exception_handler
@access_control
def operator_list(appname):
    '''
        list api for show operator list.
        Request URL:  /appname/rule/operator/list
        Http Method:  GET
        Parameters : index, limit
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"移动",
                        "code": "00,02"
                    },
                    {
                        "id": 2,
                        "title":"联通",
                        "code": "01"
                    }
                ]
            }
        }

     '''
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # view logic
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    searchKeyword = request.args.get("searchKeyword")
    cond = {}
    if searchKeyword:
        cond = search_cond(searchKeyword, Operator.search_fields)
    sort = [("last_modified", -1)]
    data = operator_info_list(
        appname, cond, sort=sort, page=index, page_size=limit)
    return json_response_ok(data, msg="")


@app.route(API_ADD_OPERATOR, methods=['POST', "OPTIONS"])
@exception_handler
@access_control
def add_operator_info(appname):
    '''
        create api to add operator.
        Request URL:  /appname/rule/operator/add
        Http Method: POST
        Parameters : Json
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"移动",
                        "code": "00,02"
                    },
                    {
                        "id": 2,
                        "title":"联通",
                        "code": "01"
                    }
                ]
            }
        }

    '''
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # check request json format
    try:
        operator_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("add operator para except:%s", expt)
        return json_response_error(
            PARAM_ERROR,
            msg="json loads error,check parameters format")

    # check required args
    for arg in ['title', 'code']:
        if arg not in operator_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # check if operator title duplicate
    title = operator_obj.get("title")
    if Operator.find_one_operator(appname, {"title": title}):
        return json_response_error(
            DUPLICATE_FIELD, msg="the locale title exist")

    # add logic
    code = operator_obj.get("code")
    save_operator_info(appname, title, code)

    cond = {}
    sort = [("last_modified", -1)]
    data = operator_info_list(appname, cond, sort=sort)
    return json_response_ok(data)


@app.route(API_EDIT_OPERATOR, methods=['GET', ])
@exception_handler
@access_control
def edit_operator(appname):
    '''
        this api is used to view one operator
        Request URL:  /appname/rule/opeartor/edit
        Http Method: GET
        Parameters : id
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"联通",
                "code": "01"
            }
        }

     '''
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    args = request.args

    # check required args
    if "id" not in args:
        return json_response_error(PARAM_REQUIRED, msg="not param:id")

    # check if operator id in db
    op_id = int(args["id"])
    if not Operator.find_one_operator(appname, {"_id": op_id}):
        return json_response_error(PARAM_ERROR, msg="the operator not in db")

    # view logic
    fields = {"first_created": 0, "last_modified": 0}
    data = get_operator_by_id(appname, op_id, fields)
    return json_response_ok(data)


@app.route(API_UPDATE_OPERATOR, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def modify_operator(appname):
    '''
        this api is used to modify one locale
        Request URL:  /appname/rule/locale/update
        HTTP Method:POST
        Parameters:
        {
           "id": 1,
           "title": "xxxx"
        }
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"zh_CN",
            }
        }
        '''
    # check appname
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # check request json format
    try:
        data_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("modify operator para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check required args
    for arg in ["id", 'title', 'code']:
        if arg not in data_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # check if operator id in db
    op_id = int(data_obj["id"])
    if not Operator.find_one_operator(appname, {"_id": op_id}):
        return json_response_error(PARAM_ERROR, msg="the operator not in db")

    # check if operator title duplicate
    title = data_obj["title"]
    op_info = Operator.find_one_operator(appname, {"title": title})
    if op_info and op_info["_id"] != op_id:
        return json_response_error(
            DUPLICATE_FIELD, msg="the locale title exist")

    # view logic
    new_operator = update_operator_info(appname, op_id, data_obj)
    _LOGGER.info("update operator:%s success", new_operator)
    return json_response_ok(new_operator)


@app.route(API_DELETE_OPERATOR, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def delete_operator(appname):
    '''
        this api is used to delete operator,
        when one operator refered, the operator cannot removed
        Request URL:  /appname/rule/operator/delete
        HTTP Method: POST
        Parameters:
            {
                "items":[3, 2]
            }
        Return:
            {
                "status": 0,
                "msg": "delete operator success",
                "data": {
                    "failed": [],
                    "success": [{"id": 3}, {"id": 2}]
                }
    '''
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # check request json format
    try:
        data_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("delete package para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # delete logic
    oids = data_obj.get("items")
    data = {}
    data["success"], data["failed"], invalid = delete_operator_info(
        appname, oids)
    if invalid:
        return json_response_error(PARAM_ERROR, msg="invalid operator id")
    if data["failed"]:
        return json_response_error(DATA_RELETED_BY_OTHER, data)
    else:
        return json_response_ok(data, msg="")
