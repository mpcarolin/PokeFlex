from mapping import ResponseMapper
from constants import ENDPOINTS as API
from sql_util import PokedexMySQLUtil

sql_util = PokedexMySQLUtil()
mapper = ResponseMapper()

BASE_URI = API["pokeapi"]["base_uri"]
ENDPOINTS = API["pokeapi"]["endpoints"]
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

@mapper.maps(uri('pokemon-by-name'), uri('pokemon-by-id'))
def pokemon_mapper(self, response):
    json = response.json()
    pid = _sql_format(json['name'])
    sql_json = sql_util.get_pokemon(pid)
    return _combine_dicts(json, sql_json)

@mapper.maps(uri('move-by-name'))
def move_mapper(self, response):
    json = response.json()
    mid = _sql_format(json['name'])
    sql_json = sql_util.get_move(mid)
    return _combine_dicts(json, sql_json)

@mapper.maps(uri('ability-by-name'))
def ability_mapper(self, response):
    json = response.json()
    aid = _sql_format(json['name'])
    sql_json = sql_util.get_ability(aid)
    return _combine_dicts(json, sql_json)

@mapper.maps(uri('item-by-name'))
def item_mapper(self, response):
    json = response.json()
    iid = _sql_format(json['name'])
    sql_json = sql_util.get_item(iid)
    return _combine_dicts(json, sql_json)

@mapper.maps(uri('set2'))
def set_mapper(self, response):
    json = response.json()
    return sql_util.get_set('gengar','ou', 6)

@mapper.maps(DEFAULT_ENDPOINTS)
def default_mapper(self, response):
    '''
    A method for all endpoints that don't need data from
    the MySQL database
    '''
    return response.json()

def _sql_format(pokemon_name):
    '''
    A helper method to insure that the arguments
    being passed to the PokedexMySQLUtil are
    formatted correctly.
    '''
    return pokemon_name.replace('-','')

def _combine_dicts(dict1, dict2):
        return {**dict1, **dict2}

