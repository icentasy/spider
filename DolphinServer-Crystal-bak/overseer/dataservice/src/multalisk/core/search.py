# -*- coding:utf-8 -*-
"""
    multalisk.core.search
    ~~~~~~~~~~~~~~~~~~~~~

    Provide :function:`search` to get the query object for different databse
    for SQL-ORM, query object will be <class 'armory.tank.mysql.ShardedQuery'>
    for mongo, query object will be <class 'pymongo.cursor.Cursor'>

    :class:`SearchParams` used for packaging query string
    :class:`QueryBuilder` used for building query from query string

    For query string, most operators to SQL/mongo are available.

"""
import inspect

from sqlalchemy import and_ as AND
from sqlalchemy import or_ as OR
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm.attributes import InstrumentedAttribute

from multalisk.core.sql_helper import get_related_association_proxy_model
from multalisk.utils.exception import ParamError
from multalisk.utils.custom_filter import get_filter_value


def _valid_orm_field(model, fieldname, relation):
    try:
        getattr(model, relation or fieldname)
    except AttributeError:
        # TODO what to do here?
        return False

    return True


def _valid_mongo_field(model, fieldname):
    """check validation of the field in mongo model
    NOT IMPLEMENT
    """
    return True


def _valid_sql_field(model, fieldname):
    """check validation of the field in sql model
    NOT IMPLEMENT
    """
    return True


def _sub_operator(model, argument, fieldname):
    """This function is for use with the ``has`` and ``any`` search operations.

    """
    if isinstance(model, InstrumentedAttribute):
        submodel = model.property.mapper.class_
    elif isinstance(model, AssociationProxy):
        submodel = get_related_association_proxy_model(model)
    else:  # TODO what to do here?
        pass

    # Support legacy has/any with implicit eq operator
    return getattr(submodel, fieldname) == argument


def _escape_regex(raw_string):
    """This function is for use to escape mongodb regex string
    """
    _KEY_CHARS = '\\.*+-?[]()'
    for key in _KEY_CHARS:
        raw_string = raw_string.replace(key, '\\' + key)

    return raw_string


SQL_OPERATORS = {
    # Operators which accept a single argument.
    'is_null': lambda f: f is None,
    'is_not_null': lambda f: f is not None,
    # TODO what are these?
    'desc': lambda f: f.desc,
    'asc': lambda f: f.asc,
    # Operators which accept two arguments.
    '==': lambda f, a: f == a,
    'eq': lambda f, a: f == a,
    'equals': lambda f, a: f == a,
    'equal_to': lambda f, a: f == a,
    '!=': lambda f, a: f != a,
    'ne': lambda f, a: f != a,
    'neq': lambda f, a: f != a,
    'not_equal_to': lambda f, a: f != a,
    'does_not_equal': lambda f, a: f != a,
    '>': lambda f, a: f > a,
    'gt': lambda f, a: f > a,
    '<': lambda f, a: f < a,
    'lt': lambda f, a: f < a,
    '>=': lambda f, a: f >= a,
    'ge': lambda f, a: f >= a,
    'gte': lambda f, a: f >= a,
    'geq': lambda f, a: f >= a,
    '<=': lambda f, a: f <= a,
    'le': lambda f, a: f <= a,
    'lte': lambda f, a: f <= a,
    'leq': lambda f, a: f <= a,
    'ilike': lambda f, a: f.ilike(a),
    'like': lambda f, a: f.like(a),
    'in': lambda f, a: f.in_(a),
    'not_in': lambda f, a: ~f.in_(a),
    # Operators which accept three arguments.
    'has': lambda f, a, fn: f.has(_sub_operator(f, a, fn)),
    'any': lambda f, a, fn: f.any(_sub_operator(f, a, fn)),
}


