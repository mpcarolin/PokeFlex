from flask_api import FlaskAPI
from flask import request
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

def SET_CORS(allowed_uris):


class FlexApp(FlaskAPI):
    '''
    App for hosting an API. 
    '''
    def __init__(self, json_mapper = ResponseMapper()):
        super(FlexApp, self).__init__(PROJECT_NAME)
        self.json_mapper = json_mapper
        set_passthroughs(self, json_mapper)

class HTTPExchange(object):
    '''
    A wrapper around the flask request and response objects that constitute
    the http exchange for a given endpoint. This is passed to the mapping 
    methods. Only accepts the response object since it contains the request
    object.
    '''
    def __init__(self, response, params={}):
        self.response = response
        self.params = params

    def json(self):
        try:
            return self.response.json()
        except Exception as e: #TODO: make more specific
            return {}

    @property
    def request(self):
        return self.response.request

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
    def make_handler(http_method):
        def adapted_handler(endpoint, flask_request): 
            args = flask_request.args
            json = flask_request.data
            if http_method == 'GET':
                return requests.get(endpoint, params=args)
            elif http_method == 'POST':
                return requests.post(endpoint, data=args, json=json)
            elif http_method == 'PUT':
                return requests.put(endpoint, data=json)
            elif http_method == 'DELETE':
                return requests.delete(endpoint)

        return adapted_handler
        

    request_handlers = { method: make_handler(method) for method in ['GET', 'POST', 'PUT', 'DELETE'] }

    def dispatch(endpoint, **params):
        '''
        Executes the request handler for the current request (as supplied by the
        flask request class), obtains the response, then maps it using the 
        mapper object passed to set_passthroughs
        '''
        full_uri = make_uri(endpoint, params)
        api_request_handler = request_handlers[request.method]
        response = api_request_handler(full_uri, request)
        response.headers.add('Access-Control-Allow-Origin', '*')
        exchange = HTTPExchange(response, params=params)

        return mapper.map(endpoint, exchange)

    def assign_routing_rules_for_api(api_data):
        '''
        @param api_data: A dictionary with two key-value pairs:
                - base_uri:  The base uri that prefixes all endpoints
                - endpoints: A dictionary of endpoint names to endpoints. 
                             Any parameters specified using flask syntax
        '''
        base_uri = api_data["base_uri"]
        uri_list = api_data["endpoints"].items()
        for name, endpoint in uri_list:
            full_uri = base_uri + endpoint
            f = partial(dispatch, full_uri)
            f.__name__ = name
            app.add_url_rule(endpoint, view_func=f, methods=request_handlers.keys())

    for api_info in APIS.values():
        assign_routing_rules_for_api(api_info)


def make_uri(uri, params):
    '''
    Replaces parameters in the uri with parameters in the
    params dict. The uri endpoint should specify parameters
    using the flask syntax <type:name>, such as <string:color>
    '''
    for name, value in params.items():
        pattern = '<.*:name>'.replace('name', name)
        uri = re.sub(pattern, str(value), uri, count=1)

    return uri
