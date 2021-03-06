﻿#coding:utf-8
#!/usr/bin/env python

import time
from django.db import IntegrityError
from gclib.object import object
from gclib.DBConnection import DBConnection
from gclib.user import user
from gclib.utility import currentTime
from gclib.exception import NotImplemented, DuplicateNickname

class account(object):
	
	def __init__(self):
		"""
		构造函数
		"""
		object.__init__(self)
	
	@classmethod
	def login(cls,usrname, password):
		"""
		登入
		"""
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM account WHERE accountname = %s AND password = %s", [usrname, password])
		if len(res) == 1:
			acc = cls.accountObject()
			acc.id = res[0][0]
			acc.username = res[0][1]
			acc.nickname = res[0][3]
			acc.gender = res[0][4]
			acc.roleid = res[0][5]
			acc.openid = res[0][6]
			acc.longitude = res[0][8]
			acc.latitude = res[0][9]
			acc.saveLogin()
			return acc
		return None
				
	def install(self, roleid):
		"""
		安装
		"""
		object.install(self, roleid)
		
	def getUser(self):
		"""
		得到用户
		"""
		usr = self.userCls().get(self.roleid)
		if not usr:
			return None	
		return usr
	
	def makeUserAndBind(self, nickname, avatar, gender):		
		usr = self.userObject()
		usr.init(self)
		usr.last_login = self.last_login
		usr.name = nickname
		usr.gender = gender
		usr.avatar = avatar		
		usr.install(0)
		self.roleid = usr.id
		try:
			self.bind(usr.id, nickname, gender)
		except:
			usr.delete()
			raise
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
		"""
		拿取帐号
		"""
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM account WHERE id = %s ", [accid])
		if len(res) == 1:
			acc = cls.accountObject()
			acc.id = res[0][0]
			acc.username = res[0][1]
			acc.nickname = res[0][3]
			acc.gender = res[0][4]		
			acc.roleid = res[0][5]
			acc.openid = res[0][6]			
			acc.saveLogin()
			return acc
		return None
	
	@classmethod
	def get_by_account_name(cls, name)	:
		"""
		拿取帐号名
		"""
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM account WHERE accountname = %s ", [name])
		if len(res) == 1:
			acc = cls.accountObject()
			acc.id = res[0][0]
			acc.username = res[0][1]
			acc.nickname = res[0][3]
			acc.gender = res[0][4]		
			acc.roleid = res[0][5]
			acc.openid = res[0][6]			
			return acc
		return None
	
	def save(self):
		"""
		保存
		"""
		raise NotImplemented
	
	@staticmethod
	def load(self, roleid, data):
		"""
		读取
		"""
		object.laod(self, roleid, data)
	
	
	@classmethod
	def new(cls, accountName, password):
		"""
		新帐号
		"""
		try:
			sql = "INSERT INTO account (accountname, password) VALUES (%s, %s)"
			conn = DBConnection.getConnection()
			conn.excute(sql, [accountName, password])
		
			acc = cls.accountObject()
			acc.id = conn.insert_id()
			acc.username = accountName
			acc.nickname = ''
			acc.roleid = 0
			acc.openid = 0
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
		"""
		绑定roleid
		"""
		try:
			conn = DBConnection.getConnection()
			conn.excute("UPDATE account SET roleid = %s, nickname = %s, gender = %s WHERE id = %s", [roleid, nickname, gender, self.id])
		except IntegrityError:
			raise DuplicateNickname
		
	def saveLogin(self):
		"""
		保存登入
		"""
		self.last_login = currentTime()
		conn = DBConnection.getConnection()
		conn.excute("UPDATE account SET lastlogin = %s WHERE id = %s", [time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(self.last_login)), self.id])
		
	@staticmethod
	def getRoleid(name):
		"""
		得到roleid
		"""
		conn = DBConnection.getConnection()				
		res = conn.query("SELECT * FROM account WHERE nickname = %s", [name])
		if len(res) == 1:
			return res[0][5]
		return 0
	
	def onLogin(self):
		pass