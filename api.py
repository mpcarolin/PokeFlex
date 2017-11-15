from flask_api import FlaskAPI
from functools import partial
from mapping import JsonMapper
import requests_cache as cache
import requests
import config
import json
import os

from constants import BASE_URI, ENDPOINTS

# initialize the request caching
cache.install_cache(
    cache_name = config.CACHE_NAME,
    backend = config.CACHE_DB,
    expire_after = config.SYNC_INTERVAL
)

def get_uri(endpoint):
    return BASE_URI + endpoint

class FlexApp(FlaskAPI):
    def __init__(self, json_mapper = JsonMapper()):
        super(FlexApp, self).__init__(config.PROJECT_NAME)
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

