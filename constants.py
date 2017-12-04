from configparser import SafeConfigParser
import os

config = SafeConfigParser()
config.read('./config.ini')

PROJECT_NAME = config.get('USER', 'name')
ROOT_PATH = config.get('USER', 'root')

SYNC_INTERVAL = config.getint('USER', 'sync_interval')
CACHE_PATH = config.get('USER', 'cache_path')
CACHE_DB = config.get('USER', 'cache_db')
CACHE_NAME = PROJECT_NAME + '_cache'

BASE_URI = 'https://pokeapi.co/api/v2'
ENDPOINTS = {
	#Used endpoints
	"pokemon-by-id": "/pokemon/<int:param>",
    "pokemon-by-name": "/pokemon/<string:param>",
	"move-by-name": "/move/<string:param>",
    "ability-by-name": "/ability/<string:param>",
    "item-by-name": "/item/<string:param>",

	#Unused endpoints
    "evolution-chain": "/evolution-chain",
    "move-battle-style": "/move-battle-style",
    "generation": "/generation",
    "evolution-trigger": "/evolution-trigger",
    "encounter-condition-value": "/encounter-condition-value",
    "all-pokemon": "/pokemon",
	"pokemon-forms": "/pokemon-form/<int:param>",
    "move-damage-class": "/move-damage-class",

    "pal-park-area": "/pal-park-area",
    "contest-effect": "/contest-effect",
    "machine": "/machine",
    "version": "/version",
    "pokemon-color": "/pokemon-color",
    "location": "/location",
    "item-attribute": "/item-attribute",
    "pokeathlon-stat": "/pokeathlon-stat",
    "pokemon-habitat": "/pokemon-habitat",
    "type": "/type",
    "pokemon-shape": "/pokemon-shape",
    "item-pocket": "/item-pocket",
    "pokemon-species": "/pokemon-species",
    "stat": "/stat",
    "encounter-method": "/encounter-method",
    "berry-flavor": "/berry-flavor",
    "nature": "/nature",
    "pokemon-form": "/pokemon-form",
    "item-fling-effect": "/item-fling-effect",
    "super-contest-effect": "/super-contest-effect",
    "move-ailment": "/move-ailment",
    "item-category": "/item-category",
    "move-learn-method": "/move-learn-method",
    "move-target": "/move-target",
    "location-area": "/location-area",
    "move-category": "/move-category",
    "language": "/language",
    "gender": "/gender",
    "region": "/region",
    "growth-rate": "/growth-rate",
    "version-group": "/version-group",
    "berry": "/berry",
    "characteristic": "/characteristic",
    "egg-group": "/egg-group",
    "contest-type": "/contest-type",
    "berry-firmness": "/berry-firmness",
    "encounter-condition": "/encounter-condition",
    "pokedex": "/pokedex"
}
