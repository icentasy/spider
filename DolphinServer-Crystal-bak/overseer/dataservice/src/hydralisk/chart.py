# -*- coding: utf-8 -*-
"""
    hydralisk.chart
    ~~~~~~~~~~~~~~~

    Create charts data for hydralisk app to create report mail.
"""
import logging
import copy
from collections import defaultdict

from multalisk.model import MODEL_CONF
from multalisk.core.search import search
from multalisk.core.sql_helper import inst_to_dict
from multalisk.core.feature import create_multi_feature, ChartType
from multalisk.utils.exception import ParamError


_LOGGER = logging.getLogger('hydralisk')

_HIGHCHART_NAME_DCT = {
    ChartType.Pie: 'pie',
    ChartType.Line: 'line',
    ChartType.Bar: 'bar'
}


def _get_model_info(model_id):
    """get model info by model_id from MODEL_CONF init at model/init.py
    """
    if model_id not in MODEL_CONF:
        msg = 'model id[%s] not configed in MODEL_CONF!' % model_id
        raise ParamError(msg)
    model_dict = MODEL_CONF[model_id]
    return (model_dict['db_type'],
            model_dict['model_class'],
            model_dict['mapped_db'])


def create_format_data(chart_conf):
    """create formatted data for email, return a dict include all formatted
    data. The key for result is chart type(may be multi)
    """
    result = defaultdict(list)
    for chart_item in chart_conf:
        model_id = chart_item['model_id']
        x_dimension = chart_item['x_dimension']
        y_dimension = chart_item['y_dimension']
        order_by = chart_item.get('order_by')
        search_q = chart_item['default_q']
        chart_type = chart_item['chart_type']

        db_type, model_class, mapped_db = _get_model_info(model_id)
        query = search(db_type, model_class, search_q)

        if db_type.endswith('sql'):
            objects = [inst_to_dict(model_class, x) for x in query]
        else:
            objects = [x for x in query]

        feature_list = create_multi_feature(chart_type, x_dimension,
                                            y_dimension, order_by, objects)
        # Table and csv use same data structure
        key = (chart_type & ChartType.Table) | (chart_type &
                                                ChartType.Csv)
        if key:
            result[key].append(_convert_to_table(
                feature_list[ChartType.COMMON], chart_item))
        # BadDesign: pie use different struct from others
        if chart_type & ChartType.Pie:
            high_charts = _convert_to_highchart(feature_list[
                ChartType.Pie], chart_item, 'pie')
            result[ChartType.Pie].extend(high_charts)
        # line and bar use same
        key = (chart_type & ChartType.Line) | (chart_type &
                                               ChartType.Bar)
        if key:
            high_charts = _convert_to_highchart(
                feature_list[ChartType.COMMON], chart_item,
                _HIGHCHART_NAME_DCT.get(chart_type))
            result[key].extend(high_charts)

    return result


def _convert_to_highchart(origin_data, conf, chart_type):
    # TODO:some highchart options should be exported to app users
    infile = {
        'chart': {
            'type': chart_type
        },
        'title': {
            'text': conf.get('title', '')
        },
        'series': [],
    }
    if chart_type == 'pie':
        # data for pie is unordered, and x axis is not needed
        # each y_name is a new pie picture
        infile['plotOptions'] = {
            'pie': {
                'dataLabels': {
                    'enabled': True,
                    'format': '<b>{point.name}</b>: {point.percentage:.1f} %',
                }
            }
        }
        result = {}
        for y_conf in conf['y_dimension']:
            cur_infile = copy.deepcopy(infile)
            cur_infile.update({
                'yAxis': {
                    'title': {
                        'text': y_conf['name'],
                    }
                },
                'series': [{
                    'name': y_conf['name'],
                    'data': [],
                }]
            })
            result[y_conf['name']] = cur_infile
        for y_name, y_dct in origin_data.iteritems():
            for feature_name, feature_value in y_dct.iteritems():
                result[feature_name]['series'][0][
                    'data'].append({
                        'name': y_name,
                        'y': feature_value
                    })
        return result.values()
    else:
        # data for line or bar is ordered as list, y_val is a dict
        # all value are drawn at one pic
        infile.setdefault('xAxis', {}).setdefault('categories', [])
        temp_yval_dct = {}
        for data_dct in origin_data:
            infile['xAxis']['categories'].append(data_dct['x_val'])
            for y_name, y_data in data_dct['y_val'].iteritems():
                temp_yval_dct.setdefault(y_name, []).append(y_data)
        for y_name, y_data in temp_yval_dct.iteritems():
            infile['series'].append({
                'name': y_name,
                'data': y_data,
            })
        return [infile]


def _convert_to_table(origin_data, conf):
    """simpify result to format like following:
    {
        headers:[header1(primary_key), header2,...heardern], n columns
        rows:[[data1, data2, ..., datan]...], m rows
        It descs a m * n table.
    }
    """
    table = {'headers': [conf['x_dimension']], 'rows': []}
    auxiliary_dct = {conf['x_dimension']: 0}
    for index, y_conf in enumerate(conf['y_dimension']):
        table['headers'].append(y_conf['name'])
        auxiliary_dct[y_conf['name']] = index + 1

    max_column = len(table['headers'])
    for data_dct in origin_data:
        cur_row = ['-'] * max_column
        cur_row[0] = data_dct['x_val']
        for y_name, y_data in data_dct['y_val'].iteritems():
            cur_row[auxiliary_dct[y_name]] = y_data

        table['rows'].append(cur_row)

    return table
