from functools import partial
from constants import APIS

class ResponseMapper(object):
    '''
    JsonMapper object. Users should import an instance of this class,
    then define the mapping functions using the maps decorator.
    '''
    def __init__(self):
        self.funcs = {}
        for api in APIS.keys():
            for name, endpoint in APIS[api]["endpoints"].items():
                self.funcs[endpoint] = lambda exchange: exchange.response.json()

    def maps(self, *endpoints):
        '''
        Decorator for assigning functions to endpoints. 
        Usage:
            @maps('/pokemon/')
            def foo(exchange): return modify(exchange.response.json()) ...
        '''
        def maps_decorator(func):
            for endpoint in endpoints:
                self.funcs[endpoint] = partial(func, endpoint)
            def func_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return func_wrapper
        return maps_decorator

    def map(self, endpoint, exchange): 
        '''
        Calls the function assigned for mapping the endpoint.
        If no function is assigned, the unmodified json is returned.
        '''
        if endpoint in self.funcs:
            return self.funcs[endpoint](exchange)
        else:
            return exchange.response.json()

