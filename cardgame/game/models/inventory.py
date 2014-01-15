﻿#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from game.utility.config import config
from game.game_def import serverid
from gclib.utility import currentTime
import time
from game.routine.equipment import equipment
from game.routine.stone import stone
from game.routine.skill import skill
from game.routine.pet import pet

class inventory(object):
	
	def __init__(self):
		object.__init__(self)
		self.card = []
		self.item = []
		self.team = ['', '', '', '', '', '']	
		self.equipment = []
		self.stone = []		
		self.user = None
		self.skill = []
		
	def init(self):		
		return		
		
	def install(self, roleid):
		object.install(self, roleid)
		
	def getData(self):
		data = object.getData(self)
		data['card'] = self.card
		data['item'] = self.item
		data['team'] = self.team
		data['equipment'] = self.equipment
		data['stone'] = self.stone
		data['skill'] = self.skill
		return data
		
		
	@staticmethod
	def getClientCard(card):
		data = card.copy()
		if data.has_key('slot'):
			del data['slot']
		if data.has_key('st_slot'):
			del data['st_slot']
		if data.has_key('sk_slot'):
			del data['sk_slot']
		return data
		
	def getClientData(self):
		data = {}		
		card = {}
		
		for c in self.card:			
			card[c['id']] = inventory.getClientCard(c)
		team = [{},{},{},{},{},{}]
		for i, memberid in enumerate(self.team):
			if memberid:
				cd = self.getCard(memberid)
				if cd:
					team[i] = cd
		
		equipment  = {}
		for equip in self.equipment:
			equipment[equip['id']] = equip
			
		for m in team:
			if m and m.has_key('slot'):
				for equip in m['slot']:
					if equip:
						equipment[equip['id']] = equip
						
		stone = {}
		for st in self.stone:
			stone[st['id']] = st
		
		for m in team:
			if m and m.has_key('st_slot'):
				for st in m['st_slot']:
					if st:
						stone[st['id']] = st
		
		skill = {}
		for sk in self.skill:
			skill[sk['id']]	= sk
			
		for m in team:
			if m and m.has_key('sk_slot'):
				for sk in m['sk_slot']:
					if sk:
						skill[sk['id']] = sk
					
		item = {}		
		for  it in self.item:
			item[it['id']] = it
		
		data['card'] = card
		data['team'] = self.team
		data['item'] = item
		data['equipment'] = equipment
		data['slot'] = self.getSlots()
		data['st_slot'] = self.getStSlots()
		data['sk_slot'] = self.getSkSlots()
		data['stone'] = stone
		data['skill'] = skill
		return data
		
	def load(self, roleid, data):
		object.load(self, roleid, data)
		self.card = data['card']
		self.item = data['item']
		self.team = data['team']
		self.equipment = data['equipment']
		self.stone = data['stone']
		self.skill = data['skill']
		
	def addCard(self, cardid, level = 1):
		cardConf = config.getConfig('pet')				
		if cardConf.has_key(cardid):
			card = pet.make_pet(self, cardid, level, cardConf)
			self.card.append(card)
			usr = self.user
			al = usr.getAlmanac()
			al.insert(cardid)
			return card
		return None
	
	def addAllCard(self, cardid):
		newCard = []
		for cid in cardid:
			if cid:
				card = self.addCard(cid)
				if card:
					newCard.append(card)
		return newCard

	def canDelCard(self, id):
		if self.team.count (id) > 0:
			return False
		for edu_slot in self.user.educate['edu_slot']:
			if edu_slot and edu_slot.has_key('cardid') and edu_slot['cardid'] == id:
				return False
		return True		
			
	def delCard(self, id):
		if not self.canDelCard(id):
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
	def addEquipmentCount(self, equipmentid, cnt):
		equipmentConf = config.getConfig('equipment')
		equipment = []
		for i in range(cnt):
			if equipmentConf.has_key(equipmentid):				
				data = {}
				data['equipmentid'] = equipmentid
				data['id'] = self.generateEquipmentName()
				self.equipment.append(data)
				equipment.append(data)
		return equipment
		
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
		self.equipment = filter(lambda e : e['id'] != id, self.equipment)
		return 1
	
	def generateCardName(self):
		return self.generateName('C')
		
	def generateEquipmentName(self):
		return self.generateName('E')
	
	def generateStoneName(self):
		return self.generateName('S')
		
	def generateSkillName(self):
		return self.generateName('K')
	
	def generateItemName(self):
		return self.generateName('I')
	
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
		
	def getFirstCardType(self, cardid):
		for card in self.card:
			if card['cardid'] == cardid:
				return card
		return None
		
	def getEquipment(self, id):
		for equipment in self.equipment:
			if equipment['id'] == id:
				return equipment
		return None
		
	def getOwnerEquipment(self, card, id):
		for equipment in card['slot']:
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
		st_slot = {}
		
		for i, t in enumerate(self.team):
			if t:
				tc = self.getCard(t)
				if tc.has_key('st_slot'):
					st_slot['t' + str(i)] = tc['st_slot']
				else:
					st_slot['t' + str(i)] = stone.make_st_solt()
			else:
				st_slot['t' + str(i)] = stone.make_st_solt()
		return st_slot
		
	def getSkSlots(self):
		sk_slot = {}
		
		for i, t in enumerate(self.team):
			if t:
				tc = self.getCard(t)
				if tc.has_key('sk_slot'):
					sk_slot['t'+ str(i)] = tc['sk_slot']
				else:
					sk_slot['t' + str(i)] = skill.make_sk_slot()
			else:
				sk_slot['t' + str(i)] = skill.make_sk_slot()
		return sk_slot
	
	def setTeam(self, cardid1, cardid2, cardid3, cardid4, cardid5, cardid6, deq, dst, dsk):
		
		if cardid1 != '':
			if cardid1 == cardid2 or cardid1 == cardid3 or cardid1 == cardid4 or cardid1 == cardid5 or cardid1 == cardid6:
				return {'team':self.team}
		if cardid2 != '':
			if cardid2 == cardid3 or cardid2 == cardid4 or cardid2 == cardid5 or cardid2 == cardid6:
				return {'team':self.team}
		if cardid3 != '':
			if cardid3 == cardid4 or cardid3 == cardid5 or cardid3 == cardid6:
				return {'team':self.team}
		if cardid4 != '':
			if cardid4 == cardid5 or cardid4 == cardid6:
				return {'team':self.team}
		if cardid5 != '':
			if cardid5 == cardid6:
				return {'team':self.team}
				
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
			
		deq1, dst1, dsk1 = self.setTeamEquipmentStoneSkill(cardid1, 0, gameConf)
		deq2, dst2, dsk2 = self.setTeamEquipmentStoneSkill(cardid2, 1, gameConf)
		deq3, dst3, dsk3 = self.setTeamEquipmentStoneSkill(cardid3, 2, gameConf)
		deq4, dst4, dsk4 = self.setTeamEquipmentStoneSkill(cardid4, 3, gameConf)
		deq5, dst5, dsk5 = self.setTeamEquipmentStoneSkill(cardid5, 4, gameConf)
		deq6, dst6, dsk6 = self.setTeamEquipmentStoneSkill(cardid6, 5, gameConf)		
		
		deq.extend(deq1)
		deq.extend(deq2)
		deq.extend(deq3)
		deq.extend(deq4)
		deq.extend(deq5)
		deq.extend(deq6)
		
		dst.extend(dst1)
		dst.extend(dst2)
		dst.extend(dst3)
		dst.extend(dst4)
		dst.extend(dst5)
		dst.extend(dst6)
		
		dsk.extend(dsk1)
		dsk.extend(dsk2)
		dsk.extend(dsk3)
		dsk.extend(dsk4)
		dsk.extend(dsk5)
		dsk.extend(dsk6)

		self.save()
		return None
	
	
	def setTeamEquipmentStoneSkill(self, cardid, teamPos, gameConf):
		dst = []
		deq = []
		dsk = []
		if cardid:
			card = self.getCard(cardid)
			card['slot'] = equipment.make_slot()
			card['st_slot'] = stone.make_st_solt()
			card['sk_slot'] = skill.make_sk_slot()
			if self.team[teamPos]:
				teamCard = self.getCard(self.team[teamPos])
				deq.extend(equipment.exchage(self, card, teamCard, gameConf))
				dst.extend(stone.exchage(self, card, teamCard, gameConf))
				dsk.extend(skill.exchage(self, card, teamCard, gameConf))
			self.team[teamPos] = cardid
		elif self.team[teamPos]:
			teamCard = self.getCard(self.team[teamPos])
			deq.extend(equipment.takeoff(self, teamCard))
			dst.extend(stone.takeoff(self, teamCard))
			dsk.extend(skill.takeoff(self, teamCard))			
			self.team[teamPos] = ''
		return deq, dst, dsk
		
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
		
	def addStoneCount(self, stoneid, cnt):
		stoneConf = config.getConfig('stone')
		
		stone = []
		stoneInfo = stoneConf[stoneid]		
		for i in range(cnt):
			st = {}
			st['stoneid'] = stoneid
			st['id'] = self.generateStoneName()
			st['level'] = 1
			st['exp'] = 0
			self.stone.append(st)
			stone.append(st)
		return stone
		
	def getStone(self, id):					
		for st in self.stone:			
			if st['id'] == id:
				return st
		return None
		
	def delStone(self, id):
		self.stone = filter(lambda s : s['id'] != id, self.stone)
		return 1
			
	def depositStone(self, st):
		self.stone.append(st)
		
	def withdrawStone(self, id):
		res = None
		for i, st in enumerate(self.stone):			
			if st['id'] == id:
				res = st
				break
		if res:
			self.stone.remove(res)
		return res
		
	def addSkill(self, skillid, level = 1):
		skillConf = config.getConfig('skill')
		
		skillInfo = skillConf[skillid]
		
		sk = {}
		sk['skillid'] = skillid
		sk['id'] = self.generateSkillName()
		sk['level'] = level
		sk['exp'] = 0
		self.skill.append(sk)
		return sk
	
	def addSkillCount(self, skillid, cnt):
		skillConf = config.getConfig('skill')
		skillInfo = skillConf[skillid]
		
		skill = []
		
		for i in range(cnt):
			sk = {}
			sk['skillid'] = skillid
			sk['id'] = self.generateSkillName()
			sk['level'] = 1
			sk['exp'] = 0
			self.skill.append(sk)
			skill.append(sk)
		return skill
	
	def addAllSkill(self, skillid):
		newSkill = []
		for sid in skillid:
			if sid:
				skill = self.addSkill(sid)
				if skill:
					newSkill.append(skill)
		return newSkill
		
	def getSkill(self, id):
		for sk in self.skill:
			if sk['id'] == id:
				return sk
		return None
	
	def delSkill(self, id):
		self.skill = filter(lambda s : s['id'] != id, self.skill)
		return 1
			
	def depositSkill(self, sk):
		self.skill.append(sk)
		
	def withdrawSkill(self, id):
		res = None
		for i, sk in enumerate(self.skill):
			if sk['id'] == id:
				res = sk
				break
		if res:
			self.skill.remove(res)
		return res
		
	def addItem(self, itemid):
		itemConf = config.getConfig('item')
		itemInfo = itemConf[itemid]
		
		for it in self.item:
			if it['itemid'] == itemid and it['count'] < itemInfo['stack']:
				it['count'] = it['count'] + 1
				return it, None
		
		it = {}
		it['itemid'] = itemid
		it['id'] = self.generateItemName()
		it['count'] = 1
		self.item.append(it)
		return None, it
	
	def addItemCount(self, itemid, cnt):
		itemConf = config.getConfig('item')
		itemInfo = itemConf[itemid]
		
		itemCount = cnt
		
		its = []
		
		for it in self.item:
			if it['itemid'] == itemid and itemCount and it['count'] < itemInfo['stack']:
				if it['count'] + itemCount > itemInfo['stack']:
					itemCount = it['count'] + itemCount - itemInfo['stack']
					it['count'] = itemInfo['stack']
					its.append(it)
				else:
					it['count'] = it['count'] + itemCount
					itemCount = 0
					its.append(its)
		
		item = []
		
		while itemCount != 0:
			it = {}			
			it['itemid'] = itemid
			it['id'] = self.generateItemName()
			if itemCount > itemInfo['stack']:
				it['count'] = itemInfo['stack']
				itemCount = itemCount - itemInfo['stack']
			else:
				it['count'] = itemCount
				itemCount = 0
			item.append(it)
			self.item.append(it)						
		return its, item
		
	def delItem(self, id, cnt = 1):
		if cnt <= 0:
			return 0
		it = self.getItem(id)
		
		if it:
			if ['count'] < cnt:
				return 0
		
			it['count'] = it['count'] - cnt
			if it['count'] > 0:
				return it
			else: 
				self.item.remove(it)
				return None
		return 0
			
	def getItem(self, id):
		for it in self.item:
			if it['id'] == id:
				return it
		return None
		