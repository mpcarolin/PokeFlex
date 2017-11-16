from mapping import JsonMapper

mapper = JsonMapper()

@mapper.maps('/pokemon', '/berry')
def pokemon_mapper(self, json):
    new_json = json
    new_json['weight'] = 78
    return new_json

