# -*- coding:utf-8 -*-
from spider.model import orm


class Deal(orm.Model):
    __tablename__ = 'deal'
    # __route_key__ = "tuangou"
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
    is_show = orm.Column(orm.Boolean, default=True)

    # def __init__(self, id, title, image, source, detail, out_link, new_price, old_price,
    #     location, city, type, type_detail, invalid_time, is_show):
    #     self.id = id
    #     self.title = title
    #     self.image = image
    #     self.source = source
    #     self.detail = detail
    #     self.out_link = out_link
    #     self.new_price = new_price
    #     self.old_price = old_price
    #     self.location = location
    #     self.city = city
    #     self.type = type
    #     self.type_detail = type_detail
    #     self.invalid_time = invalid_time
    #     self.is_show = is_show