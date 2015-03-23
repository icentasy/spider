# -*- coding: utf-8 -*-

"""custom filter contains 3 kinds type:
    1. A function, including 2 kinds:
        - just a function, call it without any para, can be lambda;
        - a tuple, include (func, [args], {kargs}), parms will send when call;

    2. An object of a subclass of `CustomFilter`, you can write `__init__` as
    you like, `obj.get_value()` will be called without any parms.

"""

import inspect
import pytz
from datetime import datetime, timedelta


def get_filter_value(v):
    if inspect.isfunction(v):
        return v()
    elif isinstance(v, tuple):
        func = v[0]
        args = v[1]
        try:
            kwargs = v[2]
        except IndexError:
            kwargs = {}
        return func(*args, **kwargs)
    elif isinstance(v, CustomFilter):
        return v.get_value()
    else:
        return v


def n_days_ago(n, f='%Y%m%d', time_zone='utc'):
    tz = pytz.utc
    if time_zone.lower() != 'utc':
        tz = pytz.timezone(time_zone)
    return (datetime.now(tz).date() - timedelta(days=n)).strftime(f)


class CustomFilter(object):

    """An interface for special view filter, exec it every time but not just
    once."""

    def get_value(self):
        raise NotImplementedError('get_value is a virtual func')
