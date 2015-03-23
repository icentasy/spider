# -*- coding: utf-8 -*-
import logging
from auth_service.model.apps import App
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_ERROR

_LOGGER = logging.getLogger(__name__)


def app_create(appname, name, app_value, order=1):
    '''
    create api to add app.
    Parameters:
    {
        'app_name': 'rule',
        'app_value': '配置规则',
        'order': 1
    }
    '''
    app_cond = {'name': name, "app_name": appname}
    if App.find_one_app(appname, app_cond):
        return json_response_error(PARAM_ERROR, msg="the app exist")
    app_instance = App.new(appname, name, app_value, order)
    App.save(appname, app_instance)
    return json_response_ok()


def app_delete(appname, aid):
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
    aid = int(aid)
    app_info = App.find_one_app(appname, {"_id": aid}, None)
    data = {"id": aid}
    if app_info:
        App.del_app(appname, aid)
        return json_response_ok(data, msg="delete app success")
    else:
        _LOGGER.info("app id %s is not exist" % aid)
        return json_response_error(
            PARAM_ERROR, data, msg="invalid app id,check parameters")


def app_list(appname):
    sort = [("_id", 1)]
    app_cursor = App.find_app(appname, {}, fields=None).sort(sort)
    total = App.find_app(appname, {}).count()
    apps = []
    for item in app_cursor:
        item["id"] = item.pop("_id")
        apps.append(item)
    data = {}
    data.setdefault("items", apps)
    data.setdefault("total", total)
    return json_response_ok(data)


def app_mod(appname, aid, data):
    try:
        aid = int(aid)
    except ValueError as expt:
        _LOGGER.error("modify app para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="app_id error,check parameters format")
    for key in data:
        if key not in App.params:
            json_response_error(PARAM_ERROR, msg="unnecessary param:%s" % key)
    name = data["name"]
    old_app = App.find_one_app(appname, {"name": name, "app_name": appname})
    if old_app and old_app["_id"] != aid:
        return json_response_error(PARAM_ERROR, msg="the appname exist")
    cond = {"_id": aid}
    App.update_app(appname, cond, data)
    return json_response_ok()


def app_get(appname, app_id):
    '''
        this api is used to view one app
        Request URL: /auth/app/{aid}
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
                        "last_login": "2014-10-10"
                    }
            }
    '''
    try:
        app_id = int(app_id)
    except ValueError as expt:
        _LOGGER.error("get app info  para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="user_id error,check parameters format")
    app_info = App.find_one_app(appname, {'_id': app_id}, None)
    if app_info:
        return json_response_ok(app_info)
    else:
        return json_response_error(PARAM_ERROR, msg="not app:%s" % app_id)


def order_app(appname, projectname, apps):
    sort = [("order", 1), ("_id", 1)]
    cond = {"app_name": projectname, "name": {"$in": apps}}
    app_cursor = App.find_app(appname, cond, fields=None).sort(sort)
    app_names = []
    app_names = [item["name"] for item in app_cursor]
    return app_names
