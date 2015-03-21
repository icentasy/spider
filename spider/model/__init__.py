from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECT_STRING = "mysql://root:123456@localhost/tuangou?charset=utf8"
engine = create_engine(DB_CONNECT_STRING, echo=False, encoding='utf8')
DB_Session = sessionmaker(bind=engine)
session = DB_Session()