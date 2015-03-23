# -*- coding: utf-8 -*-
import logging
from auth_service.model.group import Group
from auth_service.model.right import Right
from armory.marine.json_rsp import json_response_ok, json_response_error
from armory.marine.respcode import PARAM_ERROR, PARAM_REQUIRED
from auth_service import settings
from auth_service.view.user import user_info

_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = settings.PAGE_LIMIT
DATA_RELETED_BY_OTHER = 1004


def group_create(appname, group_name, perm_list={}):
    '''
    create api to add group.
    Request URL:  /auth/group/add
    Http Method:  POST
    Parameters:
        {
           "group_name":"xxx",
           "perm_list":{}
        }
    Return :
    {
     "status":0
     "data":{}
    }
    '''
    if Group.find_one_group(appname, {"group_name": group_name}):
        return json_response_error(
            PARAM_ERROR, msg="the groupname exist")
    group_instance = Group.new(group_name, perm_list)
    Group.save(appname, group_instance)
    cond = {"group_name": group_name}
    group_info = Group.find_one_group(
        appname, cond, {"_id": 1, "group_name": 1})
    group_info["id"] = group_info["_id"]
    return json_response_ok(group_info)


def group_list(appname, page=0, page_size=PAGE_SIZE):
    '''
    list api for show group list.
    Request URL:  /auth/group/list
    Http Method:  GET
    Parameters : None
    Return :
    {
     "status":0
     "data":{
              "items":[
                {
                "_id":"2",
                "group_name":"admin",
                "permission_list":[19,20,21,22]
                },
                {
                    "_id":4,
                    "group_name":"translator",
                    "permission_list":[22,23]
                }
              ]
            }
        }

    '''
    cond = {}
    fields = {"_id": 1, "group_name": 1}
    sort = [("_id", 1)]
    group_cursor = Group.find_group(appname, cond, fields)
    if sort is not None:
        group_cursor = group_cursor.sort(sort)
    group_cursor = group_cursor.skip(
        page * page_size).limit(page_size)
    total = Group.find_group(appname, cond).count()
    groups = []
    for item in group_cursor:
        item["id"] = item.pop("_id")
        groups.append(item)
    data = {}
    data.setdefault("items", groups)
    data.setdefault("total", total)
    return json_response_ok(data)


def group_get(appname, gid):
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
                        "last_login":"2014-4-10"
                    }
            }
    '''
    try:
        group_id = int(gid)
    except ValueError as expt:
        _LOGGER.error("modify uesr para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="group_id error,check parameters format")
    group_info = user_info(appname, group_id)
    data = {}
    data.setdefault("items", group_info)
    return json_response_ok(data)


def group_name_mod(appname, gid, data):
    '''
        this api is used to modify one group
        Request URL: /auth/user/{gid}
        HTTP Method:POST
        Parameters:
        {
           "group_name":"xxx",
        }
        Return :
        {
            "status":0
            "data":{}
        }
        '''
    try:
        gid = int(gid)
    except ValueError as expt:
        _LOGGER.error("modify group para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="group_id error,check parameters format")
    for key in Group.params:
        if key not in data:
            return json_response_error(PARAM_REQUIRED, msg="no param:%s" % key)
    group_name = data["group_name"]
    old_group = Group.find_one_group(appname, {"group_name": group_name})
    if old_group and old_group["_id"] != gid:
        return json_response_error(
            PARAM_ERROR, msg="the groupname exist")
    cond = {"_id": gid}
    Group.update_group(appname, cond, data)
    group_info = Group.find_one_group(
        appname, cond, {"_id": 1, "group_name": 1})
    group_info["id"] = group_info["_id"]
    return json_response_ok(group_info)


def group_right_get(appname, projectname, gid):
    '''
        this api is used to get group perm list
        Request URL: /auth/user/{uid}
        HTTP Method:POST
        Parameters:None
        Return :
        {
        "status":0
        "data":{
            "perm_list":[1,2,3,4],
            "id": 1
            }
        "msg":""
        }
        '''
    try:
        group_id = int(gid)
    except ValueError as expt:
        _LOGGER.error("get uesr perm list para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="user_id error,check parameters format")
    cond = {"_id": group_id}
    group_info = Group.find_one_group(appname, cond, None)
    if not group_info:
        return json_response_error(
            PARAM_ERROR, msg="the group not exist")
    right_ids = group_info.get("permission_list")
    right_ids = right_ids.get(projectname, [])
    rights = {}
    rights.setdefault("perm_list", right_ids)
    rights.setdefault("id", group_id)
    return json_response_ok(rights)


def group_right_mod(appname, projectname, gid, data):
    '''
        this api is used to modify one group
        Request URL: /auth/user/{gid}
        HTTP Method:POST
        Parameters:
        {
           "perm_list":[1,2,3,4]
        }
        Return :
        {
            "status":0
            "data":{}
        }
        '''
    try:
        gid = int(gid)
    except ValueError as expt:
        _LOGGER.error("modify group para except:%s", expt)
        return json_response_error(
            PARAM_ERROR, msg="group_id error,check parameters format")
    # check param
    for key in ["perm_list", ]:
        if key not in data:
            return json_response_error(PARAM_REQUIRED, msg="no param:%s" % key)

    # check if group id in db
    cond = {"_id": gid}
    fields = {"_id": 0}
    group_info = Group.find_one_group(appname, cond, fields)
    if not group_info:
        return json_response_error(PARAM_ERROR, msg="the group not exist")

    right_list = [int(rid) for rid in data["perm_list"]]
    right_list = list(set(right_list))

    # check if right id in db
    for rid in right_list:
        if not Right.find_one_right(appname, {"_id": rid}):
            return json_response_error(
                PARAM_ERROR, msg="the right id:%s not exist" % rid)

    # update group right info
    group_info["permission_list"][projectname] = right_list
    Group.update_group(appname, cond, group_info)
    return json_response_ok({}, msg="update group right success")


def group_delete(appname, gid):
    '''
    this api is used to delete group,when one group removed,the user who
    in this group ,the group id will remove too.
    Request URL: /auth/group/delete
    HTTP Method: POST
    Parameters:
        {
            "gids":3
        }
    Return:
     {
     "status":0
     "data":{}
     "msg":"delete successfully"
     }
    '''
    gid = int(gid)
    group = Group.find_one_group(appname, {"_id": gid}, None)
    data = {"id": gid}
    if group:
        users = user_info(appname, int(gid))
        if users:
            _LOGGER.info("group id %s is refer" % gid)
            return json_response_error(DATA_RELETED_BY_OTHER, data)
        else:
            Group.del_group(appname, gid)
            return json_response_ok(data, msg="delete group success")
    else:
        _LOGGER.info("group id %s is not exist" % gid)
        return json_response_error(
            PARAM_ERROR, data, msg="invalid group id,check parameters")


def _gid2name(appname, gids):
    assert(isinstance(gids, list))
    namedict = {}
    for gid in gids:
        group = Group.find_one_group(appname, {"_id": gid})
        namedict[gid] = group['group_name']
    return namedict


def get_role_display_data(appname):
    sort = [("last_modified", -1)]
    fields = {"_id": 1, "group_name": 1}
    info = {"name": "role", "items": []}
    group_cursor = Group.find_group(appname, {}, fields).sort(sort)
    for role_item in group_cursor:
        role_dict = {"display_value": "", "value": ""}
        role_dict["value"] = role_item.get("_id")
        role_dict["display_value"] = role_item.get("group_name")
        info["items"].append(role_dict)

    return info
