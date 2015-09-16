from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from armory.tank.mysql import ArmoryOrm

DB_CONNECT_STRING = "mysql://root:123456@localhost/tuangou?charset=utf8"
engine = create_engine(DB_CONNECT_STRING, echo=False, encoding='utf8')
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

conf = {"tuangou": "mysql://root:123456@127.0.0.1:3306/tuangou?charset=utf8"}
orm = ArmoryOrm()
orm.init_conf(conf)