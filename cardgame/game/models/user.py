#coding:utf-8
#!/usr/bin/env python

from gclib.gcuser import gcuser

class user(gcuser):
	def init(self, acc):
		self.id = acc.roleid
		self.name = acc.username
		self.level = 1
		self.stamina = 100
		self.gems = 0
		self.gold = 0
		self.exp = 0
		self.vipLevel = 1
		
	
	def getdata(self):	
		data = {}
		data['name'] = self.name
		data['level'] = self.level
		data['stamina'] = self.stamina
		data['gems'] = self.gems
		data['gold'] = self.gold
		data['exp'] = self.exp
		data['vipLevel'] = self.vipLevel
		return data
		
		
	def load(self, id, data):
		self.name = data['name']
		self.level = data['level']
		self.stamina = data['stamina']
		self.gems = data['gems']
		self.gold = data['gold']
		self.exp = data['exp']
		self.vipLevel = data['vipLevel']
		
		