MONGO_OPERATORS = {
    '==': lambda f, a: {f: a},
    'eq': lambda f, a: {f: a},
    'equals': lambda f, a: {f: a},
    'equal_to': lambda f, a: {f: a},
    '!=': lambda f, a: {f: {'$ne': a}},
    'ne': lambda f, a: {f: {'$ne': a}},
    'neq': lambda f, a: {f: {'$ne': a}},
    'not_equal_to': lambda f, a: {f: {'$ne': a}},
    'does_not_equal': lambda f, a: {f: {'$ne': a}},
    '>': lambda f, a: {f: {'$gt': a}},
    'gt': lambda f, a: {f: {'$gt': a}},
    '<': lambda f, a: {f: {'$lt': a}},
    'lt': lambda f, a: {f: {'$lt': a}},
    '>=': lambda f, a: {f: {'$gte': a}},
    'ge': lambda f, a: {f: {'$gte': a}},
    'gte': lambda f, a: {f: {'$gte': a}},
    'geq': lambda f, a: {f: {'$gte': a}},
    '<=': lambda f, a: {f: {'$lte': a}},
    'le': lambda f, a: {f: {'$lte': a}},
    'lte': lambda f, a: {f: {'$lte': a}},
    'leq': lambda f, a: {f: {'$lte': a}},
    'like': lambda f, a: {f: {'$regex': _escape_regex(a)}},
    'in': lambda f, a: {f: {'$in': a.split(',')}},
    'not_in': lambda f, a: {f: {'$nin': a.split(',')}},
}


HIVE_OPERATORS = {
    '==': lambda f, a: "%s %s %s" % (f, "=", a),
    'eq': lambda f, a: "%s %s %s" % (f, "=", a),
    'equals': lambda f, a: "%s %s %s" % (f, "=", a),
    'equal_to': lambda f, a: "%s %s %s" % (f, "=", a),
    '!=': lambda f, a: "%s %s %s" % (f, "!=", a),
    'ne': lambda f, a: "%s %s %s" % (f, "!=", a),
    'neq': lambda f, a: "%s %s %s" % (f, "!=", a),
    'not_equal_to': lambda f, a: "%s %s %s" % (f, "!=", a),
    'does_not_equal': lambda f, a: "%s %s %s" % (f, "!=", a),
    '>': lambda f, a: "%s %s %s" % (f, ">", a),
    'gt': lambda f, a: "%s %s %s" % (f, ">", a),
    '<': lambda f, a: "%s %s %s" % (f, "<", a),
    'lt': lambda f, a: "%s %s %s" % (f, "<", a),
    '>=': lambda f, a: "%s %s %s" % (f, ">=", a),
    'ge': lambda f, a: "%s %s %s" % (f, ">=", a),
    'gte': lambda f, a: "%s %s %s" % (f, ">=", a),
    'geq': lambda f, a: "%s %s %s" % (f, ">=", a),
    '<=': lambda f, a: "%s %s %s" % (f, "<=", a),
    'le': lambda f, a: "%s %s %s" % (f, "<=", a),
    'lte': lambda f, a: "%s %s %s" % (f, "<=", a),
    'leq': lambda f, a: "%s %s %s" % (f, "<=", a),
    'like': lambda f, a: "%s %s %s" % (f, "like", "'%" + a.strip("'") + "%'"),
}


class OrderBy(object):
    """Represents an "order by" in a SQL query expression."""

    def __init__(self, field, direction='asc'):
        """Instantiates this object with the specified attributes.

        `field` is the name of the field by which to order the result set.

        `direction` is either ``'asc'`` or ``'desc'``, for "ascending" and
        "descending", respectively.

        """
        self.field = field
        self.direction = direction

    def __repr__(self):
        """Returns a string representation of this object."""
        return '<OrderBy {0}, {1}>'.format(self.field, self.direction)


class GroupBy(object):
    """Represents a "group by" in a SQL query expression."""

    def __init__(self, field):
        """Instantiates this object with the specified attributes.

        `field` is the name of the field by which to group the result set.

        """
        self.field = field

    def __repr__(self):
        """Returns a string representation of this object."""
        return '<GroupBy {0}>'.format(self.field)


class Filter(object):

    """Aggregates a filter to apply to a SQL query.
    """

    def __init__(self, fieldname, operator, argument=None, otherfield=None):
        """Instantiates this object with the specified attributes.
        """
        self.fieldname = fieldname
        self.operator = operator
        self.argument = argument
        self.otherfield = otherfield

    def __repr__(self):
        """Returns a string representation of this object."""
        return '<Filter {0} {1} {2}>'.format(self.fieldname, self.operator,
                                             self.argument or self.otherfield)

    @staticmethod
    def from_dictionary(dictionary):
        """Returns a new :class:`Filter` object with arguments parsed from
        `dictionary`.

        `dictionary` is a dictionary of the form::

            {'name': 'age', 'op': 'lt', 'val': 20}

        or::

            {'name': 'age', 'op': 'lt', 'field': height}

        """
        fieldname = dictionary.get('name')
        operator = dictionary.get('op')
        argument = get_filter_value(dictionary.get('val'))
        otherfield = dictionary.get('field')
        return Filter(fieldname, operator, argument, otherfield)


