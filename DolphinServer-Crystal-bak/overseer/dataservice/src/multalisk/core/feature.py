# -*- coding:utf-8 -*-
"""
    multalisk.core.feature
    ~~~~~~~~~~~~~~~~~~~~~~

    Provide function to create report feature.

    One x dimension with multiple y dimension feature is supported,
    and multiple aggregate function are available to create complex feature.

"""
import re
import logging

from multalisk.utils.exception import ParamError

_LOGGER = logging.getLogger(__name__)


_REGEX_FIELD_OPERATOR = '\+|-|\*|/'


def _inspect_x(x_dimension, record_list):
    """This function used for inspecting
    whether the target record has `x_dimension` field then
    get the `available_list` return
    """
    available_list = []
    for record in record_list:
        if x_dimension not in record:
            msg = 'x dimension `%s` not in query object!' % x_dimension
            _LOGGER.warn(msg)
            continue
        available_list.append(record)

    return available_list


def _get_target_field_val(_rec, y_dimension):
    if not y_dimension.target_field_group:
        res_val = _rec.get(y_dimension.target_field)
    else:
        # multiple field operation
        group_field = y_dimension.target_field_group
        for field in re.split(_REGEX_FIELD_OPERATOR, group_field):
            field_val = _rec.get(field)
            group_field = group_field.replace(field, str(field_val))
        try:
            res_val = eval('float(1)*' + group_field)
        except Exception as e:
            print 'exception(%s) when eval %s' % (e, group_field)
            res_val = 0

    return res_val


def _operator_no_func(x_dimension, y_dimension, query_list):
    """no aggregate function operator
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: `y_dimension.target_field`
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: `y_dimension.target_field`
            }
            ...
        }
    """
    feature_dict = {}
    for _rec in query_list:
        x_field = feature_dict.setdefault(_rec.get(x_dimension), {})
        field_val = _get_target_field_val(_rec, y_dimension)
        x_field[y_dimension.feature_name] = field_val

    return feature_dict


def _operator_sum(x_dimension, y_dimension, query_list):
    """sum aggregation of `y_dimension.target_field` group by `x_dimension`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
        }
    """
    feature_dict = {}
    for _rec in query_list:
        x_field = feature_dict.setdefault(_rec.get(x_dimension), {})
        x_field.setdefault(y_dimension.feature_name, 0)
        field_val = _get_target_field_val(_rec, y_dimension)
        x_field[y_dimension.feature_name] += float(field_val)

    return feature_dict


def _operator_sum_groupby(x_dimension, y_dimension, query_list):
    """sum aggregation of `y_dimension.target_field`
    multiple group by `x_dimension` and `y_dimension.groupby`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: {
                    'group01': sum(`y_dimension.target_field`),
                    'group02': sum(`y_dimension.target_field`)
                 }
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: {
                    'group01': sum(`y_dimension.target_field`),
                    'group02': sum(`y_dimension.target_field`)
                }
            }
        }
    """
    feature_dict = {}
    for _rec in query_list:
        if len(y_dimension.groupby) > 1:
            group_key = '_'.join([unicode(_rec.get(i))
                                  for i in y_dimension.groupby])
        else:
            # just for performance when only one groupby field
            # using join here will cost more than 0.01s per 10000 record
            group_key = _rec.get(y_dimension.groupby[0])

        f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})\
            .setdefault(y_dimension.feature_name, {})
        f_dict.setdefault(group_key, 0)
        field_val = _get_target_field_val(_rec, y_dimension)
        f_dict[group_key] += float(field_val)

    return feature_dict


def _operator_multi_sum(x_dimension, y_dimension, query_list):
    """multiple column operation
    1. sum aggregation of each column group by `x_dimension`
    2. multiple column operation(+-*/)
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
        }
    """
    # multiple field operation
    group_field = y_dimension.target_field_group
    if group_field is None:
        raise ParamError('`target_field_group` not found!')

    feature_list = {}
    field_list = re.split(_REGEX_FIELD_OPERATOR, group_field)
    for field in field_list:
        # get the sum result for each field
        feature_dict = {}
        for _rec in query_list:
            feature_dict.setdefault(_rec.get(x_dimension), 0)
            field_val = _rec.get(field)
            feature_dict[_rec.get(x_dimension)] += field_val

        feature_list.update({field: feature_dict})

    res_dict = feature_list[field_list[0]]
    feature_dict = dict(res_dict)
    for x_key in res_dict.keys():
        tmp_field = group_field
        for field in re.split(_REGEX_FIELD_OPERATOR, tmp_field):
            sum_field = feature_list.get(field).get(x_key)
            tmp_field = tmp_field.replace(field, str(sum_field))
        try:
            res_val = eval('float(1)*' + tmp_field)
        except Exception as e:
            print 'exception(%s) when eval %s' % (e, tmp_field)
            res_val = None
        feature_dict.update({x_key: {y_dimension.feature_name: res_val}})

    return feature_dict


