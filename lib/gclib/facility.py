#coding:utf-8
#!/usr/bin/env python

from gclib.cache import cache


class facility():
	
	def __init__(self):
		self.id = 0
		
	
	def install(self, name):
		return DBPersistent.installFacility(self, name)
		
	@classmethod	
	def get(cls, name):		
		return DBPersistent.getFacility(cls, name)
		
		
	def delete(self):
		return DBPersistent.delete(self)
		
	def getData(self):
		return {}	
	
	def load(self, roleid, data):
		self.roleid = roleid
		return 0
		
		
	def save(self):
		return DBPersistent.save(self)
	

		
	@classmethod
	def syncdb(cls):
		"""
		create database table related object
		this function use to call in manage.py
		"""
		sql = "CREATE TABLE `" + cls.__name__ +"""` (
  					`id` BIGINT NOT NULL AUTO_INCREMENT,
  					`name` VARCHAR NOT NULL,
  					`object` TEXT NOT NULL,
  					PRIMARY KEY (`id`));
  				"""
		conn = DBconnection.getConnection()
		conn.excute(sql, [])

