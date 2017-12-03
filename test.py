from mapping import JsonMapper
from sql_util import PokedexMySQLUtil
import mysql.connector

mapper = JsonMapper()
sql_util = PokedexMySQLUtil()

@mapper.maps('/pokemon/<int:param>')
def pokemon_mapper(self, json):
	return _supplement_pokemon(json)

@mapper.maps('/pokemon/<string:param>')
def pokemon_mapper(self, json):
	return _supplement_pokemon(json)

def _supplement_pokemon(json):
	pid = _sql_format(json['name'])
	sql_json = sql_util.get_pokemon(pid)
	json['pid'] = sql_json['pid']
	return json

def _sql_format(pokemon_name):
	'''
	A helper method to insure that the arguments
	being passed to the PokedexMySQLUtil are
	formatted correctly.
	'''
	return pokemon_name.replace('-','')