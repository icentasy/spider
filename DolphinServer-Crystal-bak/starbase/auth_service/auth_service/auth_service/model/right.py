# -*- coding: utf-8 -*-
import logging
from base import ModelBase

_LOGGER = logging.getLogger("model")


class Right(ModelBase):
    collection = 'permission'
    required = ('perm_name', 'module', 'app_label', 'action')
    unique = ('perm_name',)
    optional = (
        ('lc', '')
    )
    params = set(['module', 'app_label', 'action'])

    @classmethod
    def new(
            cls, appname, projectname, perm_module, perm_opname, perm_action,
            perm_type="module", perm_lc=''):
        '''
        create right instance
        '''
        instance = cls()
        instance.data = {}
        perm_name = '%s-%s-%s' % (perm_opname, perm_module, perm_action)

        instance.data['perm_name'] = perm_name
        instance.data['app_name'] = projectname
        instance.data['app_label'] = perm_opname
        instance.data['module'] = perm_module
        instance.data['action'] = perm_action
        instance.data['lc'] = perm_lc
        instance.data['perm_type'] = perm_type
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance.data['_id'] = max_id
        return cls.insert(appname, instance.data)

    @classmethod
    def update_right(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_right(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_right(cls, appname, cond, fields={}):
        users = cls.find(appname, cond, fields, toarray=True)
        if users:
            return users[0]
        else:
            return None

    @classmethod
    def del_right(cls, appname, rids):
        no_rid = []
        for rid in rids:
            right = cls.find_right(appname, {"_id": int(rid)})
            if right:
                cls.remove(appname, {"_id": int(rid)})
                _LOGGER.info("remove user id %d" % int(rid))
            else:
                _LOGGER.info("rid %d is not exist" % int(rid))
                no_rid.append(rid)
        return no_rid
