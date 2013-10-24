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
		#conn = DBConnection.getConnection()
		#conn.excute("INSERT INTO " + self.__class__.__name__ + "(roleid, object) VALUES (%s, %s)", [roleid, json.dumps(self.getData())])
		#self.id = conn.insert_id()
		#self.roleid = roleid
		#return self.id
		
	@classmethod	
	def get(cls, roleid):
		return DBPersistent.get(cls, roleid)
		#conn = DBConnection.getConnection()		
		#res = conn.query("SELECT * FROM " + cls.__name__ + " WHERE roleid = %s", [roleid])
		#if len(res) == 1:
		#	obj = cls()
		#	obj.id = res[0][0]
		#	obj.roleid = res[0][1]			
		#	obj.load(roleid, json.loads(res[0][2]))
		#	i = 0			
		#	for column in obj.extend_columns:
		#		setattr(obj, column, res[0][3 + i])
		#		i = i + 1
		#	return obj
		#return None
		
		
	def delete(self):
		return DBPersistent.delete(self)
		#conn = DBconnection.getConnection()
		#conn.excute("DELETE FROM " + self.__class__.__name__ + " WHERE id = %s", [self.id])		
		#return		
		
	def getData(self):
		return {}	
	
	def load(self, roleid, data):
		self.roleid = roleid
		return 0
		
	def save(self):
		return DBPersistent.save(self)
		#conn = DBConnection.getConnection()
		#data = self.getData()
		#dumpstr = json.dumps(data)
		#update_columns = ['object = %s']
		#update_value = [dumpstr]
		#for column in self.extend_columns:
		#	update_columns.append(column + ' = %s')
		#	update_value.append(getattr(self, column))
		#update_value.append(self.id)		
		#sql = "UPDATE " + self.__class__.__name__ + " SET " + ', '.join(update_columns) + " WHERE id = %s"			
		#conn.excute(sql, update_value)
		#return 0
	
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
