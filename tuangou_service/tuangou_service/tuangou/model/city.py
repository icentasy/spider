# -*- coding:utf-8 -*-
from tuangou.model import orm


class City(orm.Model):
    __tablename__ = "city"
    id = orm.Column(orm.Integer, primary_key=True)
    first_char = orm.Column(orm.VARCHAR(2))
    pinyin = orm.Column(orm.VARCHAR(255))
    name = orm.Column(orm.VARCHAR(255))