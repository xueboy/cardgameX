#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.DBConnection import DBConnection
from gclib.user import user
from gclib.utility import currentTime
import time


class account(object):
	
	def __init__(self):
		object.__init__(self)
	
	@classmethod
	def login(cls,usrname, password):
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM account WHERE email = %s AND password = %s", [usrname, password])
		if len(res) == 1:
			acc = cls.accountObject()
			acc.id = res[0][0]
			acc.username = res[0][1]
			acc.nickname = res[0][3]		
			acc.roleid = res[0][4]
			acc.opendid = res[0][5]
			acc.saveLogin()
			return acc
		return None
			
	def getUser(self):
		
		if self.roleid == 0:
			return self.makeUser()
		print self.roleid
		return self.userObject().get(self.roleid)
	
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
	def new(cls, accountName, password):
		sql = "INSERT INTO account (email, password) VALUES (%s, %s)"
		conn = DBConnection.getConnection()
		conn.excute(sql, [accountName, password])
		
		acc = cls.accountObject()
		acc.id = conn.insert_id()
		acc.username = accountName
		acc.nickname = ''
		acc.roleid = 0
		acc.opendid = 0
		acc.saveLogin()
	
	@classmethod 
	def accountObject(cls):
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
		res = conn.query("SELECT * FROM account WHERE nickname = %s", [name])
		if len(res) == 1:
			return res[0][4]
		return 0