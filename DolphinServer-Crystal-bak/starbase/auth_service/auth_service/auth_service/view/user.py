# -*- coding: utf-8 -*-
import logging
import re


from auth_service.model.user import User
from auth_service.model.group import Group
from auth_service.model.right import Right
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import AUTH_ERROR, PARAM_ERROR, PARAM_REQUIRED
from armory.marine.util import now_timestamp, str2objid,  unixto_string
from auth_service import settings

_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = settings.PAGE_LIMIT


def user_supervise(appname, uid):
    user_check = User.find_one_user(appname, {'_id': int(uid)}, None)
    if not user_check or not user_check['is_superuser']:
        return False
    return True


def user_login(appname, user_name, password, session):
    user_cond = {'user_name': user_name, 'password': password}
    user_check = User.find_one_user(appname, user_cond, None)
    if not user_check:
        return json_response_error(
            AUTH_ERROR, {}, msg='username or password err')
    elif not user_check["is_active"]:
        return json_response_error(AUTH_ERROR, {}, msg='user is not active')
    else:
        session["uid"] = int(user_check['_id'])
        uid = user_check['_id']
        upt_dict = {
            "last_login": now_timestamp(),
            "total_login": user_check.get("total_login") + 1}
        User.update_user(appname, {"_id": uid}, upt_dict)
        # 业务相关拆分
        # permissions = Permission.init_menu(uid)
        return json_response_ok({"uid": uid})


def user_chpasswd(appname, uid, old_pwd, new_pwd):
    usr = User.find_one_user(appname, {'_id': int(uid)}, None)
    if usr:
        if usr.get("password") == old_pwd:
            User.update_user(
                appname, {"_id": int(uid)}, {"password": new_pwd})
            return json_response_ok()
        else:
            _LOGGER.error('old_pwd err')
            return json_response_error(AUTH_ERROR)
    else:
        return json_response_error(AUTH_ERROR)


def user_list(appname, page=0, page_size=PAGE_SIZE, searchKeyword=None):
    '''
        list api for show user list.

        Request URL:  /appname/auth/user/list

        Http Method:  GET

        Parameters : None

        Return :
        {
        "status":0
        "data":{
                "items":[
                {
                "_id":"2",
                "user_name":"admin",
                "email":"xx@bainainfo.com",
                "permission_list":[19,20,21,22]
                },
                {
                    "_id":4,
                    "user_name":"translator",
                    "email":"xx@bainainfo.com",
                    "permission_list":[22,23]
                }
                ]
                }
            }

     '''
    cond = {}
    if searchKeyword:
        cond = search_cond(appname, searchKeyword)
    fields = {
        "password": 0, "super": 0, "permission_list": 0, "department": 0,
        "is_superuser": 0}
    sort = [("last_login", -1)]
    user_cursor = User.find_users(appname, cond, fields)
    if sort is not None:
        user_cursor = user_cursor.sort(sort)
    user_cursor = user_cursor.skip(
        page * page_size).limit(page_size)
    total = User.find_users(appname, cond).count()
    users = []
    for item in user_cursor:
        item["id"] = item.pop("_id")
        item["last_login"] = unixto_string(item.get("last_login"))
        item["role"] = get_role(appname, item["group_id"])
        users.append(item)
    data = {}
    data.setdefault("items", users)
    data.setdefault("total", total)
    return json_response_ok(data)


def user_info(appname, gid):
    '''
        get user info by group id

        Parameters : groupid

        Return :
        {
            "items":[
                {
                    "id":2,
                    "user_name":"admin@baina.com",
                    "role":[19,20,21,22],
                    "last_login":"2015-01-02",
                    "total_login": 2,
                    "mark": ""
                },
                {
                    "id":2,
                    "user_name":"admin@baina.com",
                    "role":[19,20,21,22],
                    "last_login":"2015-01-02",
                    "total_login": 2,
                    "mark": ""
                }
            ]
        }

     '''
    cond = {"group_id": gid}
    fields = {
        "password": 0, "super": 0, "permission_list": 0, "department": 0,
        "is_superuser": 0}
    sort = [("last_login", -1)]
    user_cursor = User.find_users(appname, cond, fields).sort(sort)
    users = []
    for item in user_cursor:
        item["id"] = item.pop("_id")
        item["last_login"] = unixto_string(item.get("last_login"))
        item["role"] = get_role(appname, item["group_id"])
        users.append(item)
    return users


