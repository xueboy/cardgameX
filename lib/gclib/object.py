#coding:utf-8
#!/usr/bin/env python

from django.conf import settings
from gclib.DBPersistent import DBPersistent
from gclib.json import json
from gclib.persistable import persistable




class object(persistable):
	
	def __init__(self):
		"""
		构造函数
		"""
		persistable.__init__(self)
		self.id = 0
		self.roleid = 0
		self.__needSave = False
		
	
	def install(self, roleid):
		"""
		安装
		"""
		return DBPersistent.installObject(self, roleid)
		
	@classmethod	
	def get(cls, roleid):
		"""
		得到
		"""
		return DBPersistent.getObject(cls, roleid)
		
		
	def delete(self):
		"""
		删除
		"""
		return DBPersistent.delete(self)
		
	def getData(self):
		"""
		得到数据
		"""
		return {}	
	
	def load(self, roleid, data):
		"""
		加载
		"""
		self.roleid = roleid
		return 0
		
	def save(self):
		"""
		保存
		"""
		#return DBPersistent.save(self)
		self.__needSave = True
		self.do_save()
		
	def do_save(self):
		"""
		保存
		"""
		if self.__needSave:
			return DBPersistent.saveObject(self)
		
		
	@classmethod
	def syncdb(cls):
		"""
		保存数据库
		"""
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
