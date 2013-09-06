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
		self.last_card_no = 0
		self.leader = {}
		self.friends = {}
		
	
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
		data['last_card_no'] = self.last_card_no
		data['last_login'] = self.last_login
		data['friend_request'] = self.friend_request
		data['leader'] = self.leader
		data['friends'] = self.friends
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
		data['friend_request'] = self.friend_request
		data['friends'] = self.friends
		return data
		
		
	def load(self, roleid, data):
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
		if not data.has_key('last_card_no'):
			data['last_card_no'] = 0
		self.last_card_no = data['last_card_no']
		if not data.has_key('last_login'):
			data['last_login'] = currentTime()
		self.last_login = data['last_login']
		if not data.has_key('friend_request'):
			data['friend_request'] = {}
		self.friend_request = data['friend_request']
		if not data.has_key('leader'):
			data['leader'] = ''
		self.leader = data['leader']
		if not data.has_key('friends'):
			data['friends'] = {}
		self.friends = data['friends']
			
		
	def getCardNo(self):
		self.last_card_no = self.last_card_no + 1
		return self.last_card_no		
		
	def getDungeon(self):				
		dun = dungeon.get(self.id)
		if dun == None:			
			dun = dungeon()
			dun.install(self.roleid)
		dun.user = self
		return dun
	
	
	def getInventory(self):
		if self.id == 0:
			raise "error"
		inv = inventory.get(self.id)
		if inv == None:			
			inv = inventory()
			inv.install(self.roleid)
		inv.user = self
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
		
			
	def addFriendRequest(self, requestRoleid, requestData):
		self.friend_request[requestRoleid] = requestData
		
	def confirmFriendRequest(self, friend, isConfirm):
		if isConfirm != 0:
			self.addFriend(friend)
			friend.addFriend(self)
			self.save()
			friend.save()			
		else:
			del self.friend_request[friend.roleid]
			self.save()			
	
	def addFreind(self, friend):
		self.friends[friend.roleid] =  {'name': friend.name, 'level': friend.level, 'last_login': friend.last_login, 'leader': friend.leader}
			
		
		