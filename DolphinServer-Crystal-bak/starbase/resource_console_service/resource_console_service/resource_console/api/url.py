# -*- coding:utf-8 -*-
import logging
import simplejson

from resource_console.api import request, app
from resource_console.model.icon import Icon
from resource_console.view.icon import (
    update_icon_info, get_icon_display_data, icon_info_list,
    save_icon_info, get_icon_by_id, delete_icon_info, upload_icon_info)
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import (
    PARAM_REQUIRED, METHOD_ERROR, PARAM_ERROR)
from resource_console.decorator import exception_handler, access_control
from resource_console.settings import MONGO_CONFIG
from resource_console.utils.common import search_cond

_LOGGER = logging.getLogger(__name__)

API_GET_ICON = '/<appname>/resource/v1/icon/list'
API_GET_DISPLAYDATA = '/<appname>/resource/v1/icon/getDisplayData'
API_ADD_ICON = '/<appname>/resource/v1/icon/add'
API_EDIT_ICON = '/<appname>/resource/v1/icon/edit'
API_UPDATE_ICON = '/<appname>/resource/v1/icon/update'
API_UPLOAD_ICON = '/<appname>/resource/v1/icon/upload'
API_DELETE_ICON = '/<appname>/resource/v1/icon/delete'


DATA_RELETED_BY_OTHER = 1004
DATA_DUPLICATE_DELETE = 1005
DUPLICATE_FIELD = 1006
_ONE_DAY = 86400.0
_PIC_TYPES = ['png', 'jpg', "gif", "jpeg", "bmp"]


@app.route(API_GET_ICON, methods=['GET', ])
@exception_handler
@access_control
def icon_list(appname):
    if request.method == 'GET':
        if appname not in MONGO_CONFIG:
            return json_response_error(PARAM_ERROR, msg="appname error")
        index = int(request.args.get('index', 1)) - 1
        limit = int(request.args.get('limit', 20))
        searchKeyword = request.args.get("searchKeyword")
        cond = {}
        if searchKeyword:
            cond = search_cond(appname, searchKeyword)
        sort = [("last_modified", -1)]
        fields = {
            "first_created": 0, "last_modified": 0, "platform": 0,
            "package": 0, "type": 0, "refered_info": 0}
        data = icon_info_list(
            appname, cond, sort=sort, fields=fields, page=index,
            page_size=limit)
        return json_response_ok(data, msg="")
    else:
        return json_response_error(METHOD_ERROR, msg="http method error")


@app.route(API_GET_DISPLAYDATA, methods=['GET', ])
@exception_handler
@access_control
def get_displaydata(appname):
    if request.method == 'GET':
        data = {}
        data["platform"] = get_icon_display_data(appname)
        return json_response_ok(data, msg="")
    else:
        return json_response_error(METHOD_ERROR, msg="http method error")


@app.route(API_ADD_ICON, methods=['POST', "OPTIONS"])
@exception_handler
@access_control
def add_icon_info(appname):
    if request.method == 'POST':
        iconfile = request.files.get('icon')
        if not iconfile:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:icon")
        data_obj = request.form
        required_list = ("title", "type", "platform", "package")
        for arg in required_list:
            if arg not in data_obj:
                return json_response_error(
                    PARAM_REQUIRED, msg="not param:%s" % arg)

        iconfile = request.files['icon']
        icon_name = iconfile.filename.lower()

        icon_suffix = icon_name.split('.')[-1]

        if icon_suffix not in _PIC_TYPES:
            return json_response_error(
                PARAM_ERROR, msg='upload file format error[%s]' % (icon_name))
        title = data_obj.get("title")
        if Icon.find_one_icon(appname, {"title": title}):
            return json_response_error(
                DUPLICATE_FIELD, msg="the icon title exist")
        icon_name = "%s.%s" % (title, icon_suffix)
        icon_dict = {}
        icon_dict["title"] = title
        icon_dict["package"] = simplejson.loads(data_obj.get("package"))
        icon_dict["type"] = simplejson.loads(data_obj.get("type"))
        icon_dict["platform"] = int(data_obj.get("platform"))
        icon_dict["icon"] = icon_name
        save_icon_info(appname, iconfile, icon_dict)
        icon_info = Icon.find_one_icon(appname, {"title": title}, None)
        icon_info["id"] = icon_info.pop("_id")
        '''
        cond = {}
        sort = [("last_modified", -1)]
        data = icon_info_list(appname, cond, sort=sort)
        '''

        return json_response_ok(data=icon_info, msg="add icon success")
    else:
        return json_response_error(METHOD_ERROR)


