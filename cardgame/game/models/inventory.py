#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from game.utility.config import config
from game.game_def import serverid
from gclib.utility import currentTime
import time
import copy
from game.routine.equipment import equipment
from game.routine.stone import stone

class inventory(object):
	
	def __init__(self):
		object.__init__(self)
		self.card = []
		self.team = ['', '', '', '', '', '']	
		self.equipment = []
		self.stone = []		
		self.user = None
		
	def init(self):
		return
		
		
	def getData(self):
		data = {}
		data['card'] = self.card
		data['team'] = self.team
		data['equipment'] = self.equipment
		data['stone'] = self.stone		
		return data
		
	def getClientData(self):
		data = {}		
		card = []
		
		for c in self.card:
			c1 = c.copy()
			if c1.has_key('slot'):
				del c1['slot']
			if c1.has_key('st_slot'):
				del c1['st_slot']
			card.append(c1)		
		
		data['card'] = card
		data['team'] = self.team
		data['equipment'] = self.equipment
		data['slots'] = self.getSlots()
		data['st_slots'] = self.getStSlots()
		data['stone'] = self.stone	
		return data
		
	def load(self, roleid, data):
		self.roleid = roleid
		self.card = data['card']
		self.team = data['team']
		self.equipment = data['equipment']
		self.stone = data['stone']		
		
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
	
	def generateStoneName(self):
		return self.generateName('S')
	
	def generateName(self, perfix):
		serveridLen = len(str(serverid))
		roleidLen = len(str(self.roleid))
		tm = time.gmtime(currentTime())
		ts = time.strftime('%Y%m%d%H%M%S', tm)
		no = str(self.user.getCardNo())
		noLen = len(no)
		name = ''.join([perfix, str(serveridLen), str(serverid), str(roleidLen), str(self.roleid), ts, str(noLen), no])
		self.user.save()	#save card no
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
		for i, t in enumerate(self.team):
			if t:
				tc = self.getCard(t)
				slots['t' + str(i)] = tc['slot']
			else: 
				slots['t' + str(i)] = equipment.make_slot()
			i = i + 1
		return slots
		
	def getStSlots(self):
		st_slots = {}
		
		for i, t in enumerate(self.team):
			if t:
				tc = self.getCard(t)
				if tc.has_key('st_slot'):
					st_slots['t' + str(i)] = tc['st_slot']
				else:
					st_slots['t' + str(i)] = stone.make_st_solt()
			else:
				st_slots['t' + str(i)] = stone.make_st_solt()
		return st_slots
	
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
				
		gameConf = config.getConfig('game')
		
		teamLevelConf = gameConf['team_member_open_level']
		
		usr = self.user
		
		if cardid1 != self.team[0] and usr.level <  teamLevelConf[0]:
			return {'msg':'level_required'}
		if cardid2 != self.team[1] and usr.level <  teamLevelConf[1]:
			return {'msg':'level_required'}
		if cardid3 != self.team[2] and usr.level <  teamLevelConf[2]:
			return {'msg':'level_required'}
		if cardid4 != self.team[3] and usr.level <  teamLevelConf[3]:
			return {'msg':'level_required'}
		if cardid5 != self.team[4] and usr.level <  teamLevelConf[4]:
			return {'msg':'level_required'}
		if cardid6 != self.team[5] and usr.level <  teamLevelConf[5]:
			return {'msg':'level_required'}	
			
		deq = []
		dst = []
		
		deq1, dst1 = self.setTeamEquipmentStone(cardid1, 0, gameConf)
		deq2, dst2 = self.setTeamEquipmentStone(cardid2, 1, gameConf)
		deq3, dst3 = self.setTeamEquipmentStone(cardid3, 2, gameConf)
		deq4, dst4 = self.setTeamEquipmentStone(cardid4, 3, gameConf)
		deq5, dst5 = self.setTeamEquipmentStone(cardid5, 4, gameConf)		
		
		deq.extend(deq1)
		deq.extend(deq2)
		deq.extend(deq3)
		deq.extend(deq4)
		deq.extend(deq5)
		
		dst.extend(dst1)
		dst.extend(dst2)
		dst.extend(dst3)
		dst.extend(dst4)
		dst.extend(dst5)		

		self.save()
		return self.team, deq, dst
	
	
	def setTeamEquipmentStone(self, cardid, teamPos, gameConf):
		dst = []
		deq = []
		if cardid:
			card = self.getCard(cardid)
			card['slot'] = equipment.make_slot()
			card['st_slot'] = stone.make_st_solt()
			if self.team[teamPos]:
				teamCard = self.getCard(self.team[teamPos])
				deq.extend(equipment.exchage(card, teamCard))
				dst.extend(stone.exchage(self, card, teamCard, gameConf))
			self.team[teamPos] = cardid
		elif self.team[teamPos]:
			teamCard = self.getCard(self.team[teamPos])
			deq.extend(equipment.takeoff(self, teamCard))
			dst.extend(stone.takeoff(self, teamCard))
			del teamCard['slot']
			del teamCard['st_slot']
			self.team[teamPos] = ''
		return deq, dst
		
	def addStone(self, stoneid):
		stoneConf = config.getConfig('stone')
		
		stoneInfo = stoneConf[stoneid]		
		st = {}
		st['stoneid'] = stoneid
		st['id'] = self.generateStoneName()
		st['level'] = 1
		st['exp'] = 0
		self.stone.append(st)
		return st
		
	def getStone(self, id):					
		for i in range(0, len(self.stone)):
			print i
			print id
			print self.stone[i]['id']
			if self.stone[i]['id'] == id:				
				return self.stone[i]
		return None
		
	def delStone(self, id):
		self.stone = filter(lambda s : s['id'] != id, self.stone)		
			
	def depositStone(self, st):
		self.stone.append(st)
		
	def withdrawStone(self, id):
		res = None
		for i, st in enumerate(self.stone):
			print st
			if st['id'] == id:
				res = st
				break
		self.stone.remove(res)
		return res
		