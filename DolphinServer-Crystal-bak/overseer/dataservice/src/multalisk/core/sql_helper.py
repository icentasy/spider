# -*- coding:utf-8 -*-
"""
    multalisk.core.sql_helper
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Provide function to transform ORM query object to python dict
    Ralation-ship in ORM is supported.

"""
import inspect
import datetime
import uuid

from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.inspection import inspect as sqlalchemy_inspect
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import RelationshipProperty as RelProperty


RELATION_BLACKLIST = ('query', 'query_class', '_sa_class_manager',
                      '_decl_class_registry')


def primary_key_names(model):
    """Returns all the primary keys for a model."""
    return [key for key, field in inspect.getmembers(model)
            if isinstance(field, QueryableAttribute)
            and isinstance(field.property, ColumnProperty)
            and field.property.columns[0].primary_key]


def primary_key_name(model_or_instance):
    """Returns the name of the primary key of the specified model or instance
    of a model, as a string.

    If `model_or_instance` specifies multiple primary keys and ``'id'`` is one
    of them, ``'id'`` is returned. If `model_or_instance` specifies multiple
    primary keys and ``'id'`` is not one of them, only the name of the first
    one in the list of primary keys is returned.

    """
    its_a_model = isinstance(model_or_instance, type)
    model = model_or_instance if its_a_model else model_or_instance.__class__
    pk_names = primary_key_names(model)
    return 'id' if 'id' in pk_names else pk_names[0]


def is_mapped_class(cls):
    try:
        sqlalchemy_inspect(cls)
        return True
    except:
        return False


def to_dict(instance, deep=None):
    """change ORM Model instance to python dict
    `instance`: model object
    `deep`: related model dict
    """
    try:
        instance_type = type(instance)
        inspected_instance = sqlalchemy_inspect(instance_type)
        column_attrs = inspected_instance.column_attrs.keys()
    except NoInspectionAvailable as e:
        print e
        return instance
    result = dict((col, getattr(instance, col)) for col in column_attrs
                  if not (col.startswith('__')))
    for key, value in result.items():
        if isinstance(value, (datetime.date, datetime.time)):
            result[key] = value.isoformat()
        elif isinstance(value, uuid.UUID):
            result[key] = str(value)
        elif key not in column_attrs and is_mapped_class(type(value)):
            result[key] = to_dict(value)
    '''
    pacakging related instance
    '''
    deep = deep or {}
    for relation, rdeep in deep.items():
        relatedvalue = getattr(instance, relation)
        if relatedvalue is None:
            result[relation] = None
            continue
        result[relation] = [to_dict(inst, rdeep)
                            for inst in relatedvalue]

    return result


def get_relations(model):
    """Returns a list of relation names of `model` (as a list of strings)."""
    return [k for k in dir(model)
            if not (k.startswith('__') or k in RELATION_BLACKLIST)
            and get_related_model(model, k)]


def get_related_model(model, relationname):
    """Gets the class of the model to which `model` is related by the attribute
    whose name is `relationname`.

    """
    if hasattr(model, relationname):
        attr = getattr(model, relationname)
        if hasattr(attr, 'property') \
                and isinstance(attr.property, RelProperty):
            return attr.property.mapper.class_
        if isinstance(attr, AssociationProxy):
            return get_related_association_proxy_model(attr)
    return None


def get_related_association_proxy_model(attr):
    """Returns the model class specified by the given SQLAlchemy relation
    attribute, or ``None`` if no such class can be inferred.

    `attr` must be a relation attribute corresponding to an association proxy.

    """
    prop = attr.remote_attr.property
    for attribute in ('mapper', 'parent'):
        if hasattr(prop, attribute):
            return getattr(prop, attribute).class_
    return None


def inst_to_dict(model, inst):
    """Returns the dictionary representation of the specified instance.
    """
    relations = frozenset(get_relations(model))
    deep = dict((r, {}) for r in relations)
    return to_dict(inst, deep)
