# -*- coding: utf-8 -*-
import logging

_LOGGER = logging.getLogger('armory')


class ParamError(Exception):
    def __init__(self, msg):
        self.msg = 'Parameter error, %s' % msg


class AuthFailureError(Exception):
    def __init__(self, msg):
        self.msg = 'AuthFailure ERROR, %s' % msg


class UnknownError(Exception):
    def __init__(self, msg):
        self.msg = 'UnKnown ERROR, %s' % msg


class UniqueCheckError(ValueError):
    pass


class DbError(Exception):
    def __init__(self, msg):
        self.msg = 'DataBase ERROR, %s' % msg


class DataError(ValueError):
    def __init__(self, msg):
        self.msg = 'Data ERROR, %s' % msg
