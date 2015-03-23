# -*- coding:utf-8 -*-
import logging
import os
from PIL import Image
import errno
import shutil


from resource_console.model.icon import Icon
from armory.marine.util import now_timestamp, unixto_string
from resource_console.utils.common import sdel, scp
from resource_console.model import ArmoryMongo
from resource_console import settings


_LOGGER = logging.getLogger(__name__)
PAGE_SIZE = 20
HOST = settings.HOST
MEDIA_ROOT = settings.MEDIA_ROOT
_ICON_BASE_DIR = "icon/"
DB_SERVERS = settings.REMOTEDB_SETTINGS
S3_DOMAIN = settings.S3_DOMAIN


def icon_info_list(
        appname, cond, fields=None, sort=None, page=0, page_size=PAGE_SIZE):
    icon = []
    icon_cursor = Icon.find_icon(appname, cond, fields)
    if sort is not None:
        icon_cursor = icon_cursor.sort(sort)
    icon_cursor = icon_cursor.skip(
        page * page_size).limit(page_size)
    total = Icon.find_icon(appname, cond).count()
    for item in icon_cursor:
        item["id"] = item["_id"]
        item["icon"] = "http://%s/media/%s" % (HOST, item['icon'])
        item.pop("_id")
        icon.append(item)
    data = {}
    data.setdefault("items", icon)
    data.setdefault("total", total)
    return data


def save_icon_info(appname, iconfile, icon_dict):
    icon_path = os.path.join(MEDIA_ROOT, _ICON_BASE_DIR, appname)
    if not os.path.exists(icon_path):
        os.makedirs(icon_path)
    iconfilepath = os.path.join(icon_path, icon_dict["icon"])
    iconfile.save(iconfilepath)
    try:
        image = Image.open(iconfilepath)
        icon_dict["height"], icon_dict["width"] = image.size
    except:
        icon_dict["height"], icon_dict["width"] = (0, 0)
    icon_dict["icon"] = _ICON_BASE_DIR + appname + '/' + icon_dict["icon"]

    icon_instance = Icon.new(icon_dict)
    Icon.save_icon(appname, icon_instance)
    _LOGGER.info("add a new icon:%s", icon_dict["title"])


def get_icon_by_id(appname, iconid, fields=None):
    icon_id = int(iconid)
    cond = {"_id": icon_id}
    icon_info = Icon.find_one_icon(appname, cond, fields)
    if icon_info:
        icon_info["id"] = icon_info["_id"]
        icon_info["icon"] = "http://%s/media/%s" % (HOST, icon_info['icon'])
        icon_info["last_modified"] = unixto_string(
            icon_info.get("last_modified"))
        icon_info.pop("_id")
        return icon_info
    else:
        return None


def update_icon_info(appname, iconid, iconfile, data):
    cond = {"_id": iconid}
    data["last_modified"] = now_timestamp()
    if data.get("id"):
        data.pop("id")
    icon_path = os.path.join(MEDIA_ROOT, _ICON_BASE_DIR, appname)
    if not os.path.exists(icon_path):
        os.makedirs(icon_path)
    if data.get("icon"):
        # remove old icon
        icon = Icon.find_one_icon(appname, cond, None)
        old_iconfilepath = os.path.join(icon_path, icon["icon"])
        if os.path.exists(old_iconfilepath):
            os.remove(old_iconfilepath)

        # save new icon
        iconfilepath = os.path.join(icon_path, data["icon"])
        iconfile.save(iconfilepath)
        try:
            image = Image.open(iconfilepath)
            data["height"], data["width"] = image.size
        except:
            data["height"], data["width"] = (0, 0)
        data["icon"] = _ICON_BASE_DIR + appname + '/' + data["icon"]

    Icon.update_icon(appname, cond, data)
    _LOGGER.info("update icon:%s success", iconid)
    return get_icon_by_id(appname, iconid)


def delete_icon_info(appname, icon_ids):
    success_ids = []
    invalid_ids = []
    refered_ids = []
    for icon_id in icon_ids:
        cond = {}
        cond["_id"] = int(icon_id)
        icon = Icon.find_one_icon(appname, cond, None)
        if icon:
            if icon["refered_info"]:
                _LOGGER.info("icon id %s is refer" % icon_id)
                refer_info = {"id":  icon_id, "refered_info": []}
                refer_info["refered_info"] = icon["refered_info"]
                refered_ids.append(refer_info)
            else:
                Icon.del_icon(appname, icon_id)
                success_ids.append({"id": icon_id})
        else:
            _LOGGER.info("icon id %s is not exist" % icon_id)
            invalid_ids.append(icon_id)
    return success_ids, refered_ids, invalid_ids