def _operator_multi_sum_ratio(x_dimension, y_dimension, query_list):
    """multiple column operation
    1. sum aggregation of each column group by `x_dimension`
    2. multiple column operation(+-*/)
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
        }
    """
    # multiple field operation
    group_field = y_dimension.target_field_group
    if group_field is None:
        raise ParamError('`target_field_group` not found!')

    feature_list = {}
    field_list = re.split(_REGEX_FIELD_OPERATOR, group_field)
    for field in field_list:
        # get the sum result for each field
        feature_dict = {}
        for _rec in query_list:
            feature_dict.setdefault(_rec.get(x_dimension), 0)
            field_val = _rec.get(field)
            feature_dict[_rec.get(x_dimension)] += field_val

        feature_list.update({field: feature_dict})

    res_dict = feature_list[field_list[0]]
    feature_dict = dict(res_dict)
    tmp_dict = {}  # used for stored temp data for ratio calc
    assit_sum = 0
    for x_key in res_dict.keys():
        tmp_field = group_field
        for field in re.split(_REGEX_FIELD_OPERATOR, tmp_field):
            sum_field = feature_list.get(field).get(x_key)
            tmp_field = tmp_field.replace(field, str(sum_field))
        try:
            res_val = eval('float(1)*' + tmp_field)
            assit_sum += res_val
            assit_dict_y = tmp_dict.setdefault(x_key, {'sum': 0})
            assit_dict_y['sum'] += res_val
        except Exception as e:
            print 'exception(%s) when eval %s' % (e, tmp_field)
            res_val = None

        if res_val is None or assit_sum == 0:
            continue

        feature_dict.update({
            x_key: {
                y_dimension.feature_name: (float(res_val) / assit_sum)
            }
        })

        # update others' sum ratio
        for k, v in feature_dict.items():
            if k != x_key:
                if k not in tmp_dict:
                    continue
                feature_dict.update(
                    {k: {y_dimension.feature_name:
                         float(tmp_dict[k]['sum']) / assit_sum
                         }})

    return feature_dict


def _operator_multi_sum_groupby(x_dimension, y_dimension, query_list):
    """multiple column operation
    1. sum aggregation of each column group by
       `x_dimension` and `y_dimension.groupby`
    2. multiple column operation(+-*/)
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
        }
    """
    # multiple field operation
    group_field = y_dimension.target_field_group
    if group_field is None:
        raise ParamError('`target_field_group` not found!')

    feature_list = {}
    field_list = re.split(_REGEX_FIELD_OPERATOR, group_field)
    for field in field_list:
        # get the sum result for each field
        feature_dict = {}
        for _rec in query_list:
            if len(y_dimension.groupby) > 1:
                group_key = '_'.join([unicode(_rec.get(i))
                                      for i in y_dimension.groupby])
            else:
                group_key = _rec.get(y_dimension.groupby[0])

                f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})
                f_dict.setdefault(group_key, 0)
                field_val = _rec.get(field)
                f_dict[group_key] += field_val

        feature_list.update({field: feature_dict})

    res_dict = feature_list[field_list[0]]
    feature_dict = dict(res_dict)
    for x_key in res_dict.keys():
        f_dict = {}
        for k in res_dict.get(x_key):
            tmp_field = group_field
            for field in re.split(_REGEX_FIELD_OPERATOR, tmp_field):
                sum_field = feature_list.get(field).get(x_key).get(k)
                tmp_field = tmp_field.replace(field, str(sum_field))
            try:
                res_val = eval('float(1)*' + tmp_field)
            except Exception as e:
                print 'exception(%s) when eval %s' % (e, tmp_field)
                res_val = None

            f_dict.update({k: res_val})
        feature_dict.update({x_key: {y_dimension.feature_name: f_dict}})

    return feature_dict


