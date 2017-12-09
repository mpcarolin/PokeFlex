from mapping import JsonMapper
from sql_util import PokedexMySQLUtil
from constants import ENDPOINTS
import mysql.connector


mapper = JsonMapper()
sql_util = PokedexMySQLUtil()

@mapper.maps(ENDPOINTS['pokemon-by-name'], ENDPOINTS['pokemon-by-id'])
def pokemon_mapper(self, json):
    pid = _sql_format(json['name'])
    sql_json = sql_util.get_pokemon(pid)
    return _combine_dicts(json, sql_json)

@mapper.maps(ENDPOINTS['move-by-name'])
def move_mapper(self, json):
    mid = _sql_format(json['name'])
    sql_json = sql_util.get_move(mid)
    return _combine_dicts(json, sql_json)

@mapper.maps(ENDPOINTS['ability-by-name'])
def move_mapper(self, json):
    aid = _sql_format(json['name'])
    sql_json = sql_util.get_ability(aid)
    return _combine_dicts(json, sql_json)

@mapper.maps(ENDPOINTS['item-by-name'])
def item_mapper(self, json):
    iid = _sql_format(json['name'])
    sql_json = sql_util.get_item(iid)
    return _combine_dicts(json, sql_json)

@mapper.maps(ENDPOINTS['set'])
def set_mapper(self, json):
    return sql_util.get_set('genger','ou', 6)

def _sql_format(pokemon_name):
    '''
    A helper method to insure that the arguments
    being passed to the PokedexMySQLUtil are
    formatted correctly.
    '''
    return pokemon_name.replace('-','')

def _combine_dicts(dict1, dict2):
        return {**dict1, **dict2}