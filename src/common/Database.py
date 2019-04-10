import sqlite3
from sqlite3 import Error
from src.common.utils import *

config = loadConfiguration("config/config.yaml")

class Database:
	def __init__(self, dbName):
		self.logger = getLogger(str(dbName)+"-Database")
		self.conn = self.createConnection("database/"+str(dbName)+".db")
		self.createTableIfNotExists()

	def createConnection(self, db_file):
		try:
			conn = sqlite3.connect(db_file)
			self.logger.info("Database connected : "+str(db_file))
		except Error as e:
			self.logger.exception(e)
		return conn

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

	def selectAll(self):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM posts")
		rows = cur.fetchall()
		data = []
		for row in rows:
			data.append(row)
		return data

	def closeSession(self):
		self.conn.close()
		self.logger.info("Connection closed")