def _operator_multi_sum_groupby_ratio(x_dimension, y_dimension, query_list):
    """multiple column operation
    1. sum aggregation of each column group by
       `x_dimension` and `y_dimension.groupby`
    2. multiple column operation(+-*/)
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: sum(`y_dimension.target_field`)
        }
    """
    # multiple field operation
    group_field = y_dimension.target_field_group
    if group_field is None:
        raise ParamError('`target_field_group` not found!')

    feature_list = {}
    field_list = re.split(_REGEX_FIELD_OPERATOR, group_field)
    for field in field_list:
        # get the sum result for each field
        feature_dict = {}
        for _rec in query_list:
            if len(y_dimension.groupby) > 1:
                group_key = '_'.join([unicode(_rec.get(i))
                                      for i in y_dimension.groupby])
            else:
                group_key = _rec.get(y_dimension.groupby[0])

                f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})
                f_dict.setdefault(group_key, 0)
                field_val = _rec.get(field)
                f_dict[group_key] += field_val

        feature_list.update({field: feature_dict})

    res_dict = feature_list[field_list[0]]
    feature_dict = dict(res_dict)
    tmp_dict = {}  # used for stored temp data for ratio calc
    for x_key in res_dict.keys():
        f_dict = {}
        for k in res_dict.get(x_key):
            tmp_field = group_field
            for field in re.split(_REGEX_FIELD_OPERATOR, tmp_field):
                sum_field = feature_list.get(field).get(x_key).get(k)
                tmp_field = tmp_field.replace(field, str(sum_field))
            try:
                res_val = eval('float(1)*' + tmp_field)
                # for calculate ratio
                key_word_x = x_key
                assit_dict_x = tmp_dict.setdefault(key_word_x, {'sum': 0})
                assit_dict_x['sum'] += res_val
                key_word_y = '_'.join([unicode(x_key), unicode(k)])
                assit_dict_y = tmp_dict.setdefault(key_word_y, {'sum': 0})
                assit_dict_y['sum'] += res_val
            except Exception as e:
                print 'exception(%s) when eval %s' % (e, tmp_field)
                res_val = None

            if res_val is None or assit_dict_x['sum'] == 0:
                continue

            f_dict.update({k: float(res_val) / assit_dict_x['sum']})
            # update others's ratio
            for g in f_dict:
                if g != k:
                    other_key = '_'.join([unicode(x_key), unicode(g)])
                    f_dict[g] = (float(tmp_dict[other_key]['sum']) /
                                 assit_dict_x['sum'])
        feature_dict.update({x_key: {y_dimension.feature_name: f_dict}})

    return feature_dict


def _operator_avg(x_dimension, y_dimension, query_list):
    """average aggregation of `y_dimension.target_field`
    group by `x_dimension`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: avg(`y_dimension.target_field`)
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: avg(`y_dimension.target_field`)
            }
        }
    """
    feature_dict = {}
    tmp_dict = {}
    for _rec in query_list:
        key_word = _rec.get(x_dimension)
        assit_dict = tmp_dict.setdefault(key_word, {'sum': 0, 'count': 0})
        field_val = _get_target_field_val(_rec, y_dimension)
        assit_dict['sum'] += float(field_val)
        assit_dict['count'] += 1

        x_field = feature_dict.setdefault(_rec.get(x_dimension), {})
        x_field.setdefault(y_dimension.feature_name, 0)
        x_field[y_dimension.feature_name] = (float(assit_dict['sum']) /
                                             assit_dict['count'])

    return feature_dict


def _operator_avg_groupby(x_dimension, y_dimension, query_list):
    """average aggregation of `y_dimension.target_field`
    multiple group by `x_dimension` and `y_dimension.groupby`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: {
                    'group01': avg(`y_dimension.target_field`),
                    'group02': avg(`y_dimension.target_field`)
                 }
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: {
                    'group01': avg(`y_dimension.target_field`),
                    'group02': avg(`y_dimension.target_field`)
                }
            }
        }
    """
    feature_dict = {}
    tmp_dict = {}
    for _rec in query_list:
        # here we trades space for time,
        # assist_dict is used for store `sum` and `count`
        key_word = '_'.join([unicode(_rec.get(i))
                             for i in [x_dimension] + y_dimension.groupby])
        assit_dict = tmp_dict.setdefault(key_word, {'sum': 0, 'count': 0})
        field_val = _get_target_field_val(_rec, y_dimension)
        assit_dict['sum'] += float(field_val)
        assit_dict['count'] += 1

        group_key = '_'.join([unicode(_rec.get(i))
                              for i in y_dimension.groupby])
        f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})\
            .setdefault(y_dimension.feature_name, {})
        f_dict.setdefault(group_key, 0)
        f_dict[group_key] = float(assit_dict['sum']) / assit_dict['count']

    return feature_dict


