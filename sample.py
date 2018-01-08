from mapping import ResponseMapper
from constants import APIS

BASE_URI = APIS["pokeapi"]["base_uri"]
ENDPOINTS = APIS["pokeapi"]["endpoints"]

def uri(key): return BASE_URI + ENDPOINTS[key]

mapper = ResponseMapper()

@mapper.maps(uri('test'))
def test_mapping(self, exchange):
    json = exchange.response.json()
    json['new key'] = 'new value'
    return json

@mapper.maps(uri('pokemon-by-id'))
def pokemon(self, exchange):
    json = exchange.response.json()
    json['new_key'] = 'new value'
    return json

