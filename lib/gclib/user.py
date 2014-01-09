#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.DBConnection import DBConnection

class user(object):	
	
	def __init__(self):
		object.__init__(self)
		self.account = None
		self.accountid = 0
	
	def init(self, acc):
		self.id = 0
		self.account = acc
		self.accountid = acc.id
		return
			
	def install(self, roleid):
		object.install(self, roleid)
		
	def onInit(self):
		pass		
	
	def load(self, roleid, data):
		object.load(self, roleid, data)
		self.accountid = data['accountid']
		
	def getData(self):
		data = object.getData(self)
		data['accountid'] = self.accountid
		return data

		
	def update(self):
		return
		
	def saveRoleId(self):
		conn = DBConnection.getConnection()		
		self.roleid = self.id
		conn.excute('UPDATE user SET roleid = %s WHERE id = %s', [self.roleid, self.id])	
		
	def onLogin(self):
		pass
		
	def getClientData(self):
		pass		
		
	def delete(self):
		object.delete(self)
		conn = DBConnection.getConnection()
		if self.accountid:
			conn.excute('UPDATE account SET roleid = 0 ,nickname = Null, gender = Null, openid = "0", lastlogin = Null, longitude = Null, latitude = Null WHERE id=%s', [self.accountid])
	
		