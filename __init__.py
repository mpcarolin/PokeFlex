import config as _config
import api
import os

if not os.path.isdir(_config.CACHE_PATH):
    os.mkdir(_config.CACHE_PATH)
