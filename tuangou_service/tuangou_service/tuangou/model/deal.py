# -*- coding:utf-8 -*-
from tuangou.model import orm


class Deal(orm.Model):
    __tablename__ = 'deal'
    id = orm.Column(orm.Integer, primary_key=True)
    title = orm.Column(orm.VARCHAR(1024))
    image = orm.Column(orm.VARCHAR(1024))
    source = orm.Column(orm.VARCHAR(100))
    detail = orm.Column(orm.VARCHAR(255))
    out_link = orm.Column(orm.VARCHAR(1024))
    new_price = orm.Column(orm.Float)
    old_price = orm.Column(orm.Float)
    location = orm.Column(orm.VARCHAR(255))
    city = orm.Column(orm.VARCHAR(255))
    type = orm.Column(orm.VARCHAR(255))
    type_detail = orm.Column(orm.VARCHAR(255))
    invalid_time = orm.Column(orm.Integer)