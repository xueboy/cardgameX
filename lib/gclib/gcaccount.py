#coding:utf-8
#!/usr/bin/env python
from gclib.gcjson import gcjson
from gclib.object import object
from gclib.DBConnection import DBConnection
from gclib.gcuser import gcuser
from gclib.utility import currentTime
import time


class gcaccount(object):
	@classmethod
	def login(cls,usrname, password):
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM account WHERE username = %s AND passward = %s", [usrname, password])
		if len(res) == 1:
			acc = cls.accountObject()
			acc.id = res[0][0]
			acc.username = res[0][1]			
			acc.roleid = res[0][3]
			acc.opendid = res[0][4]
			acc.saveLogin()
			return acc
		return None
			
	def getUser(self):
		
		if self.roleid == 0:
			return self.makeUser()
					
		conn = DBConnection.getConnection()				
		res = conn.query("SELECT * FROM user WHERE id = %s", [self.roleid])
		if len(res) == 1:
			usr = self.userObject()
			usr.init(self)		
			usr.load(self.roleid, gcjson.loads(res[0][2]))
			usr.id = self.roleid
			usr.last_login = self.last_login
			return usr
		else:
			return self.makeUser()
	
	def makeUser(self):
		conn = DBConnection.getConnection()		
		usr = self.userObject()
		usr.init(self)
		usr.last_login = self.last_login
		usr.install(0)
		self.roleid = usr.id
		self.saveRoleId()	
		usr.saveRoleId()	
		return usr
		
	def userObject(self):
		"""
		Must overwrite in subclass and return the subclass of gcuser object
		"""
		return None
	
	@classmethod 
	def accountObject():
		"""
		Must implement in subclass and return the subclass of gcaccount object
		"""
		return None
		
		
	def saveRoleId(self):
		conn = DBConnection.getConnection()				
		conn.excute("UPDATE account SET roleid = %s WHERE id = %s", [self.roleid, self.id])		
		
	def saveLogin(self):
		self.last_login = currentTime()
		conn = DBConnection.getConnection()				
		conn.excute("UPDATE account SET lastlogin = %s WHERE id = %s", [time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(self.last_login)), self.id])
		
	@staticmethod
	def getRoleid(name):
		conn = DBConnection.getConnection()				
		res = conn.query("SELECT * FROM account WHERE username = %s", name)
		if len(res) == 1:
			return res[0][3]
		return 0
		
		