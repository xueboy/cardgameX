#coding:utf-8
#!/usr/bin/env python

from django.db import connections, connection, transaction


class DBConnection:
	
	
	
	
	def __init__(self, conn):
		self.myconnection = conn
		self.last_id = -1
		
		
	@staticmethod  
	def getConnection(name=''):
		if name == '':
			name = 'default'
		return DBConnection(connections[name])
		
		
	def query(self, sql, param):
		cursor = self.myconnection.cursor()
		cursor.execute(sql, param)
		return cursor.fetchall()
		
		
	def excute(self, sql,param):
		cursor = self.myconnection.cursor()
		cursor.execute(sql, param)
		self.last_id = cursor.lastrowid
		transaction.commit_unless_managed()		
		
	def insert_id(self):	
		return self.last_id