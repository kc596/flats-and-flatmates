from sqlite3 import Error
from src.utils import loadConfiguration, getLogger
import pathlib
import sqlite3

config = loadConfiguration("config/config.yaml")

class Database:
	def __init__(self, dbName):
		self.database = "database/"+str(dbName)+".db"
		pathlib.Path("database/").mkdir(parents=True, exist_ok=True)
		self.logger = getLogger(str(dbName)+"-Database")
		self.conn = self.createConnection(self.database)
		self.createTableIfNotExists()

	def createConnection(self, db_file):
		try:
			conn = sqlite3.connect(db_file)
			conn.row_factory = self.dict_factory
			self.logger.info("Database connected : "+str(db_file))
			return conn
		except Error as e:
			self.logger.exception(e)

	# Used for getting dictionary from sqllite select query
	def dict_factory(self, cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	def createTableIfNotExists(self):
		try:
			cur = self.conn.cursor()
			cur.execute(config['database']['query']['create'])
			self.conn.commit()
		except Error as e:
			self.logger.exception(e)

	def insertPost(self, post):
		sql = config['database']['query']['insert']
		try:
			cur = self.conn.cursor()
			cur.execute(sql, post)
			self.conn.commit()
			self.logger.debug("Inserted post: "+str(post))
		except Error as e:
			self.logger.error(e)
			return -1
		return cur.lastrowid

	# Returns array of dictionary
	def select(self, query=config['database']['query']['select']):
		try:
			cur = self.conn.cursor()
			cur.execute(query)
			return cur.fetchall()
		except Error as e:
			self.logger.exception(e)
			return []

	def closeSession(self):
		self.conn.close()
		self.logger.info("Connection closed")