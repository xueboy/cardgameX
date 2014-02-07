#coding:utf-8
#!/usr/bin/env python

from django.db import connections, connection, transaction


class DBConnection:
	
	def __init__(self, conn):
		self.myconnection = conn
		self.last_id = -1
		self.cursor = None
		
		
	@staticmethod  
	def getConnection(name=''):
		if name == '':
			name = 'default'
		return DBConnection(connections[name])
		
		
	def query(self, sql, param):
		self.updateCursor()		
		self.cursor.execute(sql, param)
		return self.cursor.fetchall()
		
	def columns(self):
		if not self.cursor:
			return None
		col = []
		for desc in self.cursor.description:
			col.append(desc[0])
		return col
		
		
	def excute(self, sql,param):
		self.updateCursor()		
		row_count = self.cursor.execute(sql, param)
		self.last_id = self.cursor.lastrowid
		#transaction.commit_unless_managed()
		self.myconnection.commit()
		return row_count
		
	def insert_id(self):	
		return self.last_id
		
	def star_transaction(self):
		self.myconnection.set_autocommit(False)
		
	def excute_no_commit(self, sql, param):
		
		self.updateCursor()		
		row_count = self.cursor.execute(sql, param)
		self.last_id = self.cursor.lastrowid		
		return row_count
		
	def commit(self):
		self.myconnection.commit()
		self.myconnection.set_autocommit(True)
		
	def rollback(self):
		self.myconnection.rollback()
		self.myconnection.set_autocommit(True)
		
	def updateCursor(self):
		if not self.cursor:
			self.cursor = self.myconnection.cursor()