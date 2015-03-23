# -*- coding:utf-8 -*-
import logging
import json

from rule_console.settings import MONGO_CONFIG
from rule_console.model.locale import Locale
from rule_console.api import request, app
from rule_console.view.locale import (
    save_locale_info, locale_info_list, update_locale_info, delete_locale_info,
    get_locale_by_id)
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_REQUIRED, PARAM_ERROR
from rule_console.decorator import exception_handler, access_control
from rule_console.utils.common import search_cond
from rule_console.utils.respcode import (
    DATA_RELETED_BY_OTHER, DUPLICATE_FIELD)


_LOGGER = logging.getLogger(__name__)

API_GET_LOCALE = '/<appname>/rule/v1/locale/list'
API_ADD_LOCALE = '/<appname>/rule/v1/locale/add'
API_EDIT_LOCALE = '/<appname>/rule/v1/locale/edit'
API_UPDATE_LOCALE = '/<appname>/rule/v1/locale/update'
API_DELETE_LOCALE = '/<appname>/rule/v1/locale/delete'


@app.route(API_GET_LOCALE, methods=['GET', ])
@exception_handler
@access_control
def locale_list(appname):
    '''
        list api for show locale list.
        Request URL:  /appname/rule/locale/list
        Http Method:  GET
        Parameters : index, limit
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"zh_CN",
                    },
                    {
                        "id": 2,
                        "title":"ru_RU",
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
        cond = search_cond(searchKeyword, Locale.search_fields)
    sort = [("last_modified", -1)]
    data = locale_info_list(
        appname, cond, sort=sort, page=index, page_size=limit)
    return json_response_ok(data, msg="")


@app.route(API_ADD_LOCALE, methods=['POST', "OPTIONS"])
@exception_handler
@access_control
def add_locale_info(appname):
    '''
        create api to add locale.
        Request URL:  /appname/rule/locale/add
        Http Method: POST
        Parameters :
        {
           "id": 1,
           "title": "zh_CN"
        }
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"zh_CN",
                    },
                    {
                        "id": 2,
                        "title":"ru_RU",
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
        locale_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("add operator para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check required args
    if "title" not in locale_obj:
        return json_response_error(PARAM_REQUIRED, msg="not param:title")

    # check if locale title duplicate
    title = locale_obj.get("title")
    if Locale.find_one_locale(appname, {"title": title}):
        return json_response_error(
            DUPLICATE_FIELD, msg="the locale title exist")

    # add logic
    save_locale_info(appname, title)

    cond = {}
    sort = [("last_modified", -1)]
    data = locale_info_list(appname, cond, sort=sort)
    return json_response_ok(data, msg="add locale success")


@app.route(API_EDIT_LOCALE, methods=['GET', ])
@exception_handler
@access_control
def edit_locale(appname):
    '''
        this api is used to view one locale
        Request URL:  /appname/rule/locale/edit
        Http Method: GET
        Parameters : id
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"zh_CN",
            }
        }

     '''
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")

    # check required args
    if "id" not in request.args:
        return json_response_error(PARAM_REQUIRED, msg="not param:id")

    # check if locale id in db
    lcid = int(request.args["id"])
    if not Locale.find_one_locale(appname, {"_id": lcid}):
        return json_response_error(PARAM_ERROR, msg="the locale not in db")

    # view logic
    fields = {"first_created": 0, "last_modified": 0}
    data = get_locale_by_id(appname, lcid, fields)
    return json_response_ok(data, msg="")


@app.route(API_UPDATE_LOCALE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def modify_locale(appname):
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
    for arg in ["id", 'title']:
        if arg not in data_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # check if locale id in db
    lcid = int(data_obj["id"])
    if not Locale.find_one_locale(appname, {"_id": lcid}):
        return json_response_error(PARAM_ERROR, msg="the locale not in db")

    # check if locale title duplicate
    title = data_obj["title"]
    lc_info = Locale.find_one_locale(appname, {"title": title})
    if lc_info and lc_info["_id"] != lcid:
        return json_response_error(
            DUPLICATE_FIELD, msg="the locale title exist")

    # update logic
    new_locale = update_locale_info(appname, lcid, data_obj)
    _LOGGER.info("update operator:%s success", new_locale)
    return json_response_ok(new_locale)


@app.route(API_DELETE_LOCALE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def delete_locale(appname):
    '''
        this api is used to delete locale,
        when one locale refered, the locale cannot removed
        Request URL:  /appname/rule/locale/delete
        HTTP Method: POST
        Parameters:
            {
                "items":[3, 2]
            }
        Return:
            {
                "status": 0,
                "msg": "delete locale success",
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
        _LOGGER.error("delete locale para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # delete logic
    oids = data_obj.get("items")
    data = {}
    data["success"], data["failed"], invalid = delete_locale_info(
        appname, oids)
    if invalid:
        return json_response_error(
            PARAM_ERROR, msg="invalid locale id,check parameters")
    if data["failed"]:
        return json_response_error(DATA_RELETED_BY_OTHER, data)
    else:
        return json_response_ok(data, msg="delete locale success")
