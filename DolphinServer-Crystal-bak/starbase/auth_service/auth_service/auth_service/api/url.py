# -*- coding:utf-8 -*-
import logging
import simplejson


from auth_service.settings import MONGO_CONFIG
from auth_service.settings import NAV_DICT
from auth_service.api import request, session, app
from auth_service.view.user import (
    user_login, user_create, user_delete, user_list, user_mod, user_get,
    user_chpasswd, user_active, user_right_get, user_right_mod)
from auth_service.view.group import (
    group_create, group_delete, group_list, group_name_mod, group_get,
    get_role_display_data, group_right_get, group_right_mod)
from auth_service.view.right import (
    right_create, right_delete, right_list, right_mod, right_get,
    check_session, menu_list, navigate_list, get_right_display_data)
from auth_service.view.modules import (
    module_create, module_list, module_mod, module_get)
from auth_service.view.apps import (
    app_create, app_list, app_mod, app_get)
from armory.marine.json import ArmoryJson
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import (
    PARAM_REQUIRED, METHOD_ERROR, AUTH_ERROR, PARAM_ERROR)
from armory.marine.access_control import access_control, exception_handler

_LOGGER = logging.getLogger('auth_service')


# login logout func
@app.route('/<appname>/login', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def login(appname):
    # check args
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    try:
        data_obj = simplejson.loads(request.data)
    except ValueError as expt:
        _LOGGER.error("login para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    for arg in ['user_name', 'password']:
        if arg not in data_obj:
            _LOGGER.error('cant find %s', arg)
            return json_response_error(
                PARAM_REQUIRED, msg='not param:%s' % arg)
        if not data_obj['user_name'] or not data_obj['password']:
            return json_response_error(PARAM_REQUIRED)
    # view logic
    return user_login(
        appname, data_obj['user_name'], data_obj['password'],
        session)


@app.route('/<appname>/logout', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def logout(appname):
    # logout remove uid from session
    session.pop('uid', None)
    # view logic
    return json_response_ok()


@app.route('/<appname>/changepwd', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def chpasswd_user(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if not session.get('uid'):
        _LOGGER.error('cant find uid in session')
        return json_response_error(AUTH_ERROR)
    try:
        pwd_data = ArmoryJson.decode(request.data)
    except ValueError as expt:
        _LOGGER.error("add uesr para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    for arg in ['current_password', 'new_password']:
        if arg not in pwd_data:
            _LOGGER.error('arg not in request')
            return json_response_error(PARAM_REQUIRED)
    return user_chpasswd(
        appname, session.get('uid'), pwd_data['current_password'],
        pwd_data['new_password'])


# add user group right
@app.route('/<appname>/user/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def add_user(appname):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    try:
        add_data = ArmoryJson.decode(request.data)
    except ValueError as expt:
        _LOGGER.error("add uesr para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    for arg in ['user_name',  'group_id']:
        if arg not in add_data:
            return json_response_error(
                PARAM_REQUIRED, msg='not param:%s' % arg)
    # view logic
    return user_create(appname, add_data)


@app.route('/<appname>/group/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def add_group(appname):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    add_data = ArmoryJson.decode(request.data)
    if "rolename" not in add_data:
        return json_response_error(PARAM_REQUIRED, msg='not param: rolename')
    # view logic
    return group_create(appname, add_data['rolename'])


@app.route('/<appname>/<projectname>/perm/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def add_right(appname, projectname):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    if projectname not in NAV_DICT.keys():
        return json_response_error(
            PARAM_ERROR, msg="projectname error, check url")
    try:
        add_data = ArmoryJson.decode(request.data)
    except ValueError as expt:
        _LOGGER.error("login para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    for arg in ['perm_module', 'perm_opname', 'perm_action']:
        if arg not in add_data:
            return json_response_error(
                PARAM_REQUIRED, msg="not param:%s" % arg)
    perm_module = add_data.get('perm_module')
    perm_opname = add_data.get('perm_opname')
    perm_action = add_data.get('perm_action')
    perm_type = add_data.get('perm_type', "module")
    if perm_type == "module" and \
            perm_action not in ['list', 'add', 'edit', 'delete']:
        return json_response_error(PARAM_ERROR)
    perm_lc = request.form.get('perm_lc', "all")

    # view logic
    return right_create(
        appname, projectname, perm_module, perm_opname,
        perm_action, perm_type, perm_lc)


@app.route('/<appname>/<projectname>/module/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def add_module(appname, projectname):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    if projectname not in NAV_DICT.keys():
        return json_response_error(
            PARAM_ERROR, msg="projectname error, check url")
    try:
        add_data = ArmoryJson.decode(request.data)
    except ValueError as expt:
        _LOGGER.error("login para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    for arg in ['module_name', "module_value", "order"]:
        if arg not in add_data:
            return json_response_error(
                PARAM_REQUIRED, msg='not param:%s' % arg)
    # view logic
    return module_create(
        appname, add_data['module_name'], add_data["module_value"],
        add_data["order"])


@app.route('/<appname>/<projectname>/app/add', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def add_app(appname, projectname):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    if projectname not in NAV_DICT.keys():
        return json_response_error(
            PARAM_ERROR, msg="projectname error, check url")
    try:
        add_data = ArmoryJson.decode(request.data)
    except ValueError as expt:
        _LOGGER.error("login para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    for arg in ['name', "app_value", "order"]:
        if arg not in add_data:
            return json_response_error(
                PARAM_REQUIRED, msg='not param:%s' % arg)
    # view logic
    return app_create(
        appname, add_data['name'], add_data["app_value"],
        add_data["order"])


# del user group right
@app.route('/<appname>/user/delete', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def del_user(appname):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    try:
        del_data = ArmoryJson.decode(request.data)
    except ValueError as expt:
        _LOGGER.error("delete user para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    if "uids" not in del_data:
        return json_response_error(PARAM_REQUIRED, msg="not param:uids")
    # view logic
    return user_delete(appname, del_data['uids'])


@app.route('/<appname>/group/delete', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def del_group(appname):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    try:
        del_data = ArmoryJson.decode(request.data)
    except ValueError as expt:
        _LOGGER.error("del group para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    if "gids" not in del_data:
        return json_response_error(PARAM_REQUIRED, msg="not param:gids")

    # view logic
    return group_delete(appname, del_data['gids'])


@app.route('/<appname>/right/delete', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def del_right(appname):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    for arg in ['pids']:
        if arg not in request.form:
            return json_response_error(PARAM_REQUIRED)
    # view logic
    return right_delete(appname, request.form['pids'])


# list user group right
@app.route('/<appname>/user/list', methods=['GET', ])
@exception_handler
@access_control
def list_user(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    searchKeyword = request.args.get("searchKeyword")
    return user_list(appname, index, limit, searchKeyword)


@app.route('/<appname>/user/getDisplayData', methods=['GET', ])
@exception_handler
@access_control
def get_role_displaydata(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    data = {}
    data["roles"] = get_role_display_data(appname)
    return json_response_ok(data, msg="")


@app.route('/<appname>/group/list', methods=['GET', ])
@exception_handler
@access_control
def list_group(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    index = int(request.args.get('index', 1)) - 1
    limit = int(request.args.get('limit', 20))
    return group_list(appname, index, limit)


@app.route('/<appname>/perm/list', methods=['GET', ])
@exception_handler
@access_control
def list_right(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    return right_list(appname)


@app.route('/<appname>/<projectname>/menu/list', methods=['GET', ])
@exception_handler
@access_control
def list_menu(appname, projectname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if projectname not in NAV_DICT.keys():
        return json_response_error(
            PARAM_ERROR, msg="projectname error, check url")
    if "uid" not in request.args:
        return json_response_error(PARAM_REQUIRED, msg='not param:uid')
    uid = request.args.get("uid")
    return menu_list(appname, projectname, uid)


@app.route('/<appname>/navigate/list', methods=['GET', ])
@exception_handler
@access_control
def list_navigate(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    if "uid" not in request.args:
        return json_response_error(PARAM_REQUIRED, msg='not param:uid')
    uid = request.args.get("uid")
    return navigate_list(appname, uid)


@app.route('/<appname>/label/list', methods=['GET', ])
@exception_handler
@access_control
def list_label(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    data = {}
    label = []
    app_names = NAV_DICT.keys()
    for app_name in app_names:
        app_dict = {}
        app_display = NAV_DICT.get(app_name)
        app_dict.setdefault("display_value", app_display)
        app_dict.setdefault("value", app_name)
        label.append(app_dict)
    data.setdefault("navigate", label)
    return json_response_ok(data, msg="")


@app.route('/<appname>/<projectname>/perm/getDisplayData', methods=['GET', ])
@exception_handler
@access_control
def perm_display(appname, projectname):
    if appname not in MONGO_CONFIG:
        _LOGGER.error('cant find appname')
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    if projectname not in NAV_DICT.keys():
        return json_response_error(
            PARAM_ERROR, msg="projectname error, check url")
    data = get_right_display_data(appname, projectname)
    return json_response_ok(data, msg="")


@app.route('/<appname>/module/list', methods=['GET', ])
@exception_handler
@access_control
def list_module(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    return module_list(appname)


@app.route('/<appname>/app/list', methods=['GET', ])
@exception_handler
@access_control
def list_app(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    return app_list(appname)


# get single user group right or mod user group right
@app.route('/<appname>/user/<uid>', methods=['GET', 'POST', 'OPTIONS'])
@exception_handler
@access_control
def user_edit(appname, uid):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if request.method == 'GET':
        # this method get user info by uid
        return user_get(appname, int(uid))
    elif request.method == 'POST':
        # this method mod user info
        try:
            modify_data = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("login para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
        return user_mod(appname, uid, modify_data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/group/<gid>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
def group_info(appname, gid):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if request.method == 'GET':
        # this method get group info by gid
        return group_get(appname, int(gid))
    elif request.method == 'POST':
        # this method mod group info
        try:
            modify_data = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("login para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
        return group_name_mod(appname, gid, modify_data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/<projectname>/module/<mid>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
def module_info(appname, projectname, mid):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR, msg="appname error, check url")
    if projectname not in NAV_DICT.keys():
        return json_response_error(
            PARAM_ERROR, msg="projectname error, check url")
    if request.method == 'GET':
        # this method get group info by gid
        return module_get(appname, int(mid))
    elif request.method == 'POST':
        # this method mod group info
        try:
            modify_data = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("module para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
        return module_mod(appname, mid, modify_data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/auth/app/<aid>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
def app_info(appname, aid):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if request.method == 'GET':
        # this method get group info by gid
        return app_get(appname, int(aid))
    elif request.method == 'POST':
        # this method mod group info
        try:
            modify_data = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("app para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
        return app_mod(appname, aid, modify_data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/perm/<pid>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
def right_info(appname, pid):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if request.method == 'GET':
        # this method get group right info by gid
        return right_get(appname, int(pid))
    elif request.method == 'POST':
        # this method mod group right info
        try:
            modify_data = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("add uesr para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
        return right_mod(appname, pid, modify_data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/<projectname>/group/perm/<pid>', methods=['POST', 'GET', 'OPTIONS'])
@exception_handler
@access_control
def group_right_info(appname, projectname, pid):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if projectname not in NAV_DICT.keys():
        return json_response_error(
            PARAM_ERROR, msg="projectname error, check url")
    if request.method == 'GET':
        # this method get group right info by gid
        return group_right_get(appname, projectname, pid)
    elif request.method == 'POST':
        # this method mod group right info
        try:
            modify_data = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("add uesr para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
        return group_right_mod(appname, projectname, pid, modify_data)
    else:
        return json_response_error(METHOD_ERROR)


@app.route('/<appname>/<projectname>/user/perm/<uid>', methods=['GET', 'POST', 'OPTIONS'])
@exception_handler
@access_control
def user_right_info(appname, projectname, uid):
    # check args
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    if projectname not in NAV_DICT.keys():
        return json_response_error(
            PARAM_ERROR, msg="projectname error, check url")
    if request.method == 'GET':
        # this method get right info by gid
        return user_right_get(appname, projectname, uid)
    elif request.method == 'POST':
        # this method mod user right info
        try:
            modify_data = ArmoryJson.decode(request.data)
        except ValueError as expt:
            _LOGGER.error("add uesr para except:%s", expt)
            return json_response_error(
                PARAM_ERROR, msg="json loads error,check parameters format")
        return user_right_mod(appname, projectname, uid, modify_data)
    else:
        return json_response_error(METHOD_ERROR)


# verify right
@app.route('/<appname>/perm/check', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def auth_right(appname):
    if appname not in MONGO_CONFIG:
        return json_response_error(PARAM_ERROR)
    for arg in ['perm_module', 'perm_opname', 'perm_action']:
        if arg not in request.args:
            return json_response_error(
                PARAM_REQUIRED, msg='not param:%s' % arg)
    if not session.get('uid'):
        return json_response_error(AUTH_ERROR)
    perm_module = request.form.get('perm_module')
    perm_opname = request.form.get('perm_opname')
    perm_action = request.form.get('perm_action')
    perm_lc = request.form.get('perm_lc')
    if not perm_lc:
        perm_lc = 'all'
    return check_session(
        appname, perm_module, perm_opname, perm_action,
        perm_lc, session['uid'])


# active user
@app.route('/<appname>/active/user', methods=['POST', 'OPTIONS'])
@exception_handler
@access_control
def active_user(appname):
    try:
        active_data = ArmoryJson.decode(request.data)
    except ValueError as expt:
        _LOGGER.error("module para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="json loads error,check parameters format")
    for arg in ['id', "is_active"]:
        if arg not in active_data:
            return json_response_error(
                PARAM_REQUIRED, msg='not param:%s' % arg)
    return user_active(appname, active_data)
