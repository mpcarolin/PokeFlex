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

    def get_pokemon(self, id):
        result_json = {}
        queries = [
            "SELECT en FROM Pokemon WHERE flex_form='%s'" % id
        ]
        
        #Get the en from the Pokemon table
        self.cursor.execute(queries[0])
        en = self.cursor.fetchone()['en']
        queries.append("SELECT url FROM Model WHERE en='%s'" % en)

        #Get data from the Model table
        self.cursor.execute(queries[1])
        for url in self.cursor:
            if '-shiny' in str(url):
                result_json['shiny_model'] = url
            else:
                result_json['model'] = url
        
        return result_json

    def get_pokemon_by_dexnum(self, dexnum):
        queries = [
            "SELECT flex_form FROM Pokemon WHERE dex_num=%d" % dexnum
        ]

        #Get pid from the Pokemon table
        self.cursor.execute(queries[0])
        flex_form = self.cursor.fetchone()['flex_form']

        #empty the rest of the cursor
        self.cursor.fetchall()

        return self.get_pokemon(flex_form)
    
    def get_move(self, id):
        result_json = {}
        en = self._to_sql_id(id)
        queries = [
            "SELECT * FROM Move WHERE en='%s'" % en,
            "SELECT flag FROM MoveFlags WHERE en='%s'" % en,
        ]

        self.cursor.execute(queries[0])
        sql_json = self.cursor.next()
        
        #Standard fields
        result_json['ldesc'] = sql_json['ldesc']
        result_json['sdesc'] = sql_json['sdesc']
        
        #Optional fields
        result_json['z_power'] = sql_json['z_power']
        result_json['z_effect'] = self._get_z_effect_desc(sql_json['z_effect'])
        result_json['z_boost'] = sql_json['z_boost']
        
        self.cursor.execute(queries[1])
        flags = []
        for result in self.cursor:
            flag = result['flag']
            flags.append(flag_desc[flag])
        
        result_json['flags'] = flags
        
        return result_json
    
    def get_ability(self, id):
        result_json = {}
        en = self._to_sql_id(id)
        query = "SELECT * FROM Ability WHERE en='%s'" % en
        self.cursor.execute(query)
        sql_json = self.cursor.next()
        result_json['rating'] = sql_json['rating']
        result_json['ldesc'] = sql_json['ldesc']
        result_json['sdesc'] = sql_json['sdesc']
        return result_json
    
    def get_item(self, id):
        result_json = {}
        en = self._to_sql_id(id)
        query = "SELECT * FROM Item WHERE en='%s'" % en
        self.cursor.execute(query)
        sql_json = self.cursor.next()
        result_json['ldesc'] = sql_json['ldesc']
        result_json['sdesc'] = sql_json['sdesc']
        result_json['ng_type'] = sql_json['type']
        result_json['ng_power'] = sql_json['power']
        result_json['debut'] = sql_json['debut']
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

    def _to_sql_id(self, id):
        return id.replace('-','')