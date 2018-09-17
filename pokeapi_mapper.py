from mapping import ResponseMapper
from constants import APIS
from sql_util import PokedexMySQLUtil

sql_util = PokedexMySQLUtil()
mapper = ResponseMapper()

API = APIS["pokeapi"]
BASE_URI = API["base_uri"]
ENDPOINTS = API["endpoints"]

def uri(key):
    print (BASE_URI + ENDPOINTS[key])
    return BASE_URI + ENDPOINTS[key]

POKEAPI_DEFAULT_ENDPOINTS = (uri('pokemon-species-by-id'), uri('pokemon-species-by-name'), uri('location'), 
                uri('location-area'), uri('encounter-method'), uri('encounter-condition'), 
                uri('encounter-condition-value'), uri('pokemon-habitat'), uri('pokemon-form'),
                uri('pokemon-color'), uri('pokemon-shape'), uri('evolution-chain'), uri('evolution-trigger'),
                uri('growth-rate'), uri('egg-group'), uri('stat'), uri('move-learn-method'),
                uri('move-target'), uri('move-category'), uri('move-battle-style'), uri('move-damage-class'),
                uri('contest-effect'), uri('contest-type'), uri('item-category'), uri('item-fling-effect'),
                uri('item-pocket'), uri('machine'), uri('berry'), uri('berry-firmness'), uri('berry-flavor'),
                uri('type'), uri('region'), uri('super-contest-effect'), uri('nature'), uri('ability-by-number'),
                uri('pokemon-by-id'))

@mapper.maps(uri('encounter'))
def encounter_mapper(self, exchange):
    return_json = {}
    encounter_data = []
    for json_obj in exchange.json():
        encounter_data.append(json_obj)

    return_json['encounter_potential'] = encounter_data
    return return_json


@mapper.maps(uri('pokemon-by-name'))
def pokemon_mapper(self, exchange):
    req_params = exchange.params
    pid = req_params['pokemon']
    sql_json = sql_util.get_pokemon(pid)
    return _combine_dicts(exchange.json(), sql_json)

@mapper.maps(uri('move-by-name'))
def move_mapper(self, exchange):
    req_params = exchange.params
    mid = req_params['move_name']
    sql_json = sql_util.get_move(mid)
    return _combine_dicts(exchange.json(), sql_json)

@mapper.maps(uri('ability-by-name'))
def ability_mapper(self, exchange):
    req_params = exchange.params
    aid = req_params['abil_name']
    sql_json = sql_util.get_ability(aid)
    return _combine_dicts(exchange.json(), sql_json)

@mapper.maps(uri('item-by-name'))
def item_mapper(self, exchange):
    req_params = exchange.params
    iid = req_params['item_name']
    sql_json = sql_util.get_item(iid)
    return _combine_dicts(exchange.json(), sql_json)

@mapper.maps(POKEAPI_DEFAULT_ENDPOINTS)
def default_pokeapi_mapper(self, exchange):
    '''
    A method for all endpoints that don't need data from
    the MySQL database
    '''
    return exchange.json()

print (APIS["smogon_dex"]["base_uri"] + APIS["smogon_dex"]["endpoints"]["set"])  

@mapper.maps(APIS["smogon_dex"]["base_uri"] + APIS["smogon_dex"]["endpoints"]["set"])
def default_smogon_mapper(self, exchange):
    return exchange.json()

def _combine_dicts(dict1, dict2):
        return {**dict1, **dict2}

