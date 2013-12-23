#coding:utf-8
#!/usr/bin/env python

from gclib.account import account as gcaccount
from gclib.DBConnection import DBConnection
from game.models.user import user


class account(gcaccount):		
		
	@classmethod 
	def accountObject(cls):
		return account()
		
	def userObject(self):
		return user()
	
	def userCls(self):
		return user
	
	def __init__(self):
		gcaccount.__init__(self)
		
	def load(self, roleid, data):
		gcaccount.load(self, roleid, data)
	
	def install(self, roleid):
		gcaccount.install(self, roleid)
		
	@staticmethod
	def locate(accountid, longitude, latitude):
		sql = 'UPDATE account SET longitude = %s, latitude = %s WHERE id=%s'
		
		conn = DBConnection.getConnection()
		conn.excute(sql, [longitude, latitude, accountid])
	
	@staticmethod	
	def getRange(minLng, maxLng, minLat, maxLat):
		sql = 'SELECT roleid, longitude, latitude FROM account WHERE longitude > %s and longitude < %s and latitude > %s and latitude < %s limit %s'
		conn = DBConnection.getConnection()
		return conn.query(sql, [minLng, maxLng, minLat, maxLat, 50])