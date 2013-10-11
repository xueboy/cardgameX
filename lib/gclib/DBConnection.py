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
		self.cursor = self.myconnection.cursor()
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
		cursor = self.myconnection.cursor()
		cursor.execute(sql, param)
		self.last_id = cursor.lastrowid
		transaction.commit_unless_managed()		
		
	def insert_id(self):	
		return self.last_id