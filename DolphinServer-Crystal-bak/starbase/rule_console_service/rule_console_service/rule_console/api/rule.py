# -*- coding:utf-8 -*-
import logging
import json
import time

from rule_console.settings import MONGO_CONFIG
from rule_console.api import request, app
from rule_console.model.rule import Rule
from rule_console.view.rule import (
    rule_info_list, delete_rule_info, get_rule_filter_list,
    get_rule_display_data, save_rule_info, get_rule_by_id, update_rule_info)
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_REQUIRED, PARAM_ERROR
from rule_console.decorator import exception_handler, access_control
from rule_console.model import ArmoryMongo
from rule_console.utils.common import search_cond
from rule_console.utils.respcode import (
    DATA_RELETED_BY_OTHER, DUPLICATE_FIELD)

_LOGGER = logging.getLogger(__name__)


API_GET_RULE = '/<appname>/rule/v1/rule/list'
API_GET_DISPLAYDATA = '/<appname>/rule/v1/rule/getDisplayData'
API_ADD_RULE = '/<appname>/rule/v1/rule/add'
API_EDIT_RULE = '/<appname>/rule/v1/rule/edit'
API_UPDATE_RULE = '/<appname>/rule/v1/rule/update'
API_DELETE_RULE = '/<appname>/rule/v1/rule/delete'

_ONE_DAY = 86400.0
_MAX_VERSION = 4294967295


@app.route(API_GET_RULE, methods=['GET', ])
@exception_handler
@access_control
def rule_list(appname):
    '''
        list api for show rule list.
        Request URL:  /appname/rule/rule/list
        Http Method:  GET
        Parameters : index, limit
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"海豚英文版",
                        "min_version": 0,
                        "max_version": 0,
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    },
                    {
                        "id": 2,
                        "title":"海豚英文版1",
                        "min_version": 0,
                        "max_version": 0,
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

    # get params
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    pn = request.args.get("package", "all")
    locale = request.args.get("locale", "all")
    start_time = request.args.get("start")
    end_time = request.args.get("end")
    searchKeyword = request.args.get("searchKeyword")
    cond = {}
    if start_time and end_time:
        start = time.mktime(time.strptime(start_time, '%Y-%m-%d'))
        end = time.mktime(time.strptime(end_time, '%Y-%m-%d')) + _ONE_DAY
        cond["last_modified"] = {"$gte": start, "$lte": end}
    if pn != "all":
        cond["package"] = int(pn)
    if locale != "all":
        cond["locale"] = int(locale)
    if searchKeyword:
        cond = search_cond(searchKeyword, Rule.search_fields)

    # view logic
    sort = [("last_modified", -1)]
    fields = {
        "_id": 1, "title": 1, "min_version": 1, "max_version": 1,
        "first_created": 1, "last_modified": 1}
    data = rule_info_list(
        appname, cond, fields, sort=sort, page=index, page_size=limit)
    filter_list = get_rule_filter_list(appname)
    data.setdefault("filters", filter_list)
    return json_response_ok(data)


@app.route(API_GET_DISPLAYDATA, methods=['GET', ])
@exception_handler
@access_control
def get_display_data(appname):
    # check appname
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="can not find appname")
    data = get_rule_display_data(appname)
    return json_response_ok(data)


@app.route(API_ADD_RULE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def rule_add(appname):
    '''
        create api to add rule.
        Request URL:  /appname/rule/rule/add
        Http Method: POST
        Parameters :
            {
                "title": "xxxx"
                "min_version": 0,
                "max_version": 0,
                "source":[1],
                "locale":[1],
                "operator":[1],
                "package":[1],
                "min_value": 0,
                "max_value": 100,
                "gray_scale": 100,
                "gray_start": 1
            }
        Return :
        {
            "status":0
            "data":{
                "items":[
                    {
                        "id": 1,
                        "title":"海豚英文版",
                        "min_version": 0,
                        "max_version": 0,
                        "first_created": "2015-02-05 21:37:38",
                        "last_modified": "2015-02-05 21:37:38"
                    },
                    {
                        "id": 2,
                        "title":"联通",
                        "min_version": 0,
                        "max_version": 0,
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
        rule_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("add package para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check request json format
    required_list = [
        'platform', 'title', 'package', 'operator', 'source',
        'locale', "min_version"]
    for arg in required_list:
        if arg not in rule_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # check if rule title duplicate
    title = rule_obj.get("title")
    if Rule.find_one_rule(appname, {"title": title}):
        return json_response_error(
            DUPLICATE_FIELD, msg="the rule title exist")

    # check if pn is []
    if not rule_obj["package"]:
        return json_response_error(PARAM_ERROR, msg="parameters:package error")

    # check if pn_id/op_id/src_id/lc_id  exist
    for arg in ["package", "operator", "source", "locale"]:
        arg_id = rule_obj[arg]
        if arg_id:
            for item_id in arg_id:
                arg_cond = {"_id": int(item_id)}
                if not ArmoryMongo[appname][arg].find_one(arg_cond):
                    return json_response_error(
                        PARAM_ERROR, msg="parameters:%s id error" % arg)

    # add logic
    save_rule_info(appname, rule_obj)

    '''
    cond = {}
    sort = [("last_modified", -1)]
    fields = {
        "_id": 1, "title": 1, "min_version": 1, "max_version": 1,
        "first_created": 1, "last_modified": 1}
    data = rule_info_list(appname, cond, fields, sort=sort)
    '''
    rule_title = rule_obj.get('title')
    rule_dict = ArmoryMongo[appname]['rule'].find_one({"title": rule_title})
    rule_dict['id'] = rule_dict['_id']
    return json_response_ok(data=rule_dict, msg="add rule success")


@app.route(API_EDIT_RULE, methods=['GET', ])
@exception_handler
@access_control
def rule_edit(appname):
    '''
        this api is used to view one rule
        Request URL:  /appname/rule/rule/edit
        Http Method: GET
        Parameters : id
        Return :
        {
            "status":0
            "data":{
                "id": 1,
                "title":"海豚英文版",
                "min_version": 0,
                "max_version": 0,
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
    if "id" not in request.args:
        return json_response_error(PARAM_REQUIRED, msg="not param:id")

    # check if rule id in db
    rule_id = int(request.args["id"])
    if not Rule.find_one_rule(appname, {"_id": rule_id}):
        return json_response_error(PARAM_ERROR, msg="the rule not in db")

    # view logic
    fields = {"first_created": 0, "last_modified": 0}
    data = get_rule_by_id(appname, rule_id, fields)
    return json_response_ok(data, msg="")


@app.route(API_UPDATE_RULE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def rule_update(appname):
    '''
        this api is used to modify one rule
        Request URL:  /appname/rule/rule/update
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
                "title":"海豚英文版",
                "min_version": 0,
                "max_version": 0,
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
        rule_obj = json.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("add package para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")

    # check required args
    required_list = [
        'platform', 'title', 'package', 'operator', 'source', 'locale',
        "min_version", "max_version", "min_value", "max_value",
        "gray_start", "gray_scale"]
    for arg in required_list:
        if arg not in rule_obj:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)

    # check if rule id in db
    rule_id = rule_obj["id"]
    if not Rule.find_one_rule(appname, {"_id": rule_id}):
        return json_response_error(PARAM_ERROR, msg="the rule not in db")

    # check if rule title duplicate
    title = rule_obj["title"]
    rule_info = Rule.find_one_rule(appname, {"title": title})
    if rule_info and rule_info["_id"] != rule_id:
        return json_response_error(
            DUPLICATE_FIELD, msg="the rule title exist")

    # check if pn is []
    if not rule_obj["package"]:
        return json_response_error(PARAM_ERROR, msg="parameters:package error")

    # check if pn_id/op_id/src_id/lc_id  exist
    for arg in ["package", "operator", "source", "locale"]:
        arg_id = rule_obj[arg]
        if arg_id:
            for item_id in arg_id:
                arg_cond = {"_id": int(item_id)}
                if not ArmoryMongo[appname][arg].find_one(arg_cond):
                    return json_response_error(
                        PARAM_ERROR, msg="parameters:%s id error" % arg)

    # update logic
    new_rule = update_rule_info(appname, rule_id, rule_obj)
    _LOGGER.info("update rule:%s success", new_rule)
    return json_response_ok(new_rule, msg="")


@app.route(API_DELETE_RULE, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def rule_delete(appname):
    '''
        this api is used to delete rule,
        when one rule refered, the rule cannot removed
        Request URL:  /appname/rule/rule/delete
        HTTP Method: POST
        Parameters:
            {
                "items":[3, 2]
            }
        Return:
            {
                "status": 0,
                "msg": "delete rule success",
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
            PARAM_ERROR,
            msg="json loads error,check parameters format")

    # delete logic
    rids = data_obj.get("items")
    data = {}
    data["success"], data["failed"], invalid = delete_rule_info(
        appname, rids)
    if invalid:
        return json_response_error(
            PARAM_ERROR, msg="invalid locale id,check parameters")
    if data["failed"]:
        return json_response_error(DATA_RELETED_BY_OTHER, data)
    else:
        return json_response_ok(data, msg="delete locale success")
    return json_response_ok({})
