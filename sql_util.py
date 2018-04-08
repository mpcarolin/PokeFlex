import configparser
import mysql.connector

flag_desc = {
    "authentic" : "Ignores a target's substitute.",
    "bite" : "Power is multiplied by 1.5 when used by a Pokemon with the Ability Strong Jaw.",
    "bullet" : "Has no effect on Pokemon with the Ability Bulletproof.",
    "charge" : "The user is unable to make a move between turns.",
    "contact" : "Makes contact.",
    "dance" : "When used by a Pokemon, other Pokemon with the Ability Dancer can attempt to execute the same move.",
    "defrost" : "Thaws the user if executed successfully while the user is frozen.",
    "distance" : "Can target a Pokemon positioned anywhere in a Triple Battle.",
    "gravity" : "Prevented from being executed or selected during Gravity's effect.",
    "heal" : "Prevented from being executed or selected during Heal Block's effect.",
    "mirror" : "Can be copied by Mirror Move.",
    "mystery" : "Unknown effect.",
    "nonsky" : "Prevented from being executed or selected in a Sky Battle.",
    "powder" : "Has no effect on Grass-type Pokemon, Pokemon with the Ability Overcoat, and Pokemon holding Safety Goggles.",
    "protect" : "Blocked by Detect, Protect, Spiky Shield, and if not a Status move, King's Shield.",
    "pulse" : "Power is multiplied by 1.5 when used by a Pokemon with the Ability Mega Launcher.",
    "punch" : "Power is multiplied by 1.2 when used by a Pokemon with the Ability Iron Fist.",
    "recharge" : "If this move is successful, the user must recharge on the following turn and cannot make a move.",
    "reflectable" : "Bounced back to the original user by Magic Coat or the Ability Magic Bounce.",
    "snatch" : "Can be stolen from the original user and instead used by another Pokemon using Snatch.",
    "sound" : "Has no effect on Pokemon with the Ability Soundproof."
    }

z_effect_desc = {
    "clearnegativeboost" : "Clears negative stat boosts.",
    "heal" : "Heals the user.",
    "healreplacement" : "Heals the replacing Pokemon.",
    "crit2" : "Increases crit rate.",
    "redirect" : "Redirects all attacks this turn to the user.",
    "curse" : "If user is Ghost type, HP is restored. Otherwise, increases Attack by one more stage."
    }


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
    
    #TODO: Include move flags
    def get_move(self, mid):
        result_json = {}
        queries = [
            "SELECT * FROM Move WHERE mid='%s-m'" % mid,
            "SELECT flag FROM MoveFlags WHERE mid='%s-m'" % mid,
        ]

        self.cursor.execute(queries[0])
        sql_json = self.cursor.next()
        
        #Standard fields
        result_json['max_pp'] = sql_json['max_pp']
        result_json['ldesc'] = sql_json['ldesc']
        result_json['sdesc'] = sql_json['sdesc']
        
        #Optional fields
        result_json['z_power'] = sql_json['z_power']
        result_json['z_effect'] = self._get_z_effect_desc(sql_json['z_effect'])
        result_json['z_boost'] = sql_json['z_boost']
        result_json['crystal'] = sql_json['crystal']
        
        self.cursor.execute(queries[1])
        flags = []
        for result in self.cursor:
            flag = result['flag']
            flags.append(flag_desc[flag])
        
        result_json['flags'] = flags
        
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
    
    def get_item(self, iid):
        result_json = {}
        query = "SELECT * FROM Item WHERE iid='%s-i'" % iid
        self.cursor.execute(query)
        sql_json = self.cursor.next()
        result_json['ldesc'] = sql_json['ldesc']
        result_json['sdesc'] = sql_json['sdesc']
        result_json['ng_type'] = sql_json['type']
        result_json['ng_power'] = sql_json['power']
        result_json['debut'] = sql_json['debut']
        return result_json
    
    def get_set(self, pid, meta, gen):
        result_json = {}
        queries = [
            ("SELECT * FROM Trick WHERE pid = '%s'"
                    " AND tier_id = '%s'"
                    " AND gen = %d" % (pid, meta, gen)),
            "SELECT specie FROM pokemon WHERE pid='%s'" % pid
        ]
        
        #compile sets
        self.cursor.execute(queries[0])
        sets = []
        data = None
        for data in self.cursor:
            set = {}
            set['level'] = data['level']
            set['ability'] = data['ability']
            set['item'] = data['item']
            set['moves'] = [data['move_1'], data['move_2'], data['move_3'], data['move_4']]
            set['title'] = data['level']
            set['nature'] = data['nature']
            set['ivs'] = self._create_stat_dict_from_set('iv',data)
            set['evs'] = self._create_stat_dict_from_set('ev',data)
            sets.append(set)
        result_json['sets'] = sets
        
        #get general info about sets
        if data is not None:
            result_json['gen'] = data['gen']
            result_json['url'] = data['url']
            result_json['tier'] = data['tier']
        
        #Get the Pokemon's proper name
        self.cursor.execute(queries[1])
        sql_json = self.cursor.next()
        result_json['name'] = sql_json['specie']
        
        return result_json
    

    def _create_stat_dict_from_set(self, type, data):
        stats = ['hp','atk','def','spatk','spdef','spd']
        result = {}
        for stat in stats:
            result[stat] = data[stat+'_'+type]
        return result

    def _get_z_effect_desc(self, flag):
        if flag in z_effect_desc:
            return z_effect_desc[flag]

        return flag