#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.DBConnection import DBConnection

class user(object):	
	
	def __init__(self):
		object.__init__(self)
	
	def init(self, acc):
		self.id = 0
		return
		
	def onInit(self):
		pass
		
		
	def update(self):
		return
		
	def saveRoleId(self):
		conn = DBConnection.getConnection()		
		self.roleid = self.id
		conn.excute("UPDATE user SET roleid = %s WHERE id = %s", [self.roleid, self.id])		
		
	
		
	def onLogin(self):
		pass
		
	def getClientData(self):
		pass