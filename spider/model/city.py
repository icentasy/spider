# -*- coding:utf-8 -*-
from tuangou.model import orm


class City(orm.Model):
    __tablename__ = "city"
    __route_key__ = "tuangou"
    id = orm.Column(orm.Integer, primary_key=True)
    first_char = orm.Column(orm.VARCHAR(2))
    pinyin = orm.Column(orm.VARCHAR(255))
    name = orm.Column(orm.VARCHAR(255))

    def __init__(self, id, first_char, pinyin, name):
        self.id = id
        self.first_char = first_char
        self.pinyin = pinyin
        self.name = name