@app.route(API_EDIT_ICON, methods=['GET', ])
@exception_handler
@access_control
def edit_icon_info(appname):
    if request.method == 'GET':
        args = request.args
        for arg in ['id', ]:
            if arg not in args:
                return json_response_error(
                    PARAM_REQUIRED, msg="not param:%s" % arg)
        icon_id = args["id"]
        fields = {
            "is_upload_ec2": 0, "is_upload_local": 0,
            "first_created": 0, "refered_info": 0}
        data = get_icon_by_id(appname, icon_id, fields)
        if not data:
            return json_response_error(
                PARAM_ERROR, msg='icon:%s not in db' % (icon_id))
        return json_response_ok(data, msg="")
    else:
        return json_response_error(METHOD_ERROR, msg="http method error")


@app.route(API_UPDATE_ICON, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def modify_icon_info(appname):
    if request.method == 'POST':
        data_obj = request.form
        for arg in ["id", 'platform', 'title', 'type', "package"]:
            if arg not in data_obj:
                return json_response_error(
                    PARAM_REQUIRED, msg="not param:%s" % arg)
        icon_id = int(data_obj["id"])
        title = data_obj["title"]
        if not Icon.find_one_icon(appname, {"_id": icon_id}):
            return json_response_error(
                PARAM_ERROR, msg="the locale not in db")
        icon_info = Icon.find_one_icon(appname, {"title": title})
        if icon_info and icon_info["_id"] != icon_id:
            return json_response_error(
                DUPLICATE_FIELD, msg="the icon title exist")

        icon_dict = {}
        icon_dict["title"] = title
        icon_dict["package"] = simplejson.loads(data_obj.get("package"))
        icon_dict["type"] = simplejson.loads(data_obj.get("type"))
        icon_dict["platform"] = int(data_obj.get("platform"))

        iconfile = request.files.get('icon')
        if iconfile:
            icon_name = iconfile.filename.lower()
            icon_suffix = icon_name.split('.')[-1]

            if icon_suffix not in _PIC_TYPES:
                return json_response_error(
                    PARAM_ERROR,
                    msg='upload file format error[%s]' % (icon_name))
            icon_name = "%s.%s" % (title, icon_suffix)
            icon_dict["icon"] = icon_name

        new_icon = update_icon_info(appname, icon_id, iconfile, icon_dict)
        _LOGGER.info("update icon:%s success", new_icon)
        return json_response_ok(new_icon)
    else:
        return json_response_error(METHOD_ERROR)


@app.route(API_DELETE_ICON, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def delete_icon_api(appname):
    if request.method == 'POST':
        try:
            data_obj = simplejson.loads(request.data)
        except ValueError as expt:
            _LOGGER.error("delete package para except:%s", expt)
            return json_response_error(
                PARAM_ERROR,
                msg="json loads error,check parameters format")

        server = data_obj.get("server", "local")
        icon_info = data_obj.get("items")
        data = {}
        if server == "admin":
            data["success"], data["failed"], invalid = delete_icon_info(
                appname, icon_info)
            if invalid:
                return json_response_error(
                    PARAM_ERROR, msg="invalid icon id,check parameters")
            if data["failed"]:
                return json_response_error(DATA_RELETED_BY_OTHER, data)
            else:
                return json_response_ok(data, msg="delete icon success")
        else:
            data["success"], data["failed"], duplicate = upload_icon_info(
                appname, icon_info, server, is_del=True)
            if duplicate:
                return json_response_error(
                    DATA_DUPLICATE_DELETE, data, msg="duplicate delete")
            if data["failed"]:
                return json_response_error(PARAM_ERROR, data)
            else:
                return json_response_ok(data)
    else:
        return json_response_error(METHOD_ERROR, msg="http method error")


@app.route(API_UPLOAD_ICON, methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def upload_icon(appname):
    """
    POST: upload icon to server
    Parameters:
        -id: the id of icon,
    Return:
        -1. upload success
            {
                "status": 0,
                "data":{
                       ...
                }
            }
        -2. error http method
            {
                "status": 11,
                "data":{
                       ...
                }
            }
    """
    if request.method == 'POST':
        try:
            data_obj = simplejson.loads(request.data)
        except ValueError as expt:
            _LOGGER.error("upload icon api para except:%s", expt)
            return json_response_error(
                PARAM_ERROR,
                msg="json loads error,check parameters format")
        required_list = ("server", "items")
        for arg in required_list:
            if arg not in data_obj:
                return json_response_error(
                    PARAM_REQUIRED, msg="not param:%s" % arg)

        server = data_obj.get("server", "local")
        icon_info = data_obj.get("items")
        data = {}
        data["success"], data["failed"], duplicate = upload_icon_info(
            appname, icon_info, server, is_del=False)
        if data["failed"]:
            return json_response_error(PARAM_ERROR, data)
        else:
            return json_response_ok(data)
    else:
        return json_response_error(METHOD_ERROR, msg="http method wrong")
