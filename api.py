from flask_api import FlaskAPI
from functools import partial, reduce
from mapping import ResponseMapper
from constants import PROJECT_NAME, BASE_URI, ENDPOINTS
from constants import CACHE_NAME, CACHE_DB, SYNC_INTERVAL
import requests_cache as cache
import requests
import json
import os
import pdb
dbreak = pdb.set_trace

# initialize the request caching
cache.install_cache(
    cache_name = CACHE_NAME,
    backend = CACHE_DB,
    expire_after = SYNC_INTERVAL
)

class FlexApp(FlaskAPI):
    def __init__(self, json_mapper = ResponseMapper()):
        super(FlexApp, self).__init__(PROJECT_NAME)
        self.json_mapper = json_mapper
        set_passthroughs(self, json_mapper)

class ResponseWrapper(object):
    def __init__(self, response, param, params, **kwargs):
        self.response = response
        self.param = param
        self.params = params or []
        self.kwargs = kwargs

    def json(self, **kwargs):
        return self.response.json(**kwargs)

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def url(self):
        return self.response.url

    @property
    def request_method(self):
        return self.response.request.method

def set_passthroughs(app, mapper):
    '''
    Passthrough routing methods for the PokeAPI endpoints.
    All make corresponding HTTP requests and pass json to the 
    defined mapper.Import an instance of JsonMapper and define 
    json mappings using the @maps(...) decorator to determine 
    how json is transformed.
    '''
    def get(endpoint, param=None, params=None, **kwargs):
        '''
        Makes a GET request to endpoint, using specified
        params. Returns the json as mapped by the 
        mapping function assigned for that endpoint.
        '''
        full_uri = make_uri(endpoint, [param])
        response = requests.get(full_uri, params, **kwargs)
        wrapped_response = ResponseWrapper(response, param, params, kwargs=kwargs)
        return mapper.map(endpoint, wrapped_response)
    
    def post(url, data, json, **kwargs):
        raise NotImplementedError

    def put():
        raise NotImplementedError

    def head():
        raise NotImplementedError

    def trace():
        raise NotImplementedError
    
    def options():
        raise NotImplementedError

    def delete():
        raise NotImplementedError

    def connect():
        raise NotImplementedError

    def patch():
        raise NotImplementedError

    request_handlers = {
        'GET': get,
        'POST': post,
        'PUT': put,
        'HEAD': head,
        'TRACE': trace,
        'OPTIONS': options,
        'DELETE': delete,
        'CONNECT': connect,
        'PATCH': patch
    }

    # TODO: add more methods
    for method in ['GET']: 
        request_handler = request_handlers[method]
        uri_list = ENDPOINTS.items()
        for name, endpoint in uri_list:
            f = partial(request_handler, endpoint)
            f.__name__ = name
            app.add_url_rule(endpoint, view_func=f)

def make_uri(endpoint, params=[]):
    uri = BASE_URI + endpoint

    return add_param(uri, params[0])
    '''
    if not params or len(params) <= 0:
        return uri
    else:
        return reduce(add_param, params)
    '''

def add_param(endpoint, param=None):
    if param is None or not requires_param(endpoint): 
        return endpoint

    start = endpoint.index('<')
    end = endpoint.index('>')
    return endpoint[:start] + str(param) + endpoint[end+1:]

def requires_param(endpoint):
    return ('<' in endpoint and '>' in endpoint)

