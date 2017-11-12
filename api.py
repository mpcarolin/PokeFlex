from flask_api import FlaskAPI
import json

with open('config.json', 'r') as config:
    json = json.loads(config.read())
    PROJECT_NAME = json['project_name'] or __name__

class DefaultJsonMapper(object):
    def map(self, endpoint, json): return json

class FlexApp(FlaskAPI):
    def __init__(self):
        super(FlexApp, self).__init__(PROJECT_NAME)
        self.json_mapper = DefaultJsonMapper()

app = FlexApp()

class BaseApi(object):
    '''
    Passthrough routing methods for the PokeAPI endpoints.
    Accepts an optional json_mapper object that can transform
    json using the map method. See DefaultJsonMapper for the 
    expected signature for map.
    '''
    def __init__(self, json_mapper=None):
        self.app = app
        if json_mapper is not None:
            app.json_mapper = json_mapper
    
    def run(self, debug):
        return self.app.run(debug=debug)

    @app.route("/pokemon", methods=['GET'])
    def pokemon():
        json = {
            'name': 'Pikachu',
            'color': 'Yellow',
            'type': 'Electric'
        }
        return app.json_mapper.map("/pokemon", json)


