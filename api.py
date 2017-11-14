from flask_api import FlaskAPI
from functools import partial
import requests_cache as cache
import requests
import config
import json
import os

cache.install_cache(
    cache_name = config.CACHE_NAME,
    backend = config.CACHE_DB,
    expire_after = config.SYNC_INTERVAL
)

BASE_URI = 'https://pokeapi.co/api/v2'
ENDPOINTS = {
    "evolution-chain": "/evolution-chain",
    "move-battle-style": "/move-battle-style",
    "generation": "/generation",
    "evolution-trigger": "/evolution-trigger",
    "move": "/move",
    "encounter-condition-value": "/encounter-condition-value",
    "pokemon": "/pokemon",
    "move-damage-class": "/move-damage-class",
    "ability": "/ability",
    "pal-park-area": "/pal-park-area",
    "contest-effect": "/contest-effect",
    "machine": "/machine",
    "version": "/version",
    "pokemon-color": "/pokemon-color",
    "location": "/location",
    "item-attribute": "/item-attribute",
    "pokeathlon-stat": "/pokeathlon-stat",
    "pokemon-habitat": "/pokemon-habitat",
    "type": "/type",
    "pokemon-shape": "/pokemon-shape",
    "item-pocket": "/item-pocket",
    "pokemon-species": "/pokemon-species",
    "stat": "/stat",
    "encounter-method": "/encounter-method",
    "berry-flavor": "/berry-flavor",
    "nature": "/nature",
    "pokemon-form": "/pokemon-form",
    "item-fling-effect": "/item-fling-effect",
    "super-contest-effect": "/super-contest-effect",
    "move-ailment": "/move-ailment",
    "item-category": "/item-category",
    "move-learn-method": "/move-learn-method",
    "move-target": "/move-target",
    "location-area": "/location-area",
    "move-category": "/move-category",
    "language": "/language",
    "gender": "/gender",
    "region": "/region",
    "growth-rate": "/growth-rate",
    "item": "/item",
    "version-group": "/version-group",
    "berry": "/berry",
    "characteristic": "/characteristic",
    "egg-group": "/egg-group",
    "contest-type": "/contest-type",
    "berry-firmness": "/berry-firmness",
    "encounter-condition": "/encounter-condition",
    "pokedex": "/pokedex"
}

class DefaultJsonMapper(object):
    def map(self, endpoint, json): return json

class FlexApp(FlaskAPI):
    def __init__(self, json_mapper = DefaultJsonMapper()):
        super(FlexApp, self).__init__(config.PROJECT_NAME)
        self.json_mapper = json_mapper
        set_passthroughs(self, json_mapper)

    def map(self, endpoint, json):
        return self.json_mapper.map(endpoint, json)

def set_passthroughs(app, mapper):
    '''
    Passthrough routing methods for the PokeAPI endpoints.
    Set the app's json_mapper to change the mapping behavior.
    See DefaultJsonMapper for the expected signature for map.
    '''
    def template_func(endpoint):
        full_uri = BASE_URI + endpoint
        json = {
            'name': 'Pikachu',
            'color': 'Yellow',
            'type': 'Electric',
            'endpoint': full_uri
        }
        return mapper.map(endpoint, json)

    for name, endpoint in ENDPOINTS.items():
        f = partial(template_func, endpoint)
        f.__name__ = name
        app.add_url_rule(endpoint, view_func=f)




