from functools import partial
from constants import ENDPOINTS

class ResponseMapper(object):
    '''
    JsonMapper object. Users should import an instance of this class,
    then define the mapping functions using the maps decorator.
    '''
    def __init__(self):
        self.funcs = {}
        for api in ENDPOINTS.keys():
            for name, endpoint in ENDPOINTS[api]["endpoints"].items():
                self.funcs[endpoint] = lambda response: response.json()

    def maps(self, *endpoints):
        '''
        Decorator for assigning functions to endpoints. 
        Usage:
            @maps('/pokemon/')
            def foo(json): return modify(json) ...
        '''
        def maps_decorator(func):
            for endpoint in endpoints:
                self.funcs[endpoint] = partial(func, endpoint)
            def func_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return func_wrapper
        return maps_decorator

    def map(self, endpoint, response): 
        '''
        Calls the function assigned for mapping the endpoint.
        If no function is assigned, the unmodified json is returned.
        '''
        if endpoint in self.funcs:
            return self.funcs[endpoint](response)
        else:
            return response.json()