def _operator_sum_ratio(x_dimension, y_dimension, query_list):
    """sum ratio aggregation operation of `y_dimension.target_field`
    group by `x_dimension`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: {
                    'group01': sum_ratio(`y_dimension.target_field`),
                    'group02': sum_ratio(`y_dimension.target_field`)
                 }
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: {
                    'group01': sum_ratio(`y_dimension.target_field`),
                    'group02': sum_ratio(`y_dimension.target_field`)
                }
            }
        }
    """
    feature_dict = {}
    tmp_dict = {}  # used for stored temp data for ratio calc
    assit_sum = 0
    for _rec in query_list:
        field_val = _get_target_field_val(_rec, y_dimension)
        assit_sum += float(field_val)
        assit_dict_y = tmp_dict.setdefault(_rec.get(x_dimension), {'sum': 0})
        assit_dict_y['sum'] += field_val

        # group_key = '_'.join([unicode(_rec.get(i))
        #                       for i in y_dimension.groupby])
        f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})
        f_dict.setdefault(y_dimension.feature_name, 0)

        if assit_sum == 0:
            continue

        f_dict[y_dimension.feature_name] = float(
            assit_dict_y['sum']) / assit_sum

        # update others' sum ratio
        for k, v in feature_dict.items():
            if k != _rec.get(x_dimension):
                feature_dict[k][y_dimension.feature_name] = float(
                    tmp_dict[k]['sum']) / assit_sum

    return feature_dict


def _operator_sum_groupby_ratio(x_dimension, y_dimension, query_list):
    """sum ratio aggregation operation of `y_dimension.target_field`
    multiple group by `x_dimension` and `y_dimension.groupby`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: {
                    'group01': sum_ratio(`y_dimension.target_field`),
                    'group02': sum_ratio(`y_dimension.target_field`)
                 }
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: {
                    'group01': sum_ratio(`y_dimension.target_field`),
                    'group02': sum_ratio(`y_dimension.target_field`)
                }
            }
        }
    """
    feature_dict = {}
    tmp_dict = {}  # used for stored temp data for ratio calc
    for _rec in query_list:
        key_word_x = _rec.get(x_dimension)
        assit_dict_x = tmp_dict.setdefault(key_word_x, {'sum': 0})
        field_val = _get_target_field_val(_rec, y_dimension)
        assit_dict_x['sum'] += float(field_val)
        key_word_y = '_'.join([unicode(_rec.get(i))
                               for i in [x_dimension] + y_dimension.groupby])
        assit_dict_y = tmp_dict.setdefault(key_word_y, {'sum': 0})
        assit_dict_y['sum'] += field_val

        group_key = '_'.join([unicode(_rec.get(i))
                              for i in y_dimension.groupby])
        f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})\
                             .setdefault(y_dimension.feature_name, {})
        f_dict[group_key] = float(assit_dict_y['sum']) / assit_dict_x['sum']
        # update others' sum ratio
        for k, v in f_dict.items():
            if k != group_key:
                other_key = '_'.join([unicode(_rec.get(x_dimension)), k])
                f_dict[k] = (float(tmp_dict[other_key]['sum']) /
                             assit_dict_x['sum'])

    return feature_dict


def _operator_count_ratio(x_dimension, y_dimension, query_list):
    """count ratio aggregation operation of row
    multiple group by `x_dimension`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: {
                    'group01': count_ratio(*),
                    'group02': count_ratio(*)
                 }
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: {
                    'group01': count_ratio(*),
                    'group02': count_ratio(*)
                }
            }
        }
    """
    feature_dict = {}
    tmp_dict = {}  # used for stored temp data for ratio calc
    assit_count = 0
    for _rec in query_list:
        assit_count += 1
        assit_dict_y = tmp_dict.setdefault(_rec.get(x_dimension), {'count': 0})
        assit_dict_y['count'] += 1

        # group_key = '_'.join([unicode(_rec.get(i))
        #                       for i in y_dimension.groupby])
        f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})
        f_dict.setdefault(y_dimension.feature_name, 0)
        f_dict[y_dimension.feature_name] = (float(assit_dict_y['count']) /
                                            assit_count)

        # update others' count ratio
        for k, v in f_dict.items():
            if k != _rec.get(x_dimension):
                feature_dict[k][y_dimension.feature_name] = float(
                    tmp_dict[k]['count']) / assit_count

    return feature_dict


