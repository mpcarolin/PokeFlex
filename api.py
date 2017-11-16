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
    Set the app's json_mapper to change the mapping behavior.
    See DefaultJsonMapper for the expected signature for map.
    '''
    def template_func(endpoint):
        json = {
            'name': 'Pikachu',
            'color': 'Yellow',
            'type': 'Electric',
            'endpoint': get_uri(endpoint)
        }
        return mapper.map(endpoint, json)

    for name, endpoint in ENDPOINTS.items():
        f = partial(template_func, endpoint)
        f.__name__ = name
        app.add_url_rule(endpoint, view_func=f)

def get_uri(endpoint):
    return BASE_URI + endpoint
