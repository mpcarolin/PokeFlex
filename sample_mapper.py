from mapping import ResponseMapper
from constants import APIS

mapper = ResponseMapper()

API = APIS["pokeapi"]
BASE_URI = API["base_uri"]
ENDPOINTS = API["endpoints"]

def uri(key): return BASE_URI + ENDPOINTS[key]

DEFAULT_ENDPOINTS = (uri('pokemon-species-by-id'), uri('pokemon-species-by-name'), uri('location'), 
                uri('location-area'), uri('encounter-method'), uri('encounter-condition'), 
                uri('encounter-condition-value'), uri('pokemon-habitat'), uri('pokemon-form'),
                uri('pokemon-color'), uri('pokemon-shape'), uri('evolution-chain'), uri('evolution-trigger'),
                uri('growth-rate'), uri('egg-group'), uri('stat'), uri('move-learn-method'),
                uri('move-target'), uri('move-category'), uri('move-battle-style'), uri('move-damage-class'),
                uri('contest-effect'), uri('contest-type'), uri('item-category'), uri('item-fling-effect'),
                uri('item-pocket'), uri('machine'), uri('berry'), uri('berry-firmness'), uri('berry-flavor'),
                uri('type'), uri('region'), uri('super-contest-effect'), uri('nature'))

@mapper.maps(uri('test'))
def post_mapper(self, exchange):
    import pdb; pdb.set_trace()
    return exchange.json()

@mapper.maps(uri('pokemon-by-name'), uri('pokemon-by-id'))
def pokemon_mapper(self, exchange):
    json = exchange.json()
    json['new-key'] = 'new value!'
    return json

def _combine_dicts(dict1, dict2):
        return {**dict1, **dict2}

