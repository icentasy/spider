# -*- coding: utf-8 -*-
"""
    pylon.rest.manager
    ~~~~~~~~~~~~~~~~~~

    Provides: class `pylon.rest.manager.RESTManager`, this class is used to
    create RESTful APIS for models.

"""
from collections import defaultdict
from collections import namedtuple

import flask
from flask import Blueprint

from .helpers import primary_key_name
from .helpers import url_for
from .views import API
from .views import FunctionAPI

READONLY_METHODS = frozenset(('GET', ))


RestlessInfo = namedtuple('RestlessInfo', ['session',
                                           'universal_preprocessors',
                                           'universal_postprocessors'])


created_managers = []


APIInfo = namedtuple('APIInfo', 'collection_name blueprint_name')


class IllegalArgumentError(Exception):
    pass


class RESTManager(object):

    """
    RESTManger class, create RESTful APIs for model
    """
    APINAME_FORMAT = '{0}api'

    BLUEPRINTNAME_FORMAT = '{0}{1}'

    def __init__(self, app=None, **kw):
        self.app = app
        self.apis_to_create = defaultdict(list)
        self.created_apis_for = {}
        url_for.created_managers.append(self)

        self.session = kw.pop('session', None)
        if self.app is not None:
            self.init_app(self.app, **kw)

    def init_app(self, app, session=None,
                 preprocessors=None, postprocessors=None):
        # If the session was provided in the constructor, use that.
        if session is None:
            session = self.session
        # Use the `extensions` dictionary on the provided Flask object to store
        # extension-specific information.
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        if 'restless' in app.extensions:
            raise ValueError('Pylon-Restless has already been initialized on'
                             ' this application: {0}'.format(app))
        app.extensions['restless'] = RestlessInfo(session,
                                                  preprocessors or {},
                                                  postprocessors or {})

        apis = self.apis_to_create
        to_create = apis.pop(app, []) + apis.pop(None, [])
        for args, kw in to_create:
            blueprint = self.create_api_blueprint(app=app, *args, **kw)
            app.register_blueprint(blueprint)

    def url_for(self, model, **kw):
        """Returns the URL for the specified model, similar to
        :func:`flask.url_for`.

        `model` is a SQLAlchemy model class. This must be a model on which
        :meth:`create_api_blueprint` has been invoked previously.

        This method only returns URLs for endpoints created by this
        :class:`RESTManager`.

        The remaining keyword arguments are passed directly on to
        :func:`flask.url_for`.

        """
        collection_name = self.collection_name(model)
        api_name = RESTManager.api_name(collection_name)
        blueprint_name = self.blueprint_name(model)
        joined = '.'.join([blueprint_name, api_name])
        return flask.url_for(joined, **kw)

    @staticmethod
    def api_name(collection_name):
        return RESTManager.APINAME_FORMAT.format(collection_name)

    def collection_name(self, model):
        return self.created_apis_for[model].collection_name

    @staticmethod
    def _next_blueprint_name(blueprints, basename):
        """Returns the next name for a blueprint with the specified base name.

        This method returns a string of the form ``'{0}{1}'.format(basename,
        number)``, where ``number`` is the next non-negative integer not
        already used in the name of an existing blueprint.

        For example, if `basename` is ``'personapi'`` and blueprints already
        exist with names ``'personapi0'``, ``'personapi1'``, and
        ``'personapi2'``, then this function would return ``'personapi3'``. We
        expect that code which calls this function will subsequently register a
        blueprint with that name, but that is not necessary.

        `blueprints` is the list of blueprint names that already exist, as read
        from :attr:`Flask.blueprints` (that attribute is really a dictionary,
        but we simply iterate over the keys, which are names of the
        blueprints).

        """
        # blueprints is a dict whose keys are the names of the blueprints
        existing = [name for name in blueprints if name.startswith(basename)]
        # if this is the first one...
        if not existing:
            next_number = 0
        else:
            # for brevity
            b = basename
            existing_numbers = [int(n.partition(b)[-1]) for n in existing]
            next_number = max(existing_numbers) + 1
        return RESTManager.BLUEPRINTNAME_FORMAT.format(basename, next_number)

    def create_api_blueprint(self, model, app=None, methods=READONLY_METHODS,
                             url_prefix='/api', collection_name=None,
                             allow_patch_many=False, allow_delete_many=False,
                             allow_functions=False, exclude_columns=None,
                             include_columns=None, include_methods=None,
                             validation_exceptions=None, results_per_page=10,
                             max_results_per_page=100,
                             post_form_preprocessor=None, preprocessors=None,
                             postprocessors=None, primary_key=None,
                             serializer=None, deserializer=None):
        if app is None:
            app = self.app
        restlessinfo = app.extensions['restless']
        if collection_name is None:
            collection_name = model.__tablename__
        # convert all method names to upper case
        methods = frozenset((m.upper() for m in methods))
        # sets of methods used for different types of endpoints
        no_instance_methods = methods & frozenset(('POST', ))
        instance_methods = \
            methods & frozenset(('GET', 'PATCH', 'DELETE', 'PUT'))
        possibly_empty_instance_methods = methods & frozenset(('GET', ))
        if allow_patch_many and ('PATCH' in methods or 'PUT' in methods):
            possibly_empty_instance_methods |= frozenset(('PATCH', 'PUT'))
        if allow_delete_many and 'DELETE' in methods:
            possibly_empty_instance_methods |= frozenset(('DELETE', ))

        # Check that primary_key is included for no_instance_methods
        if no_instance_methods:
            pk_name = primary_key or primary_key_name(model)
            if (include_columns and pk_name not in include_columns or
                    exclude_columns and pk_name in exclude_columns):
                msg = ('The primary key must be included for APIs with POST.')
                raise IllegalArgumentError(msg)

        # the base URL of the endpoints on which requests will be made
        collection_endpoint = '/{0}'.format(collection_name)
        # the name of the API, for use in creating the view and the blueprint
        apiname = RESTManager.api_name(collection_name)
        # Prepend the universal preprocessors and postprocessors specified in
        preprocessors_ = defaultdict(list)
        postprocessors_ = defaultdict(list)
        preprocessors_.update(preprocessors or {})
        postprocessors_.update(postprocessors or {})
        for key, value in restlessinfo.universal_preprocessors.items():
            preprocessors_[key] = value + preprocessors_[key]
        for key, value in restlessinfo.universal_postprocessors.items():
            postprocessors_[key] = value + postprocessors_[key]
        # the view function for the API for this model
        api_view = API.as_view(apiname, model,
                               exclude_columns, include_columns,
                               include_methods, validation_exceptions,
                               results_per_page, max_results_per_page,
                               post_form_preprocessor, preprocessors_,
                               postprocessors_, primary_key, serializer,
                               deserializer)
        # suffix an integer to apiname according to already existing blueprints
        blueprintname = RESTManager._next_blueprint_name(app.blueprints,
                                                         apiname)
        # add the URL rules to the blueprint: the first is for methods on the
        # collection only, the second is for methods which may or may not
        # specify an instance, the third is for methods which must specify an
        # instance
        # TODO what should the second argument here be?
        # TODO should the url_prefix be specified here or in register_blueprint
        blueprint = Blueprint(blueprintname, __name__, url_prefix=url_prefix)
        # For example, /api/person.
        blueprint.add_url_rule(collection_endpoint,
                               methods=no_instance_methods, view_func=api_view)
        # For example, /api/person/1.
        blueprint.add_url_rule(collection_endpoint,
                               defaults={'instid': None, 'relationname': None,
                                         'relationinstid': None},
                               methods=possibly_empty_instance_methods,
                               view_func=api_view)
        # the per-instance endpoints will allow both integer and string primary
        # key accesses
        instance_endpoint = '{0}/<instid>'.format(collection_endpoint)
        # For example, /api/person/1.
        blueprint.add_url_rule(instance_endpoint, methods=instance_methods,
                               defaults={'relationname': None,
                                         'relationinstid': None},
                               view_func=api_view)
        # add endpoints which expose related models
        relation_endpoint = '{0}/<relationname>'.format(instance_endpoint)
        relation_instance_endpoint = \
            '{0}/<relationinstid>'.format(relation_endpoint)
        # For example, /api/person/1/computers.
        blueprint.add_url_rule(relation_endpoint,
                               methods=possibly_empty_instance_methods,
                               defaults={'relationinstid': None},
                               view_func=api_view)
        # For example, /api/person/1/computers/2.
        blueprint.add_url_rule(relation_instance_endpoint,
                               methods=instance_methods,
                               view_func=api_view)
        # if function evaluation is allowed, add an endpoint at /api/eval/...
        # which responds only to GET requests and responds with the result of
        # evaluating functions on all instances of the specified model
        if allow_functions:
            eval_api_name = apiname + 'eval'
            eval_api_view = FunctionAPI.as_view(eval_api_name, model)
            eval_endpoint = '/eval' + collection_endpoint
            blueprint.add_url_rule(eval_endpoint, methods=['GET'],
                                   view_func=eval_api_view)
        # Finally, record that this RESTManager instance has created an API for
        # the specified model.
        self.created_apis_for[model] = APIInfo(collection_name, blueprint.name)
        return blueprint

    def create_api(self, *args, **kw):
        if self.app is not None:
            app = self.app
            blueprint = self.create_api_blueprint(app=app, *args, **kw)
            app.register_blueprint(blueprint)
        else:
            self.apis_to_create[None].append((args, kw))
