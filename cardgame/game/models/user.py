#coding:utf-8
#!/usr/bin/env python

from gclib.gcuser import gcuser
from game.models.dungeon import dungeon
from game.models.inventory import inventory
from gclib.utility import currentTime
from game.utility.config import config

class user(gcuser):
	def init(self, acc):
		gcuser.init(self, acc)
		self.id = acc.roleid
		self.roleid = acc.roleid
		self.name = acc.username
		self.level = 1
		self.stamina = 100
		self.gems = 0
		self.gold = 0
		self.exp = 0
		self.vipLevel = 1
		self.stamina_last_recover = currentTime()
		
	
	def getData(self):	
		data = {}
		data['name'] = self.name
		data['level'] = self.level
		data['stamina'] = self.stamina
		data['gems'] = self.gems
		data['gold'] = self.gold
		data['exp'] = self.exp
		data['vipLevel'] = self.vipLevel
		data['stamina_last_recover'] = self.stamina_last_recover
		return data
		
	def getClientData(self):
		data = {}
		data['name'] = self.name
		data['level'] = self.level
		data['stamina'] = self.stamina
		data['gems'] = self.gems
		data['gold'] = self.gold
		data['exp'] = self.exp
		data['vipLevel'] = self.vipLevel
		data['stamina_last_recover_before'] = currentTime() - self.stamina_last_recover
		return data
		
		
	def load(self, id, data):
		self.name = data['name']
		self.level = data['level']
		self.stamina = data['stamina']
		self.gems = data['gems']
		self.gold = data['gold']
		self.exp = data['exp']
		self.vipLevel = data['vipLevel']
		if not data.has_key('stamina_last_recover'):
			data['stamina_last_recover'] = currentTime()
		self.stamina_last_recover = data['stamina_last_recover']
		
	
		
		
	def getDungeon(self):				
		dun = dungeon.get(self.roleid)
		if dun == None:			
			dun = dungeon()
			dun.install(self.roleid)
		return dun
	
	
	def getInventory(self):
		inv = inventory.get(self.roleid)
		if inv == None:			
			inv = inventory()
			inv.install(self.roleid)
		return inv
	
	def updateStamina(self):
		maxStamina = config.getMaxStamina(self.level)
		stamina_recover_before = currentTime() - self.stamina_last_recover
		stamina_recove_interval = config.getConfig('game')['statmina_recove_interval']
		if maxStamina > self.stamina and stamina_recover_before > stamina_recove_interval:
			point = stamina_recover_before // stamina_recove_interval
			self.stamina_last_recover += point * stamina_recove_interval
			self.stamina += point
			if self.stamina > maxStamina:
				self.stamina = maxStamina
			
	def update(self):
		return
		
	def costStamina(self, point):
		maxStamina = config.getMaxStamina(sefl.level)
		if maxStamina == self.stamina:
			self.stamina_last_recover = currentTime()
		self.stamina -= point
		
			
		