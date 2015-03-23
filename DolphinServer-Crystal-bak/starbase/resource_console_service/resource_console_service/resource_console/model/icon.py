# -*- coding:utf-8 -*-
import logging


from resource_console.model.base import ModelBase
from armory.marine.util import now_timestamp


_LOGGER = logging.getLogger("model")


class Icon(ModelBase):
    collection = 'icon'
    required = ('title', "icon", "platfrom")
    unique = ('title',)
    optional = (
        ("width", 0), ("height", 0),
        ("package", []), ("type", []),
        ("local_url", ""), ("ec2_url", ""),
        ("is_upload_local", False), ("id_upload_ec2", False),
        ("upload_local", 0), ("upload_ec2", 0),
        ("first_created", now_timestamp), ("last_modified", now_timestamp),
        ("refered_info", []))
    params = set(['title', ])

    @classmethod
    def new(cls, faq_dict):
        """
        creat icon instance
        """
        instance = cls()
        instance.title = faq_dict["title"]
        instance.icon = faq_dict["icon"]
        instance.platform = faq_dict["platform"]
        instance.width = faq_dict["width"] if faq_dict.get("width") else 0
        instance.height = faq_dict["height"] if faq_dict.get("height") else 0
        instance.package = faq_dict["package"]
        instance.type = faq_dict["type"]
        instance.is_upload_local = False
        instance.is_upload_ec2 = False
        instance.upload_local = 0
        instance.upload_ec2 = 0
        instance.local_url = ""
        instance.ec2_url = ""
        instance.refered_info = []
        instance.first_created = now_timestamp()
        instance.last_modified = now_timestamp()
        return instance

    @classmethod
    def save_icon(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance._id = max_id
        return cls.insert(appname, instance)

    @classmethod
    def update_icon(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_icon(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_icon(cls, appname, cond, fields={}):
        icons = cls.find(appname, cond, fields, toarray=True)
        if icons:
            return icons[0]
        else:
            return None

    @classmethod
    def del_icon(cls, appname, icon_id):
        cond = {}
        cond["_id"] = int(icon_id)
        return cls.remove(appname, cond)
