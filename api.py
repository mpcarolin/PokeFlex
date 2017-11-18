from flask_api import FlaskAPI
from functools import partial
from mapping import JsonMapper
from constants import PROJECT_NAME, BASE_URI, ENDPOINTS
from constants import CACHE_NAME, CACHE_DB, SYNC_INTERVAL
import requests_cache as cache
import requests
import json
import os

# initialize the request caching
cache.install_cache(
    cache_name = CACHE_NAME,
    backend = CACHE_DB,
    expire_after = SYNC_INTERVAL
)

class FlexApp(FlaskAPI):
    def __init__(self, json_mapper = JsonMapper()):
        super(FlexApp, self).__init__(PROJECT_NAME)
        self.json_mapper = json_mapper
        set_passthroughs(self, json_mapper)

def set_passthroughs(app, mapper):
    '''
    Passthrough routing methods for the PokeAPI endpoints.
    All make GET requests and pass json to the defined mapper.
    Import an instance of JsonMapper and define json mappings
    using the @maps(...) decorator to determine how json is 
    transformed.
    '''
    def route(endpoint, param=None, params=None, **kwargs):
        '''
        Core passthrough function. Routes the endpoint by
        making a request to the full PokeAPI endpoint, then
        returns JSON transformed by the mapper.
        '''
        full_uri = make_uri(endpoint, param)
        response = requests.get(full_uri, params, **kwargs)
        poke_json = response.json()
        return mapper.map(endpoint, poke_json)

    for name, endpoint in ENDPOINTS.items():
        f = partial(route, endpoint)
        f.__name__ = name
        app.add_url_rule(endpoint, view_func=f)

def make_uri(endpoint, param=None):
    uri = BASE_URI + endpoint
    return add_param(uri, param)

def add_param(endpoint, param=None):
    if param is None or not requires_param(endpoint): 
        return endpoint

    start = endpoint.index('<')
    end = endpoint.index('>')
    return endpoint[:start] + str(param) + endpoint[end+1:]

def requires_param(endpoint):
    return ('<' in endpoint and '>' in endpoint)

