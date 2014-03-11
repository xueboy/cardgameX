#coding:utf-8
#!/usr/bin/env python

from gclib.account import account as gcaccount
from gclib.DBConnection import DBConnection
from game.models.user import user


class account(gcaccount):		
		
	@classmethod 
	def accountObject(cls):
		"""
		帐号对象
		"""
		return account()
		
	def userObject(self):
		"""
		玩家对象
		"""
		return user()
	
	def userCls(self):
		"""
		玩家类别
		"""
		return user
	
	def __init__(self):
		"""
		构造函数
		"""
		gcaccount.__init__(self)
		
	def load(self, roleid, data):
		"""
		加载
		"""
		gcaccount.load(self, roleid, data)
	
	def install(self, roleid):
		"""
		安装
		"""
		gcaccount.install(self, roleid)
		
	@staticmethod
	def locate(accountid, longitude, latitude):
		"""
		定位
		"""
		sql = 'UPDATE account SET longitude = %s, latitude = %s WHERE id=%s'
		
		conn = DBConnection.getConnection()
		conn.excute(sql, [longitude, latitude, accountid])
	
	@staticmethod	
	def getRange(minLng, maxLng, minLat, maxLat, cnt):
		"""
		得到天梯
		"""
		sql = 'SELECT roleid, longitude, latitude FROM account WHERE longitude >= %s and longitude <= %s and latitude >= %s and latitude <= %s limit %s'
		conn = DBConnection.getConnection()
		return conn.query(sql, [minLng, maxLng, minLat, maxLat, cnt])