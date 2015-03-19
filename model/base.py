import sys
sys.path.append("../../")
from sqlalchemy import Column
from sqlalchemy.types import VARCHAR, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

from spider.model import engine

BaseModel = declarative_base()


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)

class Deal(BaseModel):
    __tablename__ = 'deal'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(1024))
    image = Column(VARCHAR(1024))
    source = Column(VARCHAR(100))
    detail = Column(VARCHAR(255))
    out_link = Column(VARCHAR(1024))
    new_price = Column(Float)
    old_price = Column(Float)
    location = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    type = Column(VARCHAR(255))


class City(BaseModel):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    first_char = Column(VARCHAR(2))
    pinyin = Column(VARCHAR(255))
    name = Column(VARCHAR(255))



if __name__ == '__main__':
    init_db()