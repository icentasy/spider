#  -*- coding:utf-8 -*-
"""
    multalisk.model.base
    ~~~~~~~~~~~~~~~~~~~~

    Defines meta class for Model Class

"""
import logging
from collections import deque
from datetime import datetime

from multalisk.model import MODEL_CONF

from armory.tank.mysql import _InnerDeclarativeMeta
from armory.tank.mongo import ArmoryMongo


_LOGGER = logging.getLogger(__name__)


def _register_model(model_class, model_id):
    """This function used for register a Model Class to a model id
    In API Layer, when received a request for data, we check the model id,
    then, get the Model Class by query MODEL_CONF.So, we need to register
    the Model Class to model id at the time of class creating.
    """
    if model_id not in MODEL_CONF:
        raise Exception('model id[%s] not is MODEL_CONF!')

    MODEL_CONF[model_id].update({'model_class': model_class})


class MetaSQL(_InnerDeclarativeMeta):

    """Meta Class for SQL ORM Model

    Each ORM Model must has as `orm.Model` base class used for query mapping,
    and the base class will be assigned at `MetaSQL`:`__new__` by `model_id`
    """

    def __new__(self, name, bases, attrs):
        model_id = attrs.pop('__modelid__', None)
        if not model_id or not MODEL_CONF.get(model_id):
            _LOGGER.warn('MetaSQL:modelid in model %s invalid!' % name)
            return

        db_type = MODEL_CONF[model_id]['db_type']
        mapped_db = MODEL_CONF[model_id]['mapped_db']
        if db_type == 'mysql':
            # if mysql, we change the base class for it
            bases = (mapped_db.Model,)
        else:
            # else not support yet...
            raise Exception('db type %s Not Support by SQLBase!' % db_type)

        new_class = _InnerDeclarativeMeta.__new__(self, name, bases, attrs)
        _register_model(new_class, model_id)
        return new_class


class MetaMongo(type):

    """Meta Class for Mongo Model

    a `query` attribute will be add to Mongo Model class
    at `MetaMongo`:`__new__`
    """

    def __new__(self, name, bases, attrs):
        model_id = attrs.pop('__modelid__', None)
        if not model_id or not MODEL_CONF.get(model_id):
            _LOGGER.warn('MetaMongo:modelid in model %s invalid!' % name)
            return

        db_type = MODEL_CONF[model_id]['db_type']
        db_route = MODEL_CONF[model_id]['mapped_db']
        if db_type == 'mongo':
            # if mongo, we construct query for it
            collection = attrs.pop('__collection__', None)
            attrs['query'] = ArmoryMongo[db_route][collection]
        else:
            raise Exception('db type %s Not Support by MongoBase!' % db_type)

        new_class = type.__new__(self, name, bases, attrs)
        _register_model(new_class, model_id)
        return new_class


class MetaHive(type):

    class __HiveQuery(object):

        def __init__(self, db, t_name, t_attrs):
            self._db = db
            self._t_name = t_name
            self._t_attrs = t_attrs
            self._filters = ""
            self._limit = ""
            self._offset = ""
            self._distinct_field = ""
            self.__data = deque()

        def filter(self, filters):
            self._filters = filters
            return self

        def limit(self, limit):
            self._limit = limit
            return self

        def offset(self, offset):
            self._offset = offset
            return self

        def distinct(self, field_name):
            self._distinct_field = field_name
            return self

        def _execute_sql(self):
            if self._distinct_field != "":
                select_part = 'distinct(%s)' % self._distinct_field
            else:
                select_part = ','.join(self._t_attrs)
            sql_str = "select %s from %s" % (select_part, self._t_name)
            if self._filters != "":
                sql_str += " where %s" % self._filters
            if self._offset != "":
                assert self._limit != ""
                sql_str += " limit %s, %s" % (self._limit, self._offset)
            elif self._limit != "":
                sql_str += " limit %s" % self._limit
            _LOGGER.debug("%s : %s" %
                          (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           sql_str))

            self.__data.clear()
            self.__data = deque(self._db.hiveExecute(sql_str))

        def next(self):
            """Returns the next element."""
            if not len(self.__data):
                raise StopIteration
            if self._distinct_field != "":
                data = self.__data.popleft()
            else:
                data = dict(
                    zip(self._t_attrs, self.__data.popleft().split('\t')))
            return data

        def __iter__(self):
            """Returns the iterator itself."""
            self._execute_sql()
            return self

    def __new__(self, name, bases, attrs):
        model_id = attrs.pop('__modelid__', None)
        if not model_id or not MODEL_CONF.get(model_id):
            _LOGGER.warn('MetaHive:modelid in model %s invalid!' % name)
            return

        db_type = MODEL_CONF[model_id]['db_type']
        mapped_db = MODEL_CONF[model_id]['mapped_db']
        if db_type == 'hive':
            hive_query = MetaHive.__HiveQuery(mapped_db,
                                              attrs.pop('__t_name__', None),
                                              attrs.pop('__t_colunms__', None))
            attrs['query'] = hive_query
        else:
            raise Exception('db type %s Not Support by HiveBase!' % db_type)

        new_class = type.__new__(self, name, bases, attrs)
        _register_model(new_class, model_id)
        return new_class
