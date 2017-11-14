from config import PROJECT_NAME, CACHE_PATH, CACHE_NAME, SYNC_INTERVAL
import requests
import requests_cache

requests_cache.install_cache(
        cache_name = CACHE_NAME,
        backend='sqlite', 

class CachingAPI(object):
    def __init__(self):
        if not os.path.isdir(CACHE_PATH):
            os.mkdir(CACHE_PATH)
        




        