def user_create(appname, user_data):
    '''
    create api to add user.
    '''
    user_name = user_data["user_name"]
    password = user_data.get("password", "123456")
    superuser = user_data.get("super")
    groups = [int(gid) for gid in user_data["group_id"]]
    mark = user_data.get("mark")
    if User.find_one_user(appname, {"user_name": user_name}):
        return json_response_error(
            PARAM_ERROR, msg="the user name exist")
    user_instance = User.new(user_name, password, superuser, groups, mark=mark)
    User.save(appname, user_instance)
    return json_response_ok()


def user_get(appname, user_id):
    '''
        this api is used to view one group
        Request URL: /auth/user/{gid}
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
        user_id = int(user_id)
    except ValueError as expt:
        _LOGGER.error("modify uesr para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="user_id error,check parameters format")
    fields = {"group_id": 1, "_id": 1, "user_name": 1, "mark": 1}
    user_info = User.find_one_user(appname, {'_id': user_id}, fields)
    if user_info:
        user_info["id"] = user_info["_id"]
        _LOGGER.info(user_info)
        return json_response_ok(user_info)
    else:
        return json_response_error(PARAM_ERROR, msg="not user:%s" % user_id)


def user_mod(appname, user_id, data):
    '''
        this api is used to modify one user
        Request URL: /auth/user/{uid}
        HTTP Method:POST
        Parameters: None
        Return :
        {
        "status":0
        "data":{
            "perm_list":[1,2,3,4],
            "disable_list":[1,2,3,4],
            "id": 1
            }
        "msg":""
        }
        '''
    try:
        uid = int(user_id)
    except ValueError as expt:
        _LOGGER.error("modify uesr para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="user_id error,check parameters format")
    for key in User.params:
        if key not in data:
            return json_response_error(PARAM_ERROR, msg="no param:%s" % key)
    cond = {"_id": uid}
    user = User.find_one_user(appname, cond, None)
    if not user:
        return json_response_error(PARAM_ERROR, msg="id:%s is invalid" % uid)
    user_name = data["user_name"]
    old_user = Group.find_one_group(appname, {"user_name": user_name})
    if old_user and old_user["_id"] != int(user_id):
        return json_response_error(PARAM_ERROR, msg="the user name exist")
    group_id = [int(gid) for gid in data["group_id"]]
    user_data = {
        "user_name": user_name, "mark": data["mark"], "group_id": group_id}
    User.update_user(appname, cond, user_data)
    return json_response_ok({})


def user_active(appname, data):
    '''
        this api is used to active one user
        Request URL: /auth/active/user/
        HTTP Method:POST
        Parameters: None
        Return :
        {
        "status":0
        "data":{
            "is_active":False,
            "id": 1
            }
        "msg":""
        }
        '''
    user_id = int(data["id"])
    cond = {"_id": user_id}
    user_info = User.find_one_user(appname, cond)
    if not user_info:
        return json_response_error(PARAM_ERROR, msg="the user id not exist")
    user_data = {"is_active": data["is_active"]}
    User.update_user(appname, cond, user_data)
    return json_response_ok(data)


def user_right_get(appname, projectname, uid):
    '''
        this api is used to get user perm list
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
        user_id = int(uid)
    except ValueError as expt:
        _LOGGER.error("get uesr perm list para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="user_id error,check parameters format")
    cond = {"_id": user_id}
    user_info = User.find_one_user(appname, cond, None)
    if not user_info:
        return json_response_error(
            PARAM_ERROR, msg="the user not exist")
    right_ids = []
    disable_right_ids = []
    if user_info:
        gids = user_info.get("group_id")
        user_perm_ids = user_info.get("permission_list")
        right_ids += user_perm_ids.get(projectname, [])
        for gid in gids:
            group_info = Group.find_one_group(appname, {"_id": gid}, None)
            if group_info:
                perm_ids = group_info.get("permission_list")
                perm_ids = perm_ids.get(projectname, [])
                right_ids.extend(perm_ids)
                disable_right_ids.extend(perm_ids)
        if right_ids:
            right_ids = list(set(right_ids))
        if disable_right_ids:
            disable_right_ids = list(set(disable_right_ids))
    rights = {}
    rights.setdefault("perm_list", right_ids)
    rights.setdefault("disable_list", disable_right_ids)
    rights.setdefault("id", uid)
    return json_response_ok(rights)


def user_right_mod(appname, projectname, uid, data):
    '''
        this api is used to modify one group
        Request URL: /auth/user/{gid}
        HTTP Method:POST
        Parameters:
        {
           "perm_list":[1,2,3,4]
           "disable_list":[1,2,3,4]
        }
        Return :
        {
            "status":0
            "data":{}
        }
        '''
    try:
        user_id = int(uid)
    except ValueError as expt:
        _LOGGER.error("modify uesr para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="user_id error,check parameters format")

    # check param
    for key in ["perm_list", "disable_list"]:
        if key not in data:
            return json_response_error(PARAM_REQUIRED, msg="no param:%s" % key)

    # check if user id in db
    cond = {"_id": user_id}
    fields = {"_id": 0}
    user_info = User.find_one_user(appname, cond, fields)
    if not user_info:
        return json_response_error(PARAM_ERROR, msg="the user not exist")

    # check if right id in db
    right_list = [int(rid) for rid in data["perm_list"]]
    right_list = list(set(right_list))
    for rid in right_list:
        if not Right.find_one_right(appname, {"_id": rid}):
            return json_response_error(
                PARAM_ERROR, msg="the right id:%s not exist" % rid)

    group_perm_ids = []
    gids = user_info.get("group_id")
    for gid in gids:
        group_info = Group.find_one_group(appname, {"_id": gid}, None)
        if group_info:
            perm_ids = group_info.get("permission_list")
            group_perm_ids += perm_ids.get(projectname, [])
    if group_perm_ids:
        group_perm_ids = list(set(group_perm_ids))

    # update user right info
    user_right_list = []
    for rid in right_list:
        if rid not in group_perm_ids:
            user_right_list.append(rid)
    user_info["permission_list"][projectname] = user_right_list
    User.update_user(appname, cond, user_info)
    return json_response_ok({}, msg="update user right success")


def user_delete(appname, uid):
    '''
        this api is used to delete user.

        Request URL: /auth/user/delete

        HTTP Method: POST

        Parameters:
            {
                "uids": 3
            }

        Return:
        {
        "status":0
        "data":{}
        "msg":"delete successfully"
        }
    '''
    uid = int(uid)
    user = User.find_one_user(appname, {"_id": uid}, None)
    if user:
        User.del_user(appname, uid)
        return json_response_ok({"id": uid}, msg="delete user success")
    else:
        return json_response_error(PARAM_ERROR, msg="id:%s is invalid" % uid)


def search_cond(appname, search_keyword):
    cond = {}
    cond_list = []
    try:
        id_cond = {}
        id_cond["_id"] = int(search_keyword)
        cond_list.append(id_cond)
    except:
        _LOGGER.debug("not a number string")
    string_fields = ["user_name", ]
    for field in string_fields:
        string_cond = {}
        string_cond[field] = {"$regex": re.escape(search_keyword)}
        cond_list.append(string_cond)
    cond["$or"] = cond_list
    return cond


def get_role(appname, gids):
    roles = []
    for gid in gids:
        group_id = int(gid)
        cond = {"_id": group_id}
        group_info = Group.find_one_group(appname, cond, None)
        roles.append(group_info["group_name"])
    return roles
