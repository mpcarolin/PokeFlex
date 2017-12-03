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
		query = "SELECT * from Pokemon WHERE pid='%s'" % pid
		self.cursor.execute(query)
		return self.cursor.next()