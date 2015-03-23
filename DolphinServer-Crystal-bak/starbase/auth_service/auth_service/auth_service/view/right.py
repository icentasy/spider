# -*- coding: utf-8 -*-
import logging


from auth_service.model.user import User
from auth_service.settings import NAV_DICT
from auth_service.model.group import Group
from auth_service.model.right import Right
from auth_service.model.apps import App
from auth_service.model.module import Module
from auth_service.view.apps import order_app
from auth_service.view.modules import order_module
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import AUTH_ERROR, PARAM_ERROR

_LOGGER = logging.getLogger(__name__)


def right_create(
        appname, projectname, perm_module, perm_opname, perm_action='list',
        perm_type="module", perm_lc='all'):
    '''
    create api to add right.
    Parameters:
    {
    'perm_type': 'module',
    'perm_name': 'aospreset-aosrecommendshare-list',
    'perm_container': 'aospreset',
    'perm_lc': 'zh-cn'
    }
    '''
    perm_name = '%s-%s-%s' % (perm_opname, perm_module, perm_action)
    right_cond = {
        'perm_name': perm_name, 'app_name': projectname, "perm_lc": perm_lc}
    if Right.find_one_right(appname, right_cond):
        return json_response_error(PARAM_ERROR, msg="the right exist")
    if not App.find_one_app(appname, {"name": perm_opname}):
        return json_response_error(PARAM_ERROR, msg="the app label not exist")
    if not Module.find_one_module(appname, {"module_name": perm_module}):
        return json_response_error(
            PARAM_ERROR, msg="the app module not exist")
    right_instance = Right.new(
        appname, projectname, perm_module, perm_opname, perm_action,
        perm_type, perm_lc)
    Right.save(appname, right_instance)
    return json_response_ok()


def right_delete(appname, pids):
    '''
    delete right
    '''
    pidlist = pids.split(',')
    ids = Right.del_right(appname, pidlist)
    if not ids:
        return json_response_ok()
    else:
        return json_response_error(PARAM_ERROR, msg="ids:%s is invalid" % ids)


def right_list(appname):
    sort = [("_id", 1)]
    right_cursor = Right.find_right(appname, cond={}, fields=None)
    if sort is not None:
        right_cursor = right_cursor.sort(sort)
    total = Right.find_right(appname, {}).count()
    rights = []
    for item in right_cursor:
        item["id"] = item.pop("_id")
        rights.append(item)
    data = {}
    data.setdefault("items", rights)
    data.setdefault("total", total)
    return json_response_ok(data)


