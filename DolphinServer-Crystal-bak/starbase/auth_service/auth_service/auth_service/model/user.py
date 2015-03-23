# -*- coding: utf-8 -*-
import logging
from armory.marine.util import md5_string
from armory.marine.util import now_timestamp, str2objid
from base import ModelBase


_LOGGER = logging.getLogger("model")


class User(ModelBase):
    collection = 'user'
    required = ('user_name', 'password')
    unique = ('user_name',)
    optional = (
        ('is_active', True),
        ('is_superuser', False),
        ('group_id', []),
        ('permission_list', {}),
        ('last_login', 0),
        ('department', ''),
        ('mark', '')
    )
    params = set(['user_name',  'group_id', 'mark'])

    @classmethod
    def new(
            cls, user_name, password, is_superuser, group_id,
            permission_list={}, is_active=True, department='', mark=''):
        '''
        create user instance
        '''
        instance = cls()
        instance.data = {}
        instance.data['is_superuser'] = False if not is_superuser else \
            is_superuser
        instance.data['is_active'] = True
        instance.data['user_name'] = user_name
        instance.data['password'] = User.calc_password_hash(
            '123456' if not password else password)
        instance.data['group_id'] = group_id
        instance.data['last_login'] = now_timestamp()
        instance.data['department'] = department
        instance.data['permission_list'] = permission_list
        instance.data['total_login'] = 1
        instance.data['mark'] = mark
        return instance

    @classmethod
    def save(cls, appname, instance):
        max_id = cls.find_max_id(appname) + 1
        instance.data["_id"] = max_id
        return cls.insert(appname, instance.data)

    @classmethod
    def update_user(cls, appname, cond, upt_dict):
        return cls.update(appname, cond, upt_dict)

    @classmethod
    def find_users(cls, appname, cond, fields={}, toarray=False):
        return cls.find(appname, cond, fields, toarray=toarray)

    @classmethod
    def find_one_user(cls, appname, cond={}, fields={}):
        users = cls.find(appname, cond, fields, toarray=True)
        if users:
            return users[0]
        else:
            return None

    @classmethod
    def del_user(cls, appname, uid):
        cond = {}
        cond["_id"] = int(uid)
        return cls.remove(appname, cond)

    @staticmethod
    def calc_password_hash(password):
        return unicode(md5_string(password))
