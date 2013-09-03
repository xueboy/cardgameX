#coding:utf-8
#!/usr/bin/env python

from django.db import connections, connection, transaction


class DBConnection:
	
	def __init__(self, conn):
		self.myconnection = conn
		
		
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
		transaction.commit_unless_managed()		
		
		