# -*- coding:utf-8 -*-
import logging
import json

from rule_console.settings import MONGO_CONFIG
from rule_console.api import request, app
from rule_console.model.package import Package
from rule_console.view.package import (
    update_package_info, get_package_display_data, package_info_list,
    save_package_info, get_package_by_id, delete_package_info)
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_REQUIRED, PARAM_ERROR
from rule_console.decorator import exception_handler, access_control
from rule_console.utils.common import search_cond
from rule_console.utils.respcode import (
    DATA_RELETED_BY_OTHER, DUPLICATE_FIELD)


_LOGGER = logging.getLogger(__name__)

API_GET_PACKAGE = '/<appname>/rule/v1/package/list'
API_GET_DISPLAYDATA = '/<appname>/rule/v1/package/getDisplayData'
API_ADD_PACKAGE = '/<appname>/rule/v1/package/add'
API_EDIT_PACKAGE = '/<appname>/rule/v1/package/edit'
API_UPDATE_PACKAGE = '/<appname>/rule/v1/package/update'
API_DELETE_PACKAGE = '/<appname>/rule/v1/package/delete'


@app.route(API_GET_PACKAGE, methods=['GET', ])
@exception_handler
@access_control
def package_list(appname):
    '''
        list api for show package list.
        Request URL:  /appname/rule/package/list
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
                        "package_name": "mon",
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    },
                    {
                        "id": 2,
                        "title":"联通",
                        "package_name": "mon",
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
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
        cond = search_cond(searchKeyword, Package.search_fields)
    sort = [("last_modified", -1)]
    data = package_info_list(
        appname, cond, sort=sort, page=index, page_size=limit)
    return json_response_ok(data, msg="")


@app.route(API_GET_DISPLAYDATA, methods=['GET', ])
@exception_handler
@access_control
def get_displaydata(appname):
    # check appname
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="can not find appname")

    data = get_package_display_data(appname)
    return json_response_ok(data, msg="")


@app.route(API_ADD_PACKAGE, methods=['POST', "OPTIONS"])
@exception_handler
@access_control
def add_package_info(appname):
    '''
        create api to add operator.
        Request URL:  /appname/rule/package/add
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
                        "package_name": "mon",
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    },
                    {
                        "id": 2,
                        "title":"联通",
                        "package_name": "mon",
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
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
        data_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("add package para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check required args
    for arg in ['platform', 'title', 'package_name']:
        if arg not in data_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # check if operator title duplicate
    title = data_obj.get("title")
    platform = int(data_obj.get("platform"))
    if Package.find_one_package(appname, {"title": title}):
        return json_response_error(
            DUPLICATE_FIELD, msg="the package title exist")

    # add logic
    pn = data_obj.get("package_name")
    save_package_info(appname, title, platform, pn)

    cond = {}
    sort = [("last_modified", -1)]
    data = package_info_list(appname, cond, sort=sort)
    return json_response_ok(data, msg="add package success")


@app.route(API_EDIT_PACKAGE, methods=['GET', ])
@exception_handler
@access_control
def edit_package_info(appname):
    '''
        this api is used to view one package
        Request URL:  /appname/rule/package/edit
        Http Method: GET
        Parameters : id
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"移动",
                "package_name": "mon",
                "first_created": "2015-02-05 21:37:38",
                "last_modified": "2015-02-05 21:37:38"
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

    # check if package id in db
    pid = int(args["id"])
    if not Package.find_one_package(appname, {"_id": pid}):
        return json_response_error(PARAM_ERROR, msg="the package not in db")

    # view logic
    fields = {"first_created": 0, "last_modified": 0}
    data = get_package_by_id(appname, pid, fields)
    return json_response_ok(data, msg="")


@app.route(API_UPDATE_PACKAGE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def modify_package_info(appname):
    '''
        this api is used to modify one package
        Request URL:  /appname/rule/package/update
        HTTP Method:POST
        Parameters:
        {
           "id": 1,
           "title": "xxxx",
           "platform": 1,
           "package_name": "xxxx"
        }
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"移动",
                "package_name": "mon",
                "first_created": "2015-02-05 21:37:38",
                "last_modified": "2015-02-05 21:37:38"
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
        _LOGGER.error("modify package para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check required args
    for arg in ["id", 'platform', 'title', 'package_name']:
        if arg not in data_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # check if package id in db
    pn_id = int(data_obj["id"])
    if not Package.find_one_package(appname, {"_id": pn_id}):
        return json_response_error(
            PARAM_ERROR, msg="the package not in db")

    # check if package title duplicate
    title = data_obj["title"]
    pn_info = Package.find_one_package(appname, {"title": title})
    if pn_info and pn_info["_id"] != pn_id:
        return json_response_error(
            DUPLICATE_FIELD, msg="the package title exist")

    # update logic
    new_package = update_package_info(appname, pn_id, data_obj)
    _LOGGER.info("update package:%s success", new_package)
    return json_response_ok(new_package, msg="")


@app.route(API_DELETE_PACKAGE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def delete_package_api(appname):
    '''
        this api is used to delete package,
        when one package refered, the package cannot removed
        Request URL:  /appname/rule/package/delete
        HTTP Method: POST
        Parameters:
            {
                "items":[3, 2]
            }
        Return:
            {
                "status": 0,
                "msg": "delete package success",
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
        _LOGGER.error("delete package para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # delete logic
    pids = data_obj.get("items")
    data = {"success": [], "failed": []}
    data["success"], data["failed"], invalid = delete_package_info(
        appname, pids)
    if invalid:
        return json_response_error(
            PARAM_ERROR, msg="invalid package id,check parameters")
    if data["failed"]:
        return json_response_error(DATA_RELETED_BY_OTHER, data)
    else:
        return json_response_ok(data, msg="")
