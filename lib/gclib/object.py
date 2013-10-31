#coding:utf-8
#!/usr/bin/env python

from django.conf import settings
from gclib.DBPersistent import DBPersistent
from gclib.json import json




class object():
	"""
	encapsulate data access mothed.
	"""
	
	def __init__(self):
		self.id = 0
		self.roleid = 0
		self.__needSave = False
		self.extend_columns = []
	
	def install(self, roleid):
		return DBPersistent.install(self, roleid)
		
	@classmethod	
	def get(cls, roleid):
		return DBPersistent.get(cls, roleid)
		
		
	def delete(self):
		return DBPersistent.delete(self)
		
	def getData(self):
		return {}	
	
	def load(self, roleid, data):
		self.roleid = roleid
		return 0
		
	def save(self):
		return DBPersistent.save(self)
	
	def do_save(self):
		conn = DBConnection.getConnection()
		data = self.getData()
		dumpstr = json.dumps(data)	
		conn.excute("UPDATE " + self.__class__.__name__ + " SET object = %s WHERE id = %s", [dumpstr, self.id])
		
		
	@classmethod
	def syncdb(cls):
		"""
		create database table related object
		this function use to call in manage.py
		"""
		sql = "CREATE TABLE `" + cls.__name__ +"""` (
  					`id` BIGINT NOT NULL AUTO_INCREMENT,
  					`roleid` BIGINT NOT NULL,
  					`object` TEXT NOT NULL,
  					PRIMARY KEY (`id`));
  				"""
		conn = DBconnection.getConnection()
		conn.excute(sql, [])
