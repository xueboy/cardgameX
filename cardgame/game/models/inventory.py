#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from game.utility.config import config
from game.game_def import serverid
from gclib.utility import currentTime
import time

class inventory(object):
	
	def __init__(self):
		object.__init__(self)
		self.card = []
		self.team = ['', '', '', '', '', '']
		self.equipment = []
		self.user = None
		
	def init(self):
		return
		
		
	def getData(self):
		data = {}
		data['card'] = self.card
		data['team'] = self.team
		data['equipment'] = self.equipment
		return data
		
	def getClientData(self):
		data = {}
		data['card'] = self.card
		data['team'] = self.team
		data['equipment'] = self.equipment
		return data
		
	def load(self, roleid, data):
		self.roleid = roleid
		self.card = data['card']
		self.team = data['team']
		self.equipment = data['equipment']
		
	def addCard(self, card_id, level = 1):
		cardconf = config.getConfig('pet')				
		if cardconf.has_key(card_id):
			data = {}
			data['cardid'] = card_id
			data['id'] = self.generateCardName()
			data['level'] = level
			data['exp'] = 0	
			data['strength'] = cardconf[card_id]['strength']
			data['intelligence'] = cardconf[card_id]['intelligence']
			data['artifice'] = cardconf[card_id]['artifice']
			self.card.append(data)			
			return data
		return None
		
	def delCard(self, id):
		if self.team.count (id) > 0:
			return 0
		self.card = filter(lambda c : c['id'] == id, self.card)		
		return 1	
	
	def addEquipment(self, id):
		equipmentconf = config.getConfig('equipment')
		if equipmentconf.has_key(id):
			data = {}
			data['equipmentid'] = id
			data['id'] = self.generateEquipmentName()
			data['level'] = 1
			self.equipment.append(data)
			return data
		return None
		
	def deleteEquipment(self, id):
		self.equipment = filter(lambda e : e['id'] == id, self.equipment)		
		return 1
	
	def generateCardName(self):
		return self.generateName('C')
		
	def generateEquipmentName(self):
		return self.generateName('E')
	
	def generateName(self, perfix):
		serveridLen = len(str(serverid))
		roleidLen = len(str(self.roleid))
		tm = time.gmtime(currentTime())
		ts = time.strftime('%Y%m%d%H%M%S', tm)
		no = self.user.getCardNo()		
		noLen = len(str(no))
		name = ''.join([perfix, str(serveridLen), str(serverid), str(roleidLen), str(self.roleid), ts, str(noLen), str(no)])
		return name
		
	def getCard(self, cardid):
		for card in self.card:			
			if card['id'] == cardid:
				return card
		return None
	
	def setTeam(self, cardid1, cardid2, cardid3, cardid4, cardid5, cardid6):
		
		if cardid1 != '':
			if cardid1 == cardid2 or cardid1 == cardid3 or cardid1 == cardid4 or cardid1 == cardid5 or cardid1 == cardid6:
				return self.team			
		if cardid2 != '':
			if cardid2 == cardid3 or cardid2 == cardid4 or cardid2 == cardid5 or cardid2 == cardid6:
				return self.team			
		if cardid3 != '':
			if cardid3 == cardid4 or cardid3 == cardid5 or cardid3 == cardid6:
				return self.team			
		if cardid4 != '':
			if cardid4 == cardid5 or cardid4 == cardid6:
				return self.team
		if cardid5 != '':
			if cardid5 == cardid6:
				return self.team
		
		if cardid1 == '':
			self.team[0] = ''
		else:
			self.team[0] = self.getCard(cardid1)['id']
		if cardid2 == '':
			self.team[1] = ''
		else:
			self.team[1] = self.getCard(cardid2)['id']
		if cardid3 == '':
			self.team[2] = ''
		else:
			self.team[2] = self.getCard(cardid3)['id']
		if cardid4 == '':
			self.team[3] = ''
		else:
			self.team[3] = self.getCard(cardid4)['id']		
		if cardid5 =='':
			self.team[4] = ''
		else:
			self.team[4] = self.getCard(cardid5)['id']
		if cardid6 == '':
			self.team[5] = ''
		else: 
			self.team[5] = self.getCard(cardid6)['id']
		return self.team

		