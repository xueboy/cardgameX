﻿from gclib.DBConnection import DBConnection
from gclib.json import json


class DBPersistent:
	
	@staticmethod
	def install(obj, roleid):
		conn = DBConnection.getConnection()
		conn.excute("INSERT INTO " + self.__class__.__name__ + "(roleid, object) VALUES (%s, %s)", [roleid, json.dumps(self.getData())])
		self.id = conn.insert_id()
		self.roleid = roleid
		return self.id
		
	@staticmethod		
	def get(tp, roleid):
		conn = DBConnection.getConnection()		
		res = conn.query("SELECT * FROM " + tp.__name__ + " WHERE roleid = %s", [roleid])
		if len(res) == 1:
			obj = tp()
			obj.id = res[0][0]
			obj.roleid = res[0][1]			
			obj.load(roleid, json.loads(res[0][2]))
			i = 0			
			for column in obj.extend_columns:
				setattr(obj, column, res[0][3 + i])
				i = i + 1
			return obj
		return None
		
	@staticmethod		
	def save(obj):
		conn = DBConnection.getConnection()
		data = obj.getData()
		dumpstr = json.dumps(data)
		update_columns = ['object = %s']
		update_value = [dumpstr]
		for column in obj.extend_columns:
			update_columns.append(column + ' = %s')
			update_value.append(getattr(obj, column))
		update_value.append(obj.id)		
		sql = "UPDATE " + obj.__class__.__name__ + " SET " + ', '.join(update_columns) + " WHERE id = %s"			
		conn.excute(sql, update_value)
				
		
	def delete(obj):
		conn = DBconnection.getConnection()
		conn.excute("DELETE FROM " + self.__class__.__name__ + " WHERE id = %s", [self.id])		
		return		