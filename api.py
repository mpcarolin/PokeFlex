from flask_api import FlaskAPI
from functools import partial, reduce
from mapping import ResponseMapper
from constants import PROJECT_NAME, APIS
from constants import CACHE_NAME, CACHE_DB, SYNC_INTERVAL
import requests_cache as cache
import requests
import json
import pdb
import os
import re
dbreak = pdb.set_trace

# initialize the request caching
cache.install_cache(
    cache_name = CACHE_NAME,
    backend = CACHE_DB,
    expire_after = SYNC_INTERVAL
)

class FlexApp(FlaskAPI):
    '''
    App for hosting an API. 
    '''
    def __init__(self, json_mapper = ResponseMapper()):
        super(FlexApp, self).__init__(PROJECT_NAME)
        self.json_mapper = json_mapper
        set_passthroughs(self, json_mapper)

class ResponseWrapper(object):
    '''
    A response object passed to the mapping methods. 
    Contains the api response object and the parameters
    from the request (if any)
    '''
    def __init__(self, response, params):
        self.response = response
        self.params = params or {}

    def json(self):
        try:
            return self.response.json()
        except Exception as e: #TODO: make more sepecific
            return {}

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
    All make corresponding HTTP requests and pass a response object 
    to the defined mapper. Import an instance of JsonMapper and define 
    json mappings using the @maps(...) decorator to specify 
    a json transformation.
    '''
    def get(endpoint, **params):
        '''
        Makes a GET request to endpoint, using specified
        params. Returns the json as mapped by the 
        mapping function assigned for that endpoint.
        '''
        full_uri = make_uri(endpoint, params)
        response = requests.get(full_uri)
        wrapped_response = ResponseWrapper(response, params=kwargs)
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
        api_list = APIS.keys()
        for api in api_list:
            base_uri = APIS[api]["base_uri"]
            uri_list = APIS[api]["endpoints"].items()
            for name, endpoint in uri_list:
                full_uri = base_uri + endpoint
                f = partial(request_handler, full_uri)
                f.__name__ = name
                app.add_url_rule(endpoint, view_func=f)

def make_uri(uri, params):
    for name, value in params.items():
        pattern = '<.*:name>'.replace('name', name)
        uri = re.sub(pattern, str(value), uri, count=1)

    return uri