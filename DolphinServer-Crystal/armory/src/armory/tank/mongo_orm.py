# -*- coding: utf-8 -*-

'''
    Armory.tank.mongo_orm
    ~~~~~~~~~~~~~~~~~~~~~
    A mongo orm implemention based on mongokit
'''
from bson.dbref import DBRef
from mongokit.cursor import Cursor
from mongokit.operators import *
from mongokit.schema_document import *
from mongokit.mongo_exceptions import *
from mongokit.document import (Document, ObjectId,
                               DocumentProperties)
from mongokit.versioned_document import VersionedDocument
from mongokit.database import Database
from mongokit.collection import Collection
from mongokit.connection import (
    Connection as ConnectionOrigin,
    MongoClient, MongoReplicaSetClient,
    ReplicaSetConnection,
    CallableMixin
)
from mongokit.master_slave_connection import MasterSlaveConnection
from pymongo import (
    ASCENDING as INDEX_ASCENDING,
    DESCENDING as INDEX_DESCENDING,
    ALL as INDEX_ALL,
    GEO2D as INDEX_GEO2D,
    GEOHAYSTACK as INDEX_GEOHAYSTACK,
    GEOSPHERE as INDEX_GEOSPHERE,
    OFF as INDEX_OFF,
    HASHED as INDEX_HASHED
)
from mongokit.migration import DocumentMigration


class DocumentMeta(DocumentProperties):

    def __new__(cls, name, bases, dct):
        for base in bases:
            if base is CallableMixin:
                return type.__new__(cls, name, bases, dct)
        conn = dct['__session__']
        dct['__database__'] = conn._db_name
        dct['__collection__'] = dct['__tablename__']
        dct['__db_type__'] = 'mongo'
        if '_id' in dct['structure'] and dct['structure']['_id'] is ObjectId:
            dct.setdefault('default_values', {}).setdefault('_id', ObjectId)

        k = DocumentProperties.__new__(cls, name, bases, dct)

        conn.register([k])
        session = getattr(conn, name)
        k.__session__ = session
        k.query = session
        return k


class Connection(ConnectionOrigin):

    def __init__(self, *args, **kwargs):
        db = kwargs.pop('database', None)
        if not db:
            if len(args) < 3:
                raise ValueError('you must specify database')
            else:
                db = args[2]
        self._db_name = db
        super(Connection, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    conn = Connection(host='127.0.0.1', port=27017, database='test')

    class TestDoc(Document):
        __metaclass__ = DocumentMeta
        __tablename__ = 'test'
        __session__ = conn

        structure = {
            'age': int,
            'title': unicode,
        }

    print TestDoc.query.find_random()
