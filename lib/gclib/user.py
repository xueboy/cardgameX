#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.DBConnection import DBConnection

class user(object):	
	
	def __init__(self):
		"""
		构造函数
		"""
		object.__init__(self)
		self.accountid = 0
	
	def init(self, acc):
		"""
		初始化
		"""
		self.id = 0
		if acc:			
			self.accountid = acc.id
		return
			
	def install(self, roleid):
		"""
		安装
		"""
		object.install(self, roleid)
		
	def onInit(self):
		"""
		初始化
		"""
		pass		
	
	def load(self, roleid, data):
		"""
		加载
		"""
		object.load(self, roleid, data)
		self.accountid = data['accountid']
		
	def getData(self):
		"""
		得到数据
		"""
		data = object.getData(self)
		data['accountid'] = self.accountid
		return data

		
	def update(self):
		"""
		更新
		"""
		return
		
	def saveRoleId(self):
		"""
		保存roleid
		"""
		conn = DBConnection.getConnection()		
		self.roleid = self.id
		conn.excute('UPDATE user SET roleid = %s WHERE id = %s', [self.roleid, self.id])	
		
	def onLogin(self):
		"""
		登陆
		"""
		pass
		
	def getClientData(self):
		"""
		得到client data
		"""
		pass		
		
	def delete(self):
		"""
		删除
		"""
		object.delete(self)
		conn = DBConnection.getConnection()
		if self.accountid:
			conn.excute('UPDATE account SET roleid = 0 ,nickname = Null, gender = Null, openid = "0", lastlogin = Null, longitude = Null, latitude = Null WHERE id=%s', [self.accountid])
	
		