def get_icon_display_data(appname):
    sort = [("last_modified", -1)]
    fields = {"_id": 1, "title": 1}
    info = {"name": "platform", "items": []}
    platform_cursor = ArmoryMongo[appname]["platform"].find(
        {}, fields).sort(sort)
    for os_item in platform_cursor:
        plat_dict = {"display_value": "", "value": "", "children": {}}
        plat_dict["value"] = os_item.get("_id")
        plat_dict["display_value"] = os_item.get("title")
        plat_child = {"name": "package", "items": []}
        cond = {"platform": os_item["_id"]}
        package_cursor = ArmoryMongo[appname]["package"].find(
            cond, fields).sort(sort)
        for item in package_cursor:
            item_dict = {}
            item_dict["display_value"] = item.get("title")
            item_dict["value"] = item.get("_id")
            plat_child["items"].append(item_dict)
        plat_dict["children"] = plat_child
        info["items"].append(plat_dict)

    return info


def _save_icon_file(file_obj, appname):
    # save pic file to resource path
    # icon_name = file_obj.name.lower()
    icon_path = os.path.join(MEDIA_ROOT, _ICON_BASE_DIR, appname)
    if not os.path.exists(icon_path):
        os.makedirs(icon_path)
    iconfilepath = os.path.join(icon_path, file_obj)
    with open(iconfilepath, "wb") as picoutputfile:
        for chunk in file_obj.chunks():
            picoutputfile.write(chunk)

    # get icon file height and width
    try:
        image = Image.open(iconfilepath)
        height, width = image.size
    except:
        height, width = (0, 0)
    return height, width


def upload_icon_info(appname, icon_info, server, is_del=False):
    is_upload_server = "is_upload_%s" % server
    upload_server = "upload_%s" % server
    server_url = "%s_url" % server
    success_results = []
    failed_results = []
    duplicate_results = []
    for id_item in icon_info:
        cond = {}
        icon_id = int(id_item) if not isinstance(id_item, int) else id_item
        cond["_id"] = icon_id
        fields = {
            "title": 1, "icon": 1, is_upload_server: 1, server_url: 1, "id": 1}
        icon_info = Icon.find_one_icon(appname, cond, fields)
        if not icon_info:
            _LOGGER.error("icon:%s not in db", icon_id)
            continue
        icon_info["id"] = icon_info.pop("_id")
        icon_obj = icon_info.pop("icon")
        if is_del and not icon_info[is_upload_server]:
            _LOGGER.error("icon:%s already delete", icon_info['title'])
            duplicate_results.append(icon_info)
            continue
        result = _transfer_file(icon_obj, server, is_del)

        if not result[0]:
            _LOGGER.error("operation:%s failed", icon_info['title'])
            failed_results.append(icon_info)
            continue

        # update icon information in MongoDB
        update_info = {}
        update_info[is_upload_server] = False if is_del else True
        update_info[upload_server] = 0 if is_del else now_timestamp()
        update_info[server_url] = result[1]
        Icon.update_icon(appname, cond, update_info)

        _LOGGER.info("the id:%s is operator successful", icon_id)
        update_info["id"] = icon_id
        success_results.append(update_info)
    return success_results, failed_results, duplicate_results


def _transfer_file(file_obj, server, is_del=False, from_s3=True):
    if file_obj and server:
        local_base = MEDIA_ROOT
        server_conf = DB_SERVERS[server]
        remote_base = server_conf['remote_base'] if server_conf.get(
            'remote') else '/home/static/resources'
        s3_flag = False
        if from_s3 and server_conf.get('s3_remote'):
            remote_base = server_conf["s3_remote"]
            s3_flag = True
        remote = os.path.join(remote_base, file_obj)
        if is_del:
            if s3_flag:
                try:
                    os.unlink(remote)
                    result = True
                except OSError as e:
                    result = False
            else:
                result = sdel(
                    server_conf["statics"], 'static',
                    '/var/app/data/resource_console_service/static.pem',
                    remote)
            return (result, "")
        else:
            local = os.path.join(local_base, file_obj)
            if s3_flag:
                try:
                    mkdir = os.path.dirname(remote)
                    os.makedirs(mkdir)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise ValueError(
                            ('mkdir file path %s for s3 fail') % file_obj)
                try:
                    shutil.copy(local, remote)
                except EnvironmentError as e:
                    raise ValueError(('upload file %s to s3 fail') % file_obj)
                return (True, '%s/%s' % (S3_DOMAIN, file_obj))
            else:
                result = scp(
                    server_conf['statics'], 'static',
                    '/var/app/data/resource_console_service/static.pem',
                    local, remote)
                if not result:
                    raise ValueError(('upload file %s fail') % file_obj)
                    return (False,)
                else:
                    return (
                        True, 'http://%s/resources/%s' % (
                            server_conf['domain'], file_obj))