def _operator_count_groupby_ratio(x_dimension, y_dimension, query_list):
    """count ratio aggregation operation of row
    multiple group by `x_dimension` and `y_dimension.groupby`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: {
                    'group01': count_ratio(*),
                    'group02': count_ratio(*)
                 }
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: {
                    'group01': count_ratio(*),
                    'group02': count_ratio(*)
                }
            }
        }
    """
    feature_dict = {}
    tmp_dict = {}  # used for stored temp data for ratio calc
    for _rec in query_list:
        key_word_x = _rec.get(x_dimension)
        assit_dict_x = tmp_dict.setdefault(key_word_x, {'count': 0})
        assit_dict_x['count'] += 1
        key_word_y = '_'.join([unicode(_rec.get(i))
                               for i in [x_dimension] + y_dimension.groupby])
        assit_dict_y = tmp_dict.setdefault(key_word_y, {'count': 0})
        assit_dict_y['count'] += 1

        group_key = '_'.join([unicode(_rec.get(i))
                              for i in y_dimension.groupby])
        f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})\
                             .setdefault(y_dimension.feature_name, {})
        f_dict[group_key] = (float(assit_dict_y['count']) /
                             assit_dict_x['count'])
        # update others' count ratio
        for k, v in f_dict.items():
            if k != group_key:
                other_key = '_'.join([unicode(_rec.get(x_dimension)), k])
                f_dict[k] = (float(tmp_dict[other_key]['count']) /
                             assit_dict_x['count'])

    return feature_dict


def _operator_count(x_dimension, y_dimension, query_list):
    """count aggregation of row group by `x_dimension`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: count(*)
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: count(*)
            }
        }
    """
    feature_dict = {}
    for _rec in query_list:
        x_field = feature_dict.setdefault(_rec.get(x_dimension), {})
        x_field.setdefault(y_dimension.feature_name, 0)
        x_field[y_dimension.feature_name] += 1

    return feature_dict


def _operator_count_groupby(x_dimension, y_dimension, query_list):
    """count aggregation operation
    multiple group by `x_dimension` and `y_dimension.groupby`
    OUTPUT:
        {
            `x_dimension01`: {
                `y_dimension.feature_name`: {
                    'group01': count(*),
                    'group02': count(*)
                 }
            },
            `x_dimension02`: {
                `y_dimension.feature_name`: {
                    'group01': count(*),
                    'group02': count(*)
                }
            }
        }
    """
    feature_dict = {}
    for _rec in query_list:
        group_key = '_'.join([unicode(_rec.get(i))
                              for i in y_dimension.groupby])
        f_dict = feature_dict.setdefault(_rec.get(x_dimension), {})\
            .setdefault(y_dimension.feature_name, {})
        f_dict.setdefault(group_key, 0)
        f_dict[group_key] += 1

    return feature_dict


_AVAILABLE_FUNC = {
    'sum': _operator_sum,
    'sum_ratio': _operator_sum_ratio,
    'sum_groupby': _operator_sum_groupby,
    'sum_groupby_ratio': _operator_sum_groupby_ratio,
    'multi_sum': _operator_multi_sum,
    'multi_sum_ratio': _operator_multi_sum_ratio,
    'multi_sum_groupby': _operator_multi_sum_groupby,
    'multi_sum_groupby_ratio': _operator_multi_sum_groupby_ratio,
    'avg': _operator_avg,
    'avg_groupby': _operator_avg_groupby,
    'count': _operator_count,
    'count_ratio': _operator_count_ratio,
    'count_groupby': _operator_count_groupby,
    'count_groupby_ratio': _operator_count_groupby_ratio,
    'no_func': _operator_no_func
}