class SearchParams(object):

    """Aggregates the parameters for a search
    """

    def __init__(self, filters=None, limit=None, offset=None, order_by=None,
                 group_by=None, junction=None):
        self.filters = filters or []
        self.limit = limit
        self.offset = offset
        self.order_by = order_by or []
        self.group_by = group_by or []
        self.junction = junction

    @staticmethod
    def from_dictionary(dictionary):
        """Create a new SearchParams object with arguments parsed from
        `dictionary`.

        `dictionary` form:
            {
                'filters': [{'name': 'date', 'op': '>', 'val': 20150122}, ...],
                'limit': 10,
                'offset': 0,
                'disjunction': True
            }
        """
        from_dict = Filter.from_dictionary
        filters = [from_dict(f) for f in dictionary.get('filters', [])]
        limit = dictionary.get('limit')
        offset = dictionary.get('offset')
        order_by_list = dictionary.get('order_by', [])
        order_by = [OrderBy(**o) for o in order_by_list]
        group_by_list = dictionary.get('group_by', [])
        group_by = [GroupBy(**o) for o in group_by_list]
        disjunction = dictionary.get('disjunction')
        junction = not disjunction
        return SearchParams(filters=filters, limit=limit, offset=offset,
                            order_by=order_by, group_by=group_by,
                            junction=junction)


class QueryBuilder(object):

    """Build query object for search
    for sql, query type is <class 'armory.tank.mysql.ShardedQuery'>
    for mongo, query type is <class 'pymongo.cursor.Cursor'>
    """
    @staticmethod
    def _create_sql_operation(model, fieldname, operator, argument,
                              relation=None):
        # raises KeyError if operator not in SQL_OPERATORS
        opfunc = SQL_OPERATORS[operator]
        argspec = inspect.getargspec(opfunc)
        numargs = len(argspec.args)
        # raises AttributeError if `fieldname` or `relation` does not exist
        field = getattr(model, relation or fieldname)
        # each of these will raise a TypeError if the wrong number of argments
        # is supplied to `opfunc`.
        if numargs == 1:
            return opfunc(field)
        if argument is None:
            msg = ('To compare a value to NULL, use the is_null/is_not_null '
                   'operators.')
            raise ParamError(msg)
        if numargs == 2:
            return opfunc(field, argument)
        return opfunc(field, argument, fieldname)

    @staticmethod
    def _create_mongo_operation(fieldname, operator, argument):
        """create mongo query condition
           -fieldname: `created`
           -operator: `>`
           -argument: `0`
           ==> cond={'created': {'$gt': 0}}
        """
        # raises KeyError if operator not in MONGO_OPERATORS
        opfunc = MONGO_OPERATORS[operator]
        argspec = inspect.getargspec(opfunc)
        numargs = len(argspec.args)
        if numargs == 1:
            return opfunc(fieldname)
        if argument is None:
            msg = ('To compare a value to NULL, use the is_null/is_not_null '
                   'operators.')
            raise ParamError(msg)
        return opfunc(fieldname, argument)

    @staticmethod
    def _create_hive_operation(fieldname, operator, argument):
        opfunc = HIVE_OPERATORS[operator]
        argspec = inspect.getargspec(opfunc)
        numargs = len(argspec.args)
        if numargs == 1:
            return opfunc(fieldname)
        if argument is None:
            msg = ('To compare a value to NULL, use the is_null/is_not_null '
                   'operators.')
            raise TypeError(msg)
        return opfunc(fieldname, argument)

    @staticmethod
    def _create_sql_filters(model, search_params):
        filters = []
        for filt in search_params.filters:
            fname = filt.fieldname
            val = filt.argument
            # get the relationship from the field name, if it exists
            # in this case, `operator` must be has or any
            relation = None
            if '__' in fname:
                relation, fname = fname.split('__')
            # inspect whether the field exists in model
            # i'll implement this later...
            if not _valid_orm_field(model, fname, relation):
                continue
            # get the other field to which to compare, if it exists
            if filt.otherfield:
                val = getattr(model, filt.otherfield)
            create_op = QueryBuilder._create_sql_operation
            param = create_op(model, fname, filt.operator, val, relation)
            filters.append(param)
        return filters

    @staticmethod
    def _create_mongo_filters(model, search_params):
        filters = []
        for filt in search_params.filters:
            fname = filt.fieldname
            val = filt.argument
            # inspect whether the field exists in model
            # i'll implement this later...
            if not _valid_mongo_field(model, fname):
                continue
            create_op = QueryBuilder._create_mongo_operation
            param = create_op(fname, filt.operator, val)
            filters.append(param)
        return filters

    @staticmethod
    def _create_raw_query_str(model, search_params):
        filters = []
        for filt in search_params.filters:
            fname = filt.fieldname
            val = filt.argument
            if '__' in fname:
                msg = ('hive raw sql string Not Support'
                       'relation ship query now!')
                raise Exception(msg)
            # inspect whether the field exists in model
            # i'll implement this later...
            if not _valid_sql_field(model, fname):
                continue
            # get the other field to which to compare, if it exists
            if filt.otherfield:
                val = filt.otherfield
            else:
                # escape to string
                val = "'%s'" % filt.argument
            create_op = QueryBuilder._create_hive_operation
            param = create_op(fname, filt.operator, val)
            filters.append(param)

        return filters

    @staticmethod
    def create_query(db_type, model, search_params,
                     distinct=False, field_name=None, mapped_db=None):
        query = model.query
        if db_type.endswith('sql'):
            if distinct:
                query = mapped_db.session.query(getattr(model, field_name))
            filters = QueryBuilder._create_sql_filters(model, search_params)
            if len(filters) > 0:
                junction = AND if search_params.junction else OR
                query = query.filter(junction(*filters))

            # order the search
            if search_params.order_by:
                for val in search_params.order_by:
                    field = getattr(model, val.field)
                    direction = getattr(field, val.direction)
                    query = query.order_by(direction())

            # group the query
            if search_params.group_by:
                for groupby in search_params.group_by:
                    field = getattr(model, groupby.field)
                    query = query.group_by(field)

            # Limit it
            if search_params.limit:
                query = query.limit(search_params.limit)
            if search_params.offset:
                query = query.offset(search_params.offset)
            if distinct:
                query = query.distinct()
        elif db_type.endswith('mongo'):
            filters = QueryBuilder._create_mongo_filters(model, search_params)
            cond = {}
            if len(filters) > 0:
                op = '$and' if search_params.junction else '$or'
                cond.update({op: filters})
            query = query.find(cond)
            if search_params.offset:
                query = query.skip(search_params.offset)
            if search_params.limit:
                query = query.limit(search_params.limit)
            if distinct:
                query = query.distinct(field_name)
        elif db_type.endswith('hive'):
            filters = QueryBuilder._create_raw_query_str(model, search_params)
            filter_str = ""
            if len(filters) > 0:
                junction_str = 'and' if search_params.junction else 'or'
                tmp_str = ""
                i = 0
                for filter in filters:
                    if i > 0:
                        tmp_str += " %s " % junction_str
                    tmp_str += filter
                    i += 1
                filter_str = tmp_str
            query = query.filter(filter_str)
            if search_params.limit:
                query = query.limit(search_params.limit)
                # check `offset` only if `limit` was assigned
                if search_params.offset:
                    query = query.offset(search_params.offset)
            if distinct:
                query = query.distinct(field_name)

        return query


def search(db_type, model, search_params):
    """This function used for create query object by query string
    """
    if isinstance(search_params, dict):
        search_params = SearchParams.from_dictionary(search_params)
    query = QueryBuilder.create_query(db_type, model, search_params)
    return query


def distinct_field(db_type, mapped_db, model, field_name, search_params={}):
    """This function used for query distinct field by query string
    """
    if isinstance(search_params, dict):
        search_params = SearchParams.from_dictionary(search_params)
    query = QueryBuilder.create_query(db_type, model, search_params,
                                      distinct=True, field_name=field_name,
                                      mapped_db=mapped_db)
    return query
