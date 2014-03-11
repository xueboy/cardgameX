#coding:utf-8
#!/usr/bin/env python

from django.db import connections, connection, transaction


class DBConnection:
	
	def __init__(self, conn):
		"""
		构造函数
		"""
		self.myconnection = conn
		self.last_id = -1
		self.cursor = None
		
		
	@staticmethod  
	def getConnection(name=''):
		"""
		得到连接
		"""
		if name == '':
			name = 'default'
		return DBConnection(connections[name])
		
		
	def query(self, sql, param):
		"""
		查询
		"""
		self.updateCursor()		
		self.cursor.execute(sql, param)
		return self.cursor.fetchall()
		
	def columns(self):
		"""
		列
		"""
		if not self.cursor:
			return None
		col = []
		for desc in self.cursor.description:
			col.append(desc[0])
		return col
		
	@transaction.autocommit
	def excute(self, sql,param):
		"""
		执行sql
		"""
		self.updateCursor()
		#self.star_transaction()
		row_count = self.cursor.execute(sql, param)
		self.last_id = self.cursor.lastrowid
		#transaction.commit_unless_managed()
		self.myconnection.commit()
		return row_count
		
	def insert_id(self):
		"""
		插入id
		"""
		return self.last_id
		
	def star_transaction(self):
		"""
		开始事物
		"""
		self.myconnection.set_autocommit(False)
		
	def excute_no_commit(self, sql, param):
		"""
		执行不提交
		"""
		
		self.updateCursor()		
		row_count = self.cursor.execute(sql, param)
		self.last_id = self.cursor.lastrowid		
		return row_count
		
	def commit(self):
		"""
		提交
		"""
		self.myconnection.commit()
		self.myconnection.set_autocommit(True)
		
	def rollback(self):
		"""
		回滚
		"""
		self.myconnection.rollback()
		self.myconnection.set_autocommit(True)
		
	def updateCursor(self):
		"""
		更新
		"""
		if not self.cursor:
			self.cursor = self.myconnection.cursor()