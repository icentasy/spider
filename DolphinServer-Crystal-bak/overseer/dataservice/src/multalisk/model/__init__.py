# -*- coding: utf-8 -*-
"""
    multalisk.model.init
    ~~~~~~~~~~~~~~~~~~~~

    init db connection and `MODEL_CONF` dict.
    MODEL_CONF dict contains apps info as follows
    {
        `model_id`: {
            'db_type': 'mysql',
            'mapped_db': <db connection object>
            'model_class' <class Model>,# related one Model Class
        }
    }

"""
from hashlib import md5

from armory.tank.mysql import ArmoryOrm
from armory.tank.mongo import ArmoryMongo
from armory.tank.hive import ArmoryHive

from multalisk.utils.common import create_mongo_route


orm = ArmoryOrm()


DB_CONNS = {}

MODEL_CONF = {}


def init_db(db_conn_str, debug=False):
    """This function is used for init db connection object by conn_str
    including mongodb/mysql/hive.
    """
    db_dict = {}
    if db_conn_str.startswith('mysql://'):
        db_dict['type'] = 'mysql'
        db_orm = ArmoryOrm()
        db_orm.init_conf({'DEBUG': debug, 'db': db_conn_str})
        db_dict['obj'] = db_orm
    elif db_conn_str.startswith('mongodb://'):
        db_dict['type'] = 'mongo'
        # here we construct route name by `host`-`port`-`db`
        # and inspect mongo conn string
        db_route = create_mongo_route(db_conn_str)
        ArmoryMongo.init_conf({db_route: db_conn_str})
        db_dict['obj'] = db_route
    elif db_conn_str.startswith('hive://'):
        db_dict['type'] = 'hive'
        hive_orm = ArmoryHive(db_conn_str)
        hive_orm.hiveOpen()
        db_dict['obj'] = hive_orm
    else:
        # here we can add other db obj later
        db_dict['type'] = 'unknown'
        db_dict['obj'] = None

    return db_dict


def init_model(model_conf, debug=False):
    """This function is used for init data model
    """
    for model in model_conf:
        model_id = model['model_id']
        db_conn_str = model['db_conn']
        db_conn_key = md5(db_conn_str).hexdigest()

        if not DB_CONNS.get(db_conn_key):
            DB_CONNS[db_conn_key] = init_db(db_conn_str, debug=debug)

        model_dict = MODEL_CONF.setdefault(model_id, {})
        model_dict['db_type'] = DB_CONNS[db_conn_key]['type']
        model_dict['mapped_db'] = DB_CONNS[db_conn_key]['obj']
