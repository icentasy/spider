# -*- coding: utf-8 -*-
import logging
from auth_service.model.module import Module
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_ERROR

_LOGGER = logging.getLogger(__name__)


def module_create(appname, module_name, module_value, order=1):
    '''
    create module to add module.
    Parameters:
    {
        'module__name': 'rule',
        'module_value': '配置规则',
        'order': 1
    }
    '''
    module_cond = {'module_name': module_name, "app_name": appname}
    if Module.find_one_module(appname, module_cond):
        return json_response_error(PARAM_ERROR, msg="the module exist")
    module_instance = Module.new(appname, module_name, module_value, order)
    Module.save(appname, module_instance)
    return json_response_ok()


def module_delete(appname, mid):
    '''
    this api is used to delete app
    Request URL: /auth/app/delete
    HTTP Method: POST
    Parameters:
        {
            "aids":3
        }
    Return:
     {
     "status":0
     "data":{}
     "msg":"delete successfully"
     }
    '''
    mid = int(mid)
    module_info = Module.find_one_module(appname, {"_id": mid}, None)
    data = {"id": mid}
    if module_info:
        Module.del_module(appname, mid)
        return json_response_ok(data, msg="delete app success")
    else:
        _LOGGER.info("module id %s is not exist" % mid)
        return json_response_error(
            PARAM_ERROR, data, msg="invalid module id,check parameters")


def module_list(appname):
    sort = [("order", 1), ("_id", 1)]
    module_cursor = Module.find_module(appname, {}, fields=None).sort(sort)
    total = Module.find_module(appname, {}).count()
    modules = []
    for item in module_cursor:
        item["id"] = item.pop("_id")
        modules.append(item)
    data = {}
    data.setdefault("items", modules)
    data.setdefault("total", total)
    return json_response_ok(data)


def module_mod(appname, mid, data):
    try:
        mid = int(mid)
    except ValueError as expt:
        _LOGGER.error("modify module para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="module_id error,check parameters format")
    for key in data:
        if key not in Module.params:
            json_response_error(PARAM_ERROR, msg="unnecessary param:%s" % key)
    module_name = data["module_name"]
    old_module = Module.find_one_module(
        appname, {"module_name": module_name, "app_name": appname})
    if old_module and old_module["_id"] != mid:
        return json_response_error(PARAM_ERROR, msg="the appname exist")
    cond = {"_id": mid}
    Module.update_module(appname, cond, data)
    return json_response_ok()


def module_get(appname, mid):
    '''
        this api is used to view one module
        Request URL: /auth/module/{mid}
        HTTP Method:GET
        Return:
            Parameters: None
            {
                "status":0
                "data":{
                "item":[
                {
                    "id":"2",
                    "role":"admin",
                    "last_login":[19,20,21,22]
                }
            }
    '''
    try:
        module_id = int(mid)
    except ValueError as expt:
        _LOGGER.error("get app info  para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="user_id error,check parameters format")
    module_info = Module.find_one_module(appname, {"_id": module_id}, None)
    if module_info:
        return json_response_ok(module_info)
    else:
        return json_response_error(
            PARAM_ERROR, msg="not module:%s" % module_id)


def order_module(appname, projectname, modules):
    sort = [("order", 1), ("_id", 1)]
    cond = {"app_name": projectname, "module_name": {"$in": modules}}
    module_cursor = Module.find_module(appname, cond, fields=None).sort(sort)
    app_names = []
    app_names = [item["module_name"] for item in module_cursor]
    return app_names
