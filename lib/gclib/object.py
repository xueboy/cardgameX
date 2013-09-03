#coding:utf-8
#!/usr/bin/env python

from gclib.DBConnection import DBConnection
from gclib.gcjson import gcjson



class object():
	
	
	def install(self):
		return 0
		
	@classmethod	
	def get(cls, id):
		conn = DBConnection.getConnection()		
		res = conn.query("SELECT * FROM " + cls.__name__ + " WHERE id = %s", [id])
		if len(res) == 1:
			obj = cls()
			t = type(obj)
			obj.load(id, gcjson.loads(res[0][1]))
			return obj
		
		return None
		
		
	def delete(self):
		conn = DBconnection.getConnection()
		res = conn.query("DELETE FROM " + self.__class__.__name__ + " WHERE id = %s", [self.id])
		if len(res) == 1:
			load(gcjson.loads(res[0][2]))
		return
		
		
	def getdata(self):
		return [0]
	
	
	def load(self, id, data):		
		return 0
		
		
	def save(self):
		return 0
		
		
		
		
	
		