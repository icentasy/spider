import sys
sys.path.append("../../")
from spider.model import city, deal


# from sqlalchemy import Column, and_
# from sqlalchemy.types import VARCHAR, Integer, Float, Date, Boolean
# from sqlalchemy.ext.declarative import declarative_base

# from spider.model import engine, session

# BaseModel = declarative_base()


# def init_db():
#     BaseModel.metadata.create_all(engine)


# def drop_db():
#     BaseModel.metadata.drop_all(engine)

# class Deal(BaseModel):
#     __tablename__ = 'deal'
#     id = Column(Integer, primary_key=True)
#     title = Column(VARCHAR(1024))
#     image = Column(VARCHAR(1024))
#     source = Column(VARCHAR(100))
#     detail = Column(VARCHAR(255))
#     out_link = Column(VARCHAR(1024))
#     new_price = Column(Float)
#     old_price = Column(Float)
#     location = Column(VARCHAR(255))
#     city = Column(VARCHAR(255))
#     type = Column(VARCHAR(255))
#     type_detail = Column(VARCHAR(255))
#     invalid_time = Column(Date)
#     is_show = Column(Boolean, default=True)


# class City(BaseModel):
#     __tablename__ = 'city'
#     id = Column(Integer, primary_key=True)
#     first_char = Column(VARCHAR(2))
#     pinyin = Column(VARCHAR(255))
#     name = Column(VARCHAR(255))


def save_list(table, content_list):
    try:
        session.execute(table.__table__.insert(), content_list)
        session.commit()
        return True
    except Exception as e:
        return False

def update_deal(cond_key, cond_value, data):
    session.query(Deal).filter(cond_key == cond_value).update(data)
    session.commit()

def excute_sql(sql):
    try:
        session.execute(sql)
        session.commit()
    except Exception as e:
        print e

def get_city_from_mysql():
    return City.query().all()

# init_db()

# if __name__ == '__main__':
#     init_db()
#     res = session.query(Deal.out_link)
#     for i in res:
#         print i