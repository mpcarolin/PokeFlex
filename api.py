from flask_api import FlaskAPI
import json

with open('config.json', 'r') as config:
    json = json.loads(config.read())
    PROJECT_NAME = json['project_name'] or __name__

class DefaultJsonMapper(object):
    def map(self, endpoint, json): return json

class FlexApp(FlaskAPI):
    def __init__(self, json_mapper = DefaultJsonMapper()):
        super(FlexApp, self).__init__(PROJECT_NAME)
        self.json_mapper = json_mapper
        set_passthroughs(self, json_mapper)

    def map(self, endpoint, json):
        return self.json_mapper.map(endpoint, json)

'''
Passthrough routing methods for the PokeAPI endpoints.
Set the app's json_mapper to change the mapping behavior.
See DefaultJsonMapper for the expected signature for map.
'''
def set_passthroughs(app, mapper):
    @app.route("/pokemon", methods=['GET'])
    def pokemon():
        json = {
            'name': 'Pikachu',
            'color': 'Yellow',
            'type': 'Electric'
        }
        return mapper.map("/pokemon", json)
    

    @app.route("/trainer", methods=['GET'])
    def trainer():
        json = {
            'name': 'Red',
            'color': '...well, red.',
            'goal': 'catch all pokemon. AT ALL COSTS.'
        }
        return mapper.map('/trainer', json)
     

