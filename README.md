# TLDR 

PokeFlex is like your own PokeAPI, with auto-caching,
JSON schema customization, and simplified server startup.

# Setup and Run
First configure config.json with your parameters. Then execute:
>`python setup.py install`
>
>`python main.py`

PokeFlex will be available on localhost:5000

# Full Story
PokeFlex provides REST api endpoints to PokeAPI, running on an easy to
boot python server. Why, you may ask, would one want this when there is, you know, 
PokeAPI? Here's why we needed it:

## Caching
PokeAPI has a fair use policy that limits the requests you can
make to an individual resource per day. PokeFlex caches http
API response data on disk to minimize the number of requests
you make to PokeAPI. We also provide the means for you to 
specify how often you would like PokeFlex to ditch the cache
and resynchronize with PokeAPI.

## Simple Schema Modification
For our particular use, we needed to both modify and add to the JSON that
PokeAPI serves. Flex API simplifies this procedure.

## Simple Endpoint Modification
We also had a few sources of data that PokeAPI did not supply. Flex API enables
developers to easily add additional endpoints to serve resources, as if they
were also provided by PokeAPI.

## Encapsulation and Reuse
We wanted to separate all this code onto a separate server. By doing this we
can reuse our individual server for multiple applications that need the same
cached, modified JSON data. This also helps with encapsulation: our application
code can worry about application stuff and just query a single URI for all its 
needs.

####



