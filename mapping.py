from functools import partial
from constants import ENDPOINTS

class JsonMapper(object):
    '''
    Base JsonMapper. Users should subclass JsonMapper and 
    define a function for every endpoint for which
    they want to map json. Do this using the @maps(endpoint)
    decorator, or manually assigning functions to the funcs
    property. Child initializers must call super init.
    '''
    def __init__(self):
        self.funcs = {}
        for key in ENDPOINTS.keys():
            self.funcs[key] = None

    def maps(self, endpoint):
        '''
        Decorator for assigning functions to endpoints. 
        Usage:
            @maps('/pokemon/')
            def foo(json):
                return ...
        '''
        def maps_decorator(func):
            self.funcs[endpoint] = partial(func, endpoint)
            def func_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return func_wrapper

        return maps_decorator

    def map(self, endpoint, json): 
        '''
        Calls the function assigned for mapping the endpoint.
        If no function is assigned, the unmodified json is returned.
        '''
        if endpoint in self.funcs and self.funcs[endpoint] is not None: 
            return self.funcs[endpoint](json)
        else:
            return json 

