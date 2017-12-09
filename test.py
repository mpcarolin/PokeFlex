from mapping import ResponseMapper
from constants import ENDPOINTS

mapper = ResponseMapper()

@mapper.maps(ENDPOINTS['pokemon-by-name'], '/berry')
def pokemon_mapper(self, response):
    new_json = response.json()
    new_json['weight'] = 78
    return new_json

