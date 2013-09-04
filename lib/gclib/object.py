#coding:utf-8
#!/usr/bin/env python

from gclib.DBConnection import DBConnection
from gclib.gcjson import gcjson



class object():
	"""
	encapsulate data access mothed.
	"""
	
	
	def install(self):
		conn = DBconnection.getConnection()
		conn.excute("INSERT INTO " + cls.__name__ + "(roleid, object) VALUES (%s, %s)", [self.id, self.getdate()])		
		return 0
		
	@classmethod	
	def get(cls, id):
		conn = DBConnection.getConnection()		
		res = conn.query("SELECT * FROM " + cls.__name__ + " WHERE id = %s", [id])
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
		
		
	def getdata(self):
		return [0]
	
	
	def load(self, id, data):		
		return 0
		
		
	def save(self):
		conn = DBConnection.getConnection()
		data = self.getdate()
		dumpstr = gcjson.dump(data)
		conn.excute("UPDATE " + self.__class__.__name__ + " SET object = %s", [dumpstr])
		return 0
		
		
		
		
	
		