# -*- coding: utf-8 -*-


class GeneralError(Exception):
    def __init__(self, msg):
        self.msg = 'Parameter error, %s' % msg

    def __str__(self):
        return self.msg


class ParamError(GeneralError):
    def __init__(self, msg):
        self.msg = 'Parameter error, %s' % msg


class AuthFailureError(GeneralError):
    def __init__(self, msg):
        self.msg = 'AuthFailure ERROR, %s' % msg


class UnknownError(GeneralError):
    def __init__(self, msg):
        self.msg = 'UnKnown ERROR, %s' % msg


class DbError(GeneralError):
    def __init__(self, msg):
        self.msg = 'DataBase ERROR, %s' % msg


class DataError(GeneralError):
    def __init__(self, msg):
        self.msg = 'Data ERROR, %s' % msg