class Y_DimensionBuilder(object):

    """Aggregates the y dimension description
    """

    def __init__(self, feature_name, target_field,
                 target_field_group, func, groupby):
        self.feature_name = feature_name
        self.target_field = target_field
        self.target_field_group = target_field_group
        self.func = func
        self.groupby = groupby if isinstance(groupby, list) else [groupby]

    @staticmethod
    def from_dictionary(y_dimension):
        """Create a new y dimension object with argument parsed from
        `y_dimension`

        `y_dimension` form:
            {
                'name': 'click_count',
                'value':{
                    'field': 'click',
                    'func': 'sum'
                }
            }
        """
        feature_name = y_dimension.get('name')
        feature_value = y_dimension.get('value')
        target_field = feature_value.get('field')
        # the target field may be multiple fields
        # eg: target_field_group = 'field1/field2'
        target_field_group = feature_value.get('field_group')
        func = feature_value.get('func') or 'no_func'
        groupby = feature_value.get('groupby')
        return Y_DimensionBuilder(feature_name=feature_name,
                                  target_field=target_field,
                                  target_field_group=target_field_group,
                                  func=func,
                                  groupby=groupby)


class ChartType(object):
    Line = 1
    Bar = 1 << 1
    Pie = 1 << 2
    Table = 1 << 3
    Csv = 1 << 4
    # following is not a true type, so use BIGGER case
    COMMON = Line | Bar | Table | Csv
    HIGHCHART = Line | Bar | Pie


class FeatureBuilder(object):

    """Build Feature for graph reporting by query objects from `search`
    """
    @staticmethod
    def create_feature(x_dimension, y_dimension, query_list):
        if not isinstance(y_dimension, Y_DimensionBuilder):
            raise Exception('y_dimension is not a Y_DimensionBuilder object!')

        func_name = y_dimension.func
        if func_name not in _AVAILABLE_FUNC:
            raise ParamError('func `%s` is not supported!' % func_name)

        func = _AVAILABLE_FUNC[func_name]
        # inspect whether x dimesion in query dict
        available_list = _inspect_x(x_dimension, query_list)
        return func(x_dimension, y_dimension, available_list)


def create_feature(chart_type, x_dimension, y_dimensions, order_by,
                   query_list):
    """This function used for create feature with query list
    by feature request from client
    """
    feature_list = []
    for y_dimension in y_dimensions:
        if isinstance(y_dimension, dict):
            y_dimension = Y_DimensionBuilder.from_dictionary(y_dimension)
        try:
            # add `__index` to query obj
            for index, query_obj in enumerate(query_list):
                query_obj.update({'__index': index})
            feature = FeatureBuilder.create_feature(x_dimension, y_dimension,
                                                    query_list)
        except TypeError as e:
            _LOGGER.exception(e)
            msg = 'field `%s` with operation[%s] illegal -> %s!' %\
                (y_dimension.target_field, y_dimension.func, e)
            raise ParamError(msg)
        except Exception as e:
            _LOGGER.exception(e)
            raise e
        feature_list.append(feature)
    if chart_type & ChartType.Pie:
        # merge feature to one dict
        first_feature = feature_list[0]
        other_features = feature_list[1:]
        for key in first_feature.keys():
            for f in other_features:
                first_feature[key].update(f[key])

        return first_feature
    elif chart_type & ChartType.COMMON:
        # merge feature to one list
        merge_list = []
        first_feature = feature_list[0]
        other_features = feature_list[1:]
        for key in first_feature.keys():
            for f in other_features:
                first_feature[key].update(f[key])
            tmp_dict = {'x_val': key, 'y_val': first_feature[key]}
            # here may be we can use 'insert sorting' to accelarate
            merge_list.append(tmp_dict)
        # here we sort the feature list by default,
        # later we will extend the `order` parameter to client
        if order_by is not None and len(merge_list) > 0:
            (order_field, reverse) = order_by
            if order_field == x_dimension:
                merge_list.sort(key=lambda x: x.get('x_val'), reverse=reverse)
            elif order_field in merge_list[0]['y_val']:
                merge_list.sort(key=lambda x: x.get('y_val').get(order_field),
                                reverse=reverse)
        return merge_list
    else:
        raise ParamError('chart_type not supported')


def create_multi_feature(chart_type, x_dimension, y_dimensions, order_by,
                         query_list):
    result = {}
    if chart_type & ChartType.Pie:
        result[ChartType.Pie] = create_feature(
            ChartType.Pie, x_dimension, y_dimensions, order_by, query_list)
    if chart_type & ChartType.COMMON:
        result[ChartType.COMMON] = create_feature(
            ChartType.COMMON, x_dimension, y_dimensions, order_by, query_list)

    return result
