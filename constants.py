from configparser import SafeConfigParser
import json
import os

config = SafeConfigParser()
config.read('./config.ini')

PROJECT_NAME = config.get('USER', 'name')
ROOT_PATH = config.get('USER', 'root')

SYNC_INTERVAL = config.getint('USER', 'sync_interval')
CACHE_PATH = config.get('USER', 'cache_path')
CACHE_DB = config.get('USER', 'cache_db')
CACHE_NAME = PROJECT_NAME + '_cache'

with open('./endpoints.json', 'r') as f:
    ENDPOINTS = json.loads(f.read())