def right_get(appname, rid):
    '''
        this api is used to view one right
        Request URL: /auth/right/{rid}
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
                        "last_login":"2014-4-10"
                    }
            }
    '''
    try:
        right_id = int(rid)
    except ValueError as expt:
        _LOGGER.error("get right para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="right_id error,check parameters format")
    right_info = Right.find_one_right(appname, {'_id': right_id}, None)
    if right_info:
        return json_response_ok(right_info)
    else:
        return json_response_error(PARAM_ERROR, msg="not app:%s" % right_id)


def right_mod(appname, rid, data):
    '''
        this api is used to modify one right
        Request URL: /auth/user/{uid}
        HTTP Method:POST
        Parameters:
            {
            "group_name":"xxx",
            "perm_list":[1,2,3,4]
            }
        Return :
        {
        "status":0
        "data":{}
        "msg":"modify successfully"
        }
        '''
    try:
        right_id = int(rid)
    except ValueError as expt:
        _LOGGER.error("modify uesr para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="right_id error,check parameters format")
    cond = {"_id": right_id}
    for key in data:
        if key not in Right.params:
            json_response_error(PARAM_ERROR, msg="unnecessary param:%s" % key)
    if not App.find_one_app(appname, {"name": data["app_label"]}):
        return json_response_error(PARAM_ERROR, msg="the app label not exist")
    if not Module.find_one_module(appname, {"module_name": data["module"]}):
        return json_response_error(PARAM_ERROR, msg="the app module not exist")
    perm_name = '%s-%s-%s' % (
        data["app_label"], data["module"], data["action"])
    data["perm_name"] = perm_name
    Right.update_right(appname, cond, data)
    return json_response_ok()


def menu_list(appname, projectname, uid):
    uid = int(uid)
    cond = {"_id": uid}
    user_info = User.find_one_user(appname, cond, None)
    if not user_info:
        return json_response_error(PARAM_ERROR, msg="the user not exist")
    menu = init_menu_list(appname, projectname, uid)
    permissions = init_perms_list(appname, projectname, uid)
    features = init_features(appname, projectname, uid)
    total_login = user_info.get("total_login")
    data = {}
    data.setdefault("menu", menu)
    data.setdefault("permissions", permissions)
    if total_login == 2:
        data.setdefault("need_changepwd", True)
    else:
        data.setdefault("need_changepwd", False)
    data.setdefault("features", features)
    return json_response_ok(data)


def navigate_list(appname, uid):
    try:
        uid = int(uid)
    except ValueError as expt:
        _LOGGER.error("get navigate para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="uid error,check parameters format")
    cond = {"_id": uid}
    user_info = User.find_one_user(appname, cond, None)
    if not user_info:
        return json_response_error(PARAM_ERROR, msg="the user not exist")
    nav = init_navigate_list(appname, uid)
    data = {}
    data.setdefault("navigate", nav)
    return json_response_ok(data)


def check_session(appname, module, opname, action, lc, uid):
    '''
    check user right
    '''
    rightids = []
    perm_names = ['%s-%s-%s' % (opname, module, action), ]
    for perm_name in perm_names:
        perm = Right.find_one_right(appname, {'perm_name': perm_name})
        if perm:
            if perm['_id'] not in rightids:
                rightids.append(perm['_id'])
    usr = User.find_one_user({'_id': uid})
    usrights = usr['permission_list']
    if not usr:
        return json_response_error(AUTH_ERROR)
    if usr['is_superuser']:
        return json_response_ok()
    usrgroup = usr['group_id']
    for group in usrgroup:
        group_info = Group.find_one_group({'_id': group})
        usrights.extend(group_info['permission_list'])
    for rightid in rightids:
        if rightid in usrights:
            return json_response_ok()
    return json_response_error(AUTH_ERROR)


def get_perms_by_uid(appname, projectname, uid, perm_type="module"):
    right_ids = []
    cond = {"_id": uid}
    user_info = User.find_one_user(appname, cond, None)
    perm_cond = {"app_name": projectname, "perm_type": perm_type}
    if user_info.get("is_superuser"):
        return Right.find_right(appname, perm_cond, {"_id": 1}, toarray=True)
    else:
        user_right_info = user_info.get("permission_list")
        right_ids = user_right_info.get(projectname, [])
        gids = user_info.get("group_id")
        if gids:
            for gid in gids:
                group_info = Group.find_one_group(appname, {"_id": gid}, None)
                if group_info:
                    group_right_info = group_info.get("permission_list")
                    right_ids += group_right_info.get(projectname, [])
        if right_ids:
            right_ids = list(set(right_ids))
        return get_perms_by_ids(appname, projectname, right_ids, perm_type)


def get_perms_by_ids(appname, projectname, pids, perm_type="module"):
    '''
    an internal function for getting permissions by id array
    '''
    permissions = []
    for pid in pids:
        perm_cond = {
            "app_name": projectname, "_id": pid, "perm_type": perm_type}
        perm = Right.find_one_right(appname, perm_cond, None)
        if perm:
            permissions.append(perm)
    return permissions


def get_right_display_data(appname, projectname):
    sort = [("_id", 1)]
    fields = {"app_label": 1, "_id": 0}
    model_cond = {"app_name": projectname, "perm_type": "module"}
    menu = {"items": []}
    app_list = Right.find_right(appname, model_cond, fields, True)
    f = lambda x, y: x if y["app_label"] in [i["app_label"] for i in x] \
        else x + [y]
    app_list = reduce(f, [[], ] + app_list)
    for app_item in app_list:
        app_fields = {"_id": 1, "module": 1}
        app_info = App.find_one_app(
            appname, {"name": app_item["app_label"]}, None)
        app_dict = {"title": "", "items": []}
        app_dict["title"] = app_info["app_value"]
        module_cond = {
            "app_name": projectname, "app_label": app_item["app_label"],
            "perm_type": "module"}
        module_cursor = Right.find_right(
            appname, module_cond, app_fields, True)
        f = lambda x, y: x if y["module"] in [i["module"] for i in x] \
            else x + [y]
        module_list = reduce(f, [[], ] + module_cursor)
        for module_item in module_list:
            action_fields = {"_id": 1, "action": 1}
            action_cond = {
                "app_name": projectname, "app_label": app_item["app_label"],
                "perm_type": "module", 'module': module_item["module"]}
            action_cursor = Right.find_right(
                appname, action_cond, action_fields).sort(sort)
            module_dict = Module.find_one_module(
                appname, {"module_name": module_item["module"]}, None)
            action_dict = {"model": module_item["module"], "items": []}
            action_dict["model"] = module_dict["module_value"]
            for menu_item in action_cursor:
                role_dict = {"display_value": "", "value": ""}
                role_dict["value"] = menu_item.get("_id")
                role_dict["display_value"] = menu_item.get("action")
                action_dict["items"].append(role_dict)
            app_dict["items"].append(action_dict)
        menu["items"].append(app_dict)

    # get feature display data
    feature_cond = {"app_name": projectname, "perm_type": "feature"}
    feature_fields = {"perm_name": 1, "_id": 1}
    feature = {"items": [], "title": "Feature"}
    feature_list = Right.find_right(
        appname, feature_cond, feature_fields, True)
    if feature_list:
        for feature_item in feature_list:
            feature_dict = {"display_value": "", "value": ""}
            feature_dict["value"] = feature_item.get("_id")
            feature_dict["display_value"] = feature_item.get("perm_name")
            feature["items"].append(feature_dict)
    menu.setdefault("feature", feature)

    return menu


def init_menu_list(appname, projectname, uid):
    '''
    init menu for user by uid
    it is dynamic, it is combined with user's permissions
    '''
    menu = []
    perms = get_perms_by_uid(appname, projectname, uid)
    if perms:
        apps = []
        for perm in perms:
            apps.append(perm.get('app_label'))
        if apps:
            apps = list(set(apps))
        else:
            return apps
        # order the apps
        apps = order_app(appname, projectname, apps)
        # order the modules
        for app in apps:
            app_info = App.find_one_app(appname, {"name": app}, None)
            menu_item = {"module": app, "items": []}
            menu_item["display"] = app_info["app_value"]
            modules = []
            for perm in perms:
                if perm.get('app_label') == app:
                    modules.append(perm.get('module'))
            module_items = []
            if modules:
                modules = list(set(modules))
                modules = order_module(appname, projectname, modules)
                for module in modules:
                    module_dict = Module.find_one_module(
                        appname, {"module_name": module}, None)
                    temp = {'model': module}
                    temp['display'] = module_dict["module_value"]
                    temp['url'] = app + '/' + module
                    module_items.append(temp)
            menu_item["items"] = module_items
            menu.append(menu_item)
    return menu


def init_features(appname, projectname, uid):
    '''
    some feature function
    return like this:
        {
            "features":[a,b]
            }
    '''
    feature = []
    perms = get_perms_by_uid(appname, projectname, uid, "feature")
    for perm in perms:
        feature.append(perm.get("perm_name"))
    return feature


def init_perms_list(appname, projectname, uid):
    '''
    return values like below:
        [{
        "model":"xxx",
        "action":[add,edit]
        } ]
    '''
    assert uid
    permissions = []
    models = []
    perms = get_perms_by_uid(appname, projectname, uid)
    for perm in perms:
        model_name = perm.get("module")
        models.append(model_name)
        models = list(set(models))
    for model in models:
        temp = {}
        temp["model"] = model
        for perm in perms:
            model_label = perm.get("module")
            action = perm.get("action")
            if model == model_label:
                temp.setdefault("action", []).append(action)
        permissions.append(temp.copy())
    return permissions


def init_navigate_list(appname, uid):
    '''
    return values like below:
        [
            {
            "display_value":"环信",
            "value":"square_console"
            }
        ]
    '''
    assert uid
    cond = {"_id": uid}
    user_info = User.find_one_user(appname, cond, None)
    app_names = []
    if user_info.get("is_superuser"):
        app_names = Right.find_right(
            appname, {}, {"app_name": 1}, toarray=True)
    else:
        user_right_info = user_info.get("permission_list")
        # get user privately-owned right
        for app_name in user_right_info:
            if user_right_info.get(app_name):
                app_names.append(app_name)

        # get user publicly-owned right
        gids = user_info.get("group_id")
        if gids:
            for gid in gids:
                group_info = Group.find_one_group(appname, {"_id": gid}, None)
                if group_info:
                    group_right_info = group_info.get("permission_list")
                    for app_name in group_right_info:
                        if group_right_info.get(app_name):
                            app_names.append(app_name)
                else:
                    _LOGGER.error("group id:%s error", gid)
    navigates = []
    if app_names:
        app_names = list(set(app_names))
        for app_name in app_names:
            app_dict = {}
            app_display = NAV_DICT.get(app_name)
            app_dict.setdefault("display_value", app_display)
            app_dict.setdefault("value", app_name)
            navigates.append(app_dict)
    return navigates
