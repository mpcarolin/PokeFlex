import configparser
import mysql.connector

class PokedexMySQLUtil(object):
    '''
    A utility class for interacting with the "pokedex" database in
    MySQL
    '''
    def __init__(self):
        #Get configuration data from .ini file
        config = configparser.ConfigParser()
        config.read('config.ini')
        config = config['MySQL']
        self.db_connection = mysql.connector.connect(user=config['user'],
                                        password=config['password'],
                                        host=config['host'],
                                        database=config['database'])
        self.cursor = self.db_connection.cursor(dictionary=True, buffered=True)
    
    def get_pokemon(self, pid):
        result_json = {}
        queries = [
            "SELECT url FROM Model WHERE pid='%s'" % pid
        ]
        
        #Get data from the Model table
        self.cursor.execute(queries[0])
        for url in self.cursor:
            if '-shiny' in str(url):
                result_json['shiny_model'] = url
            else:
                result_json['model'] = url
        
        return result_json
    
    def get_move(self, mid):
        result_json = {}
        query = "SELECT * FROM Move WHERE mid='%s-m'" % mid
        self.cursor.execute(query)
        sql_json = self.cursor.next()
        result_json['z_power'] = sql_json['z_power']
        result_json['z_effect'] = sql_json['z_effect']
        result_json['crystal'] = sql_json['crystal']
        result_json['max_pp'] = sql_json['max_pp']
        result_json['ldesc'] = sql_json['ldesc']
        result_json['sdesc'] = sql_json['sdesc']
        return result_json
    
    def get_ability(self, aid):
        result_json = {}
        query = "SELECT * FROM Ability WHERE aid='%s-a'" % aid
        self.cursor.execute(query)
        sql_json = self.cursor.next()
        result_json['rating'] = sql_json['rating']
        result_json['ldesc'] = sql_json['ldesc']
        result_json['sdesc'] = sql_json['sdesc']
        return result_json

    def _combine_dicts(self, dict1, dict2):
        return {**dict1, **dict2}