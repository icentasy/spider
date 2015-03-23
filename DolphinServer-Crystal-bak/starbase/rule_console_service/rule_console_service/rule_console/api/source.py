# -*- coding:utf-8 -*-
import logging
import json

from rule_console.settings import MONGO_CONFIG
from rule_console.api import request, app
from rule_console.model.source import Source
from rule_console.view.source import (
    source_info_list, save_source_info, get_source_by_id,
    update_source_info, delete_source_info)
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_REQUIRED, PARAM_ERROR
from rule_console.decorator import exception_handler, access_control
from rule_console.utils.common import search_cond
from rule_console.utils.respcode import (
    DATA_RELETED_BY_OTHER, DUPLICATE_FIELD)


_LOGGER = logging.getLogger(__name__)

API_GET_SOURCE = '/<appname>/rule/v1/source/list'
API_ADD_SOURCE = '/<appname>/rule/v1/source/add'
API_EDIT_SOURCE = '/<appname>/rule/v1/source/edit'
API_UPDATE_SOURCE = '/<appname>/rule/v1/source/update'
API_DELETE_SOURCE = '/<appname>/rule/v1/source/delete'


@app.route(API_GET_SOURCE, methods=['GET', ])
@exception_handler
@access_control
def source_list(appname):
    '''
        list api for show source list.
        Request URL:  /appname/rule/source/list
        Http Method:  GET
        Parameters : index, limit
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"ofw"
                    },
                    {
                        "id": 2,
                        "title":"ofw1"
                    }
                ]
            }
        }

     '''
    # check appname
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="can not find appname")

    # view logic
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    searchKeyword = request.args.get("searchKeyword")
    cond = {}
    if searchKeyword:
        cond = search_cond(searchKeyword, Source.search_fields)
    sort = [("last_modified", -1)]
    data = source_info_list(
        appname, cond, sort=sort, page=index, page_size=limit)
    return json_response_ok(data, msg="")


@app.route(API_ADD_SOURCE, methods=['POST', "OPTIONS"])
@exception_handler
@access_control
def add_source_info(appname):
    '''
        create api to add source.
        Request URL:  /appname/rule/source/add
        Http Method: POST
        Parameters :
        {
           "id": 1,
           "title": "ofw1"
        }
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"ofw"
                    },
                    {
                        "id": 2,
                        "title":"ofw1"
                    }
                ]
            }
        }

    '''
    # check appname
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # check request json format
    try:
        source_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("add operator para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check required args
    if "title" not in source_obj:
        return json_response_error(PARAM_REQUIRED, msg="not param:title")

    # check if source title duplicate
    title = source_obj.get("title")
    if Source.find_one_source(appname, {"title": title}):
        return json_response_error(
            DUPLICATE_FIELD, msg="the locale title exist")

    # add logic
    save_source_info(appname, title)

    cond = {}
    sort = [("last_modified", -1)]
    data = source_info_list(appname, cond, sort=sort)
    return json_response_ok(data)


@app.route(API_EDIT_SOURCE, methods=['GET', ])
@exception_handler
@access_control
def edit_source(appname):
    '''
        this api is used to view one source
        Request URL:  /appname/rule/source/edit
        Http Method: GET
        Parameters : id
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"ofw",
            }
        }

     '''
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # check required args
    args = request.args
    if "id" not in args:
        return json_response_error(PARAM_REQUIRED, msg="not param:id")

    # check if source id in db
    src_id = int(args["id"])
    if not Source.find_one_source(appname, {"_id": src_id}):
        return json_response_error(
            PARAM_ERROR, msg="the source not in db")

    # view logic
    fields = {"first_created": 0, "last_modified": 0}
    data = get_source_by_id(appname, src_id, fields)
    return json_response_ok(data)


@app.route(API_UPDATE_SOURCE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def modify_source(appname):
    '''
        this api is used to modify one source
        Request URL:  /appname/rule/source/update
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
                "title":"ofw",
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
    for arg in ["id", 'title']:
        if arg not in data_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # check if source id in db
    src_id = int(data_obj["id"])
    if not Source.find_one_operator(appname, {"_id": src_id}):
        return json_response_error(
            PARAM_ERROR, msg="the source not in db")

    # check if source title duplicate
    title = data_obj["title"]
    src_info = Source.find_one_source(appname, {"title": title})
    if src_info and src_info["_id"] != src_id:
        return json_response_error(
            DUPLICATE_FIELD, msg="the source title exist")

    # update logic
    new_source = update_source_info(appname, src_id, data_obj)
    _LOGGER.info("update source:%s success", new_source)
    return json_response_ok(new_source)


@app.route(API_DELETE_SOURCE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def delete_source(appname):
    '''
        this api is used to delete source,
        when one source refered, the source cannot removed
        Request URL:  /appname/rule/source/delete
        HTTP Method: POST
        Parameters:
            {
                "items":[3, 2]
            }
        Return:
            {
                "status": 0,
                "msg": "delete source success",
                "data": {
                    "failed": [],
                    "success": [{"id": 3}, {"id": 2}]
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
        _LOGGER.error("delete source para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # delete logic
    sids = data_obj.get("items")
    data = {}
    data["success"], data["failed"], invalid = delete_source_info(
        appname, sids)
    if invalid:
        return json_response_error(
            PARAM_ERROR, msg="invalid source id,check parameters")
    if data["failed"]:
        return json_response_error(DATA_RELETED_BY_OTHER, data)
    else:
        return json_response_ok(data, msg="")
