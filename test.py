from mapping import ResponseMapper
from constants import ENDPOINTS as API
from sql_util import PokedexMySQLUtil
import mysql.connector

sql_util = PokedexMySQLUtil()
mapper = ResponseMapper()

BASE_URI = API["pokeapi"]["base_uri"]
ENDPOINTS = API["pokeapi"]["endpoints"]

def uri(key): return BASE_URI + ENDPOINTS[key]

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
def move_mapper(self, response):
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

def _sql_format(pokemon_name):
    '''
    A helper method to insure that the arguments
    being passed to the PokedexMySQLUtil are
    formatted correctly.
    '''
    return pokemon_name.replace('-','')

def _combine_dicts(dict1, dict2):
        return {**dict1, **dict2}

