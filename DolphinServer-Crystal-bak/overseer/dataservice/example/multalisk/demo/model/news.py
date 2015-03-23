# -*- coding: utf-8 -*-
from multalisk.model import orm
from multalisk.model.base import MetaSQL


class News_Report_ru(object):
    __metaclass__ = MetaSQL
    __modelid__ = "1001"
    __tablename__ = "report_test_tr_tr"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30))
