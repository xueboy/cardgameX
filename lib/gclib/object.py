#coding:utf-8
#!/usr/bin/env python

from gclib.DBConnection import DBConnection
import gclib.gcjson



class object():
	
	
	def install(self):
		return 0
		
		
	def get(self, id):
		conn = DBconnection.getConnection()
		res = conn.query("SELECT * FROM " + self.__class__.__name__ + " WHERE id = %d", id)
		if len(res) == 1:
			load(gcjson.loads(id, res[0][2]))
		return
		
		
	def delete(self):
		conn = DBconnection.getConnection()
		res = conn.query("DELETE FROM " + self.__class__.__name__ + " WHERE id = %d", self.id)
		if len(res) == 1:
			load(gcjson.loads(res[0][2]))
		return
		
		
	def getdata(self):
		return [0]
	
	
	def load(self, id, data):
		
		
		
		return 0
		
		
	def save(self):
		return 0
		
		
		
		
	
		