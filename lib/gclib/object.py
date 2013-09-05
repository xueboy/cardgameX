#coding:utf-8
#!/usr/bin/env python

from gclib.DBConnection import DBConnection
from gclib.gcjson import gcjson



class object():
	"""
	encapsulate data access mothed.
	"""
	
	def __init__(self):
		self.id = 0
		self.roleid = 0		
	
	def install(self, roleid):
		conn = DBConnection.getConnection()
		conn.excute("INSERT INTO " + self.__class__.__name__ + "(roleid, object) VALUES (%s, %s)", [roleid, gcjson.dumps(self.getData())])
		self.id = conn.insert_id()
		self.roleid = roleid
		return 0
		
	@classmethod	
	def get(cls, id):
		conn = DBConnection.getConnection()		
		res = conn.query("SELECT * FROM " + cls.__name__ + " WHERE roleid = %s", [id])
		if len(res) == 1:
			obj = cls()
			t = type(obj)
			obj.load(id, gcjson.loads(res[0][2]))			
			return obj		
		return None
		
		
	def delete(self):
		conn = DBconnection.getConnection()
		conn.excute("DELETE FROM " + self.__class__.__name__ + " WHERE id = %s", [self.id])		
		return		
		
	def getData(self):
		return [0]	
	
	def load(self, id, data):		
		return 0		
		
	def save(self):
		conn = DBConnection.getConnection()
		data = self.getdate()
		dumpstr = gcjson.dump(data)
		conn.excute("UPDATE " + self.__class__.__name__ + " SET object = %s", [dumpstr])
		return 0
		
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
