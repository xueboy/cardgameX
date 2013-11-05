#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from game.utility.config import config
from game.game_def import serverid
from gclib.utility import currentTime
import time
import copy
from game.routine.equipment import equipment

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
		card = []
		
		for c in self.card:
			c1 = copy.copy(c)
			if c1.has_key('slot'):
				del c1['slot']
			card.append(c1)		
		
		data['card'] = card
		data['team'] = self.team
		data['equipment'] = self.equipment
		data['slots'] = self.getSlots()
		return data
		
	def load(self, roleid, data):
		self.roleid = roleid
		self.card = data['card']
		self.team = data['team']
		self.equipment = data['equipment']
		
	def addCard(self, cardid, level = 1):
		cardconf = config.getConfig('pet')				
		if cardconf.has_key(cardid):
			data = {}
			data['cardid'] = cardid
			data['id'] = self.generateCardName()
			data['level'] = level
			data['exp'] = 0	
			data['strength'] = cardconf[cardid]['strength']
			data['intelligence'] = cardconf[cardid]['intelligence']
			data['artifice'] = cardconf[cardid]['artifice']			
			self.card.append(data)			
			return data
		return None
		
	def delCard(self, id):
		if self.team.count (id) > 0:
			return 0
		self.card = filter(lambda c : c['id'] != id, self.card)		
		return 1	
	
	def addEquipment(self, equipmentid):
		equipmentconf = config.getConfig('equipment')
		if equipmentconf.has_key(equipmentid):
			data = {}
			data['equipmentid'] = equipmentid
			data['id'] = self.generateEquipmentName()			
			self.equipment.append(data)
			return data
		return None
		
	def depositEquipment(self, equipment):
		self.equipment.append(equipment)
		return equipment
		
	def withdrawEquipment(self, id):
		res = None
		for equipment in self.equipment:
			if equipment['id'] == id:
				res = equipment
				self.equipment.remove(equipment)
		return res
	
		
	def delEquipment(self, id):
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
		
	def getCard(self, id):
		for card in self.card:			
			if card['id'] == id:
				return card
		return None	
	
		
	def getEquipment(self, id):
		for equipment in self.equipment:
			if equipment['id'] == id:
				return equipment
		return None
		
	def getSlots(self):
		slots = {}
		i = 1
		for t in self.team:
			if t:
				tc = self.getCard(t)
				slots['t' + str(i)] = tc['slot']
			else: 
				slots['t' + str(i)] = [{}, {}, {}, {}, {}]
			i = i + 1
		return slots
	
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
		
		usr = self.user
		
		if cardid1 == '':
			equipment.takeoff(usr, self.team[0])
			self.team[0] = ''
		else:
			card1 = self.getCard(cardid1)
			equipment.give(usr, self.team[0], card1)
			self.team[0] = card1['id']
		if cardid2 == '':
			equipment.takeoff(usr, self.team[1])
			self.team[1] = ''
		else:
			card2 = self.getCard(cardid2)
			equipment.give(usr, self.team[1], card2)
			self.team[1] = card2['id']
		if cardid3 == '':
			equipment.takeoff(usr, self.team[2])
			self.team[2] = ''
		else:
			card3 = self.getCard(cardid3)
			equipment.give(usr, self.team[2], card3)
			self.team[2] = card3['id']
		if cardid4 == '':
			equipment.takeoff(usr, self.team[3])
			self.team[3] = ''
		else:
			card4 =  self.getCard(cardid4)
			equipment.give(usr, self.team[3], card4)
			self.team[3] = card4['id']
		if cardid5 =='':
			equipment.takeoff(usr, self.team[4])
			self.team[4] = ''
		else:
			card5 = self.getCard(cardid5)
			equipment.give(usr, self.team[4], cardid5)
			self.team[4] = card5['id']
		if cardid6 == '':
			equipment.takeoff(usr, self.team[5])
			self.team[5] = ''
		else: 
			card6 = self.getCard(cardid6)
			equipment.give(usr, self.team[5], cardid6)
			self.team[5] = cardid6['id']
			
		self.save()
		return self.team

		