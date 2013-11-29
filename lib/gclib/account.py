#coding:utf-8
#!/usr/bin/env python

import time
from django.db import IntegrityError
from gclib.object import object
from gclib.DBConnection import DBConnection
from gclib.user import user
from gclib.utility import currentTime
from gclib.exception import NotImplemented

class account(object):
	
	def __init__(self):
		object.__init__(self)
	
	@classmethod
	def login(cls,usrname, password):
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM account WHERE accountname = %s AND password = %s", [usrname, password])
		if len(res) == 1:
			acc = cls.accountObject()
			acc.id = res[0][0]
			acc.username = res[0][1]
			acc.nickname = res[0][3]
			acc.gender = res[0][4]
			acc.roleid = res[0][5]
			acc.opendid = res[0][6]
			acc.saveLogin()
			return acc
		return None
			
	def getUser(self):		
		return self.userObject().get(self.roleid)
	
	def makeUserAndBind(self, nickname, gender):
		conn = DBConnection.getConnection()		
		usr = self.userObject()
		usr.init(self)
		usr.last_login = self.last_login
		usr.name = nickname
		usr.gender = gender
		usr.install(0)
		self.roleid = usr.id
		self.bind(usr.id, nickname, gender)	
		usr.saveRoleId()
		usr.onInit()
		return usr
		
	def userObject(self):
		"""
		Must overwrite in subclass and return the subclass of gcuser object
		"""
		return None
	
	@classmethod	
	def get(cls, accid):
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM account WHERE id = %s ", [accid])
		if len(res) == 1:
			acc = cls.accountObject()
			acc.id = res[0][0]
			acc.username = res[0][1]
			acc.nickname = res[0][3]
			acc.gender = res[0][4]		
			acc.roleid = res[0][5]
			acc.opendid = res[0][6]
			acc.saveLogin()
			return acc
		return None
		
	def save(self):
		raise NotImplemented
	
	@staticmethod
	def load(self, roleid, data):
		object.laod(self, roleid, data)
	
	
	@classmethod
	def new(cls, accountName, password):
		try:
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
		except IntegrityError:
			return {'msg':'account_already_exist'}
				
		return {'account_name':accountName}
	
	@classmethod 
	def accountObject(cls):
		"""
		Must implement in subclass and return the subclass of gcaccount object
		"""
		return None
		
		
	def bind(self, roleid, nickname, gender):
		conn = DBConnection.getConnection()
		conn.excute("UPDATE account SET roleid = %s, nickname = %s, gender = %s WHERE id = %s", [roleid, nickname, gender, self.id])
		
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
	
	def onLogin(self):
		pass