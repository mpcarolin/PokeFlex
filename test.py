from mapping import JsonMapper

mapper = JsonMapper()

# need to test the JSONMapper class. 
# Try subclassing with the decorator
@mapper.maps('/pokemon')
def pokemon_mapper(self, json):
    new_json = json
    new_json['weight'] = 78
    return new_json
