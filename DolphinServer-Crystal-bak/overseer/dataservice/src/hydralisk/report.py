# -*- coding: utf-8 -*-
"""
    hydralisk.report
    ~~~~~~~~~~~~~~~~

    Generate pictures from multalisk returned data, using phantomJS exporting
    server set up by Highchart offical convert js file. Mail template should be
    written by jinja2 template lang.
"""

import re
import csv
import json
import logging
import requests
from io import open
from uuid import uuid4

from jinja2 import Template

from multalisk.core.feature import ChartType
from multalisk.utils.custom_filter import n_days_ago

_LOGGER = logging.getLogger('hydralisk')
_TITLE_REGEX = r"<title>(.+?)</title>"


def create_report(render_conf, chart_datas, view_name, mail_template):
    '''create mail report, return email title, body, attachment and embedded
    images.
    You can use exported variables here in mail template, which should be
    written in `jinja2` template format.
    Now, exported variables include followings:
        - image_list: a cid list or url list
        - table_list: a table list order like ChartType.Table in APP_CONF
    More exported meta info will be supported...
    '''
    _LOGGER.debug('create report origin data:%s', chart_datas)
    server = render_conf['server']
    is_upload = render_conf.get('upload', False)
    embeddeds = []
    attachments = []

    table_list = []
    image_list = []
    for chart_type, chart_data in chart_datas.iteritems():
        if chart_type & ChartType.HIGHCHART:
            cur_pics = _generate_chart(server, chart_data, view_name,
                                       is_upload)
            cur_pics, embeddeds_new = _normalize_images(cur_pics, is_upload)
            image_list.extend(cur_pics)
            embeddeds.extend(embeddeds_new)
        if chart_type & ChartType.Table:
            table_list.extend(chart_data)
        if chart_type & ChartType.Csv:
            attachments.extend(_generate_csv(chart_data, view_name))

    if mail_template.startswith('/'):
        with open(mail_template, encoding='utf-8') as source:
            mail_template = source.read()

    template = Template(mail_template)
    # TODO: supply more meta info
    report_data = template.render(image_list=image_list, table_list=table_list)
    try:
        report_title = re.search(_TITLE_REGEX, report_data,
                                 re.IGNORECASE | re.DOTALL).group(1)
    except AttributeError:
        report_title = view_name

    return report_title, report_data, attachments, embeddeds


def _normalize_images(origin_images, is_upload):
    embeddeds = []
    if is_upload:
        return _upload_image(origin_images), embeddeds
    else:
        # turn base64 list into cid list
        cid_list = []
        for index, content in enumerate(origin_images):
            cid = str(uuid4())
            embeddeds.append((content, cid, 'png', 'base64'))
            cid_list.append('cid:' + cid)
        return cid_list, embeddeds


def _upload_image(pic_list):
    """turn path list into url list"""
    raise NotImplementedError("upload interface is not implemented yet.")


def _generate_chart(server, chart_list, view_name, generate_file=False):
    """return base64 list of images or path list of images"""
    post_data = {}
    pic_list = []
    for chart_data in chart_list:
        post_data['infile'] = json.dumps(chart_data)
        if generate_file:
            file_name = '%s_%s_%s.png' % (
                view_name, n_days_ago(1), str(uuid4()))
            post_data['outfile'] = '/tmp/%s' % file_name

        res = requests.post(server, json=post_data)
        if res.ok:
            if generate_file:
                pic_list.append(post_data['outfile'])
            else:
                pic_list.append(res.text)
        else:
            pic_list.append("")
    return pic_list


def _generate_csv(chart_datas, view_name):
    csv_pathes = []
    for index, chart_data in enumerate(chart_datas):
        header = chart_data['headers']
        rows = chart_data['rows']
        file_name = '%s_%s(%s).csv' % (view_name, index, n_days_ago(1))
        with open('/tmp/%s' % file_name, 'wb') as csv_file:
            writer = csv.writer(csv_file, header)
            writer.writerow(header)
            writer.writerows(rows)
        csv_pathes.append('/tmp/%s' % file_name)
    return csv_pathes


if __name__ == '__main__':
    view_name = 'news_ru'
    data = '''{\
    "chart": {
        "type": "line"
    },
    "xAxis": {
        "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]
    },
    "series": [{
        "data": [29.9, 71.5, 106.4, 129.2, 144.0, 176.0,
            135.6, 148.5, 216.4, 194.1, 95.6, 54.4
        ]
    }, {
        "data": [129.9, 171.5, 1106.4, 1129.2, 1144.0, 1176.0,
            1135.6, 1148.5, 1216.4, 1194.1, 195.6, 154.4
        ]
    }]
}'''

    all_data = {'charts': json.loads(data), 'tables': []}
    render_conf = {
        'server': 'http://127.0.0.1:3005',
        'upload': False,
    }
    mail_template = u'''\
<html xmlns="http://www.w3.org/1999/xhtml">
　<head>
　　<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
　　<title>News Crawler Report</title>
　　<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
　</head>
<body>
    <p>This is just a test email, the following shoud be some base64 image:</p>
    {% for chart in image_list %}
        <p><img src="{{ chart }}" alt="" /></p>
    {% endfor %}
    <p>The following should be a table</p>

    {% for table in table_list %}
        <table>
            <tr>
            {% for header in table.headers %}
                <th> {{ header }} </th>
            {% endfor %}
            </tr>
            {% for row in table.rows %}
            <tr>
                {% for data in row %}
                    <td>{{ data }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
    {% endfor %}

    <p>Here is the End.</p>
</body>
</html>
'''
    report_title, report_data, _, _ = create_report(render_conf, all_data,
                                                    view_name, mail_template)
    print report_title, report_data
