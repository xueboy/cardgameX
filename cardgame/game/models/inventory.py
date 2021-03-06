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
		"""
		构造函数
		"""
		object.__init__(self)
		self.card = []
		self.card_chip = {}
		self.item = []
		self.team = ['', '', '', '', '', '']	
		self.equipment = []
		self.equipment_chip = {}
		self.stone = []		
		self.user = None
		self.skill = []
		self.skill_chip = {}
		self.medal = {}
		
		
	def init(self):		
		"""
		初始化
		"""
		return		
		
	def install(self, roleid):
		"""
		安装
		"""
		object.install(self, roleid)
		
	def getData(self):
		"""
		得到数据
		"""
		data = object.getData(self)
		data['card'] = self.card
		data['card_chip'] = self.card_chip
		data['item'] = self.item		
		data['team'] = self.team
		data['equipment'] = self.equipment
		data['equipment_chip'] = self.equipment_chip
		data['stone'] = self.stone
		data['skill'] = self.skill
		data['skill_chip'] = self.skill_chip
		data['medal'] = self.medal
		
		return data
		
		
	@staticmethod
	def getClientCard(card):
		"""
		得到 client data
		"""
		data = card.copy()
		if data.has_key('slot'):
			del data['slot']
		if data.has_key('st_slot'):
			del data['st_slot']
		if data.has_key('sk_slot'):
			del data['sk_slot']
		if data.has_key('strength_ptr'):
			del data['strength_ptr']
		if data.has_key('intelligence_ptr'):
			del data['intelligence_ptr']
		if data.has_key('artifice_ptr'):
			del data['artifice_ptr']
		return data
		
	def getClientData(self):
		"""
		得到 client data
		"""
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
			skill[sk['id']]['exp'] = int(skill[sk['id']]['exp'])
			
		for m in team:
			if m and m.has_key('sk_slot'):
				for sk in m['sk_slot']:
					if sk:
						skill[sk['id']] = sk
					
		item = {}		
		for  it in self.item:
			item[it['id']] = it
			
		medal = {}
		for (mid, m) in self.medal.items():
			d = m.copy()
			del d['id']
			medal[mid] = d
					
		data['card'] = card
		data['card_chip'] = self.card_chip
		data['team'] = self.team
		data['item'] = item
		data['equipment'] = equipment
		data['equipment_chip'] = self.equipment_chip
		data['slot'] = self.getSlots()
		data['st_slot'] = self.getStSlots()
		data['sk_slot'] = self.getSkSlots()
		data['stone'] = stone
		data['skill'] = skill
		data['skill_chip'] = self.skill_chip
		data['medal'] = medal
		return data
		
	def load(self, roleid, data):
		"""
		加载
		"""
		object.load(self, roleid, data)
		
		for c in data['card']:
			if c.has_key('init_start'):
				c['init_star'] = c['init_start']
				del c['init_start']
		
		self.card = data['card']
		self.card_chip = data['card_chip']
		self.item = data['item']
		self.team = data['team']
		self.equipment = data['equipment']
		self.equipment_chip = data['equipment_chip']
		self.stone = data['stone']
		self.skill = data['skill']
		self.skill_chip = data['skill_chip']
		self.medal = data['medal']
		
		
		
	def addCard(self, cardid, level = 1):
		"""
		添加卡牌
		"""
		cardConf = config.getConfig('pet')				
		if cardConf.has_key(cardid):
			card = pet.make_pet(self, cardid, level, cardConf)
			self.card.append(card)
			usr = self.user
			al = usr.getAlmanac()
			al.addCard(cardid)
			return card
		return None
	
	def addCardCount(self, cardid, cnt, level = 1):
		"""
		添加卡牌个数
		"""
		cardConf = config.getConfig('pet')
		if cardConf.has_key(cardid):
			usr = self.user
			al = usr.getAlmanac()
			al.addCard(cardid)
			c = []
			for i in range(cnt):
				card = pet.make_pet(self, cardid, level, cardConf)
				self.card.append(card)
				c.append(card)
			return c
		return None
				
	
	def addAllCard(self, cardid):
		"""
		批量添加卡牌
		"""
		newCard = []
		for cid in cardid:
			if cid:
				card = self.addCard(cid)
				if card:
					newCard.append(card)
		return newCard

	def addCardChip(self, cardid, cnt):
		"""
		添加卡片碎片
		"""
		cardConf = config.getConfig('pet')
		if not cardConf.has_key(cardid):
			return -1
		if not self.card_chip.has_key(cardid):
			self.card_chip[cardid] = 0
		self.card_chip[cardid] = self.card_chip[cardid] + cnt
		return self.card_chip[cardid]

	def canDelCard(self, id):
		"""
		删除卡片
		"""
		if self.team.count (id) > 0:
			return False
		for edu_slot in self.user.educate['edu_slot']:
			if edu_slot and edu_slot.has_key('card_id') and edu_slot['card_id'] == id:
				return False
		return True		
			
	def delCard(self, id):
		"""
		删除卡片
		"""
		if not self.canDelCard(id):
			return 0
		self.card = filter(lambda c : c['id'] != id, self.card)		
		return 1	
	
	def CountCardByQuality(self, quality, petConf):
		"""
		以品质计算卡牌
		"""
		cnt = 0
		for card in self.card:
			petInfo = petConf[card['cardid']]
			if petInfo['quality'] == quality:
				cnt = cnt + 1
		return cnt

	def CountCardChip(self, cardid):
		"""
		计算卡牌碎片
		"""
		if not self.card_chip.has_key(cardid):
			return 0
		return self.card_chip[cardid]
	
	def addEquipment(self, equipmentid):
		"""
		添加装备
		"""
		equipmentconf = config.getConfig('equipment')
		if equipmentconf.has_key(equipmentid):
			data = {}
			data['equipmentid'] = equipmentid
			data['id'] = self.generateEquipmentName()
			self.equipment.append(data)
			usr = self.user
			al = usr.getAlmanac()
			al.addEquipment(equipmentid)
			return data
		return None
		
	def addEquipmentCount(self, equipmentid, cnt):
		"""
		添加多件装备
		"""
		equipmentConf = config.getConfig('equipment')
		equipment = []
		usr = self.user
		al = usr.getAlmanac()
		for i in range(cnt):
			if equipmentConf.has_key(equipmentid):				
				data = {}
				data['equipmentid'] = equipmentid
				data['id'] = self.generateEquipmentName()
				self.equipment.append(data)
				equipment.append(data)				
				al.addEquipment(equipmentid)
		return equipment
		
	def addEquipmentChip(self, equipmentid, cnt):
		"""
		添加装备碎片
		"""
		equipmentConf = config.getConfig('equipment')
		if not equipmentConf.has_key(equipmentid):
			return -1
		if not self.equipment_chip.has_key(equipmentid):
			self.equipment_chip[equipmentid] = 0
		self.equipment_chip[equipmentid] = self.equipment_chip[equipmentid] + cnt
		return self.equipment_chip[equipmentid]
		
	def depositEquipment(self, equipment):
		"""
		分解装备
		"""
		self.equipment.append(equipment)
		return equipment
		
	def withdrawEquipment(self, id):
		"""
		取出装备
		"""
		res = None
		for equipment in self.equipment:
			if equipment['id'] == id:
				res = equipment
				self.equipment.remove(equipment)
		return res
	
	
	def delEquipment(self, id):
		"""
		删除装备
		"""
		self.equipment = filter(lambda e : e['id'] != id, self.equipment)
		return 1
		
	def CountEquipmentChip(self, equipmentid):
		"""
		计算装备碎片
		"""
		if not self.equipment_chip.has_key(equipmentid):
			return 0
		return self.equipment_chip[equipmentid]
	
	def generateCardName(self):
		"""
		生成卡牌名称
		"""
		return self.generateName('C')
		
	def generateEquipmentName(self):
		"""
		生成装备名称
		"""
		return self.generateName('E')
	
	def generateStoneName(self):
		"""
		生成宝石名称
		"""
		return self.generateName('S')
		
	def generateSkillName(self):
		"""
		生成技能名称
		"""
		return self.generateName('K')
	
	def generateItemName(self):
		"""
		生成道具名称
		"""
		return self.generateName('I')
	
	def generateName(self, perfix):
		"""
		生成名称
		"""
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
		"""
		得到卡牌
		"""
		for card in self.card:
			if card['id'] == id:
				return card
		return None
		
	def getFirstCardType(self, cardid):
		"""
		得到第一个卡片该类型卡牌
		"""
		for card in self.card:
			if card['cardid'] == cardid:
				return card
		return None
		
	def getEquipment(self, id):
		"""
		得到装备
		"""
		for equipment in self.equipment:			
			if equipment['id'] == id:				
				return equipment
		return None
		
	def getOwnerEquipment(self, card, id):
		"""
		得到所有者装备
		"""
		for equipment in card['slot']:
			if equipment['id'] == id:
				return equipment
		return None
		
	def getSlots(self):
		"""
		得到槽位
		"""
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
		"""
		得到宝石槽位
		"""
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
		"""
		得到技能槽位
		"""
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
		"""
		设置队伍
		"""
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
		
		if cardid1 != self.team[0] and usr.level <  teamLevelConf[0] and cardid1:
			return {'msg':'level_required'}
		if cardid2 != self.team[1] and usr.level <  teamLevelConf[1] and cardid2:
			return {'msg':'level_required'}
		if cardid3 != self.team[2] and usr.level <  teamLevelConf[2] and cardid3:
			return {'msg':'level_required'}
		if cardid4 != self.team[3] and usr.level <  teamLevelConf[3] and cardid4:
			return {'msg':'level_required'}
		if cardid5 != self.team[4] and usr.level <  teamLevelConf[4] and cardid5:
			return {'msg':'level_required'}
		if cardid6 != self.team[5] and usr.level <  teamLevelConf[5] and cardid6:
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
		"""
		设置队伍的装备宝石技能
		"""
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
		"""
		添加宝石
		"""
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
		"""
		添加多个宝石
		"""
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
		"""
		得到宝石
		"""					
		for st in self.stone:			
			if st['id'] == id:
				return st
		return None
		
	def delStone(self, id):
		"""
		删除宝石
		"""
		self.stone = filter(lambda s : s['id'] != id, self.stone)
		return 1
			
	def depositStone(self, st):
		"""
		放入宝石
		"""
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
		"""
		添加技能
		"""
		skillConf = config.getConfig('skill')
		
		skillInfo = skillConf[skillid]
		
		sk = {}
		sk['skillid'] = skillid
		sk['id'] = self.generateSkillName()
		sk['level'] = level
		sk['exp'] = 0
		self.skill.append(sk)
		usr = self.user
		al = usr.getAlmanac()
		al.addSkill(skillid)		
		return sk
	
	def addSkillCount(self, skillid, cnt):
		"""
		添加多个技能
		"""
		skillConf = config.getConfig('skill')
		skillInfo = skillConf[skillid]
		
		skill = []
		usr = self.user
		al = usr.getAlmanac()
		for i in range(cnt):
			sk = {}
			sk['skillid'] = skillid
			sk['id'] = self.generateSkillName()
			sk['level'] = 1
			sk['exp'] = 0
			self.skill.append(sk)
			skill.append(sk)
			al.addSkill(skillid)
		return skill
		
	def addSkillChip(self, skillid, cnt):
		"""
		添加技能碎片
		"""
		skillConf = config.getConfig('skill')
		if not skillConf.has_key(skillid):
			return -1
		
		if not self.skill_chip.has_key(skillid):
			self.skill_chip[skillid] = 0
		self.skill_chip[skillid] = self.skill_chip[skillid] + cnt
		return self.skill_chip[skillid]
	
	def addAllSkill(self, skillid):
		"""
		添加所有的技能
		"""
		newSkill = []
		for sid in skillid:
			if sid:
				skill = self.addSkill(sid)
				if skill:
					newSkill.append(skill)
		return newSkill
		
	def getSkill(self, id):
		"""
		得到技能
		"""
		for sk in self.skill:
			if sk['id'] == id:
				return sk
		return None
	
	def delSkill(self, id):
		"""
		删除技能
		"""
		self.skill = filter(lambda s : s['id'] != id, self.skill)
		return 1
		
	def CountSkillChip(self, skillid):
		"""
		计算技能碎片个数
		"""
		if not self.skill_chip.has_key(skillid):
			return 0
		return self.skill_chip[skillid]
			
			
	def depositSkill(self, sk):
		self.skill.append(sk)
		
	def withdrawSkill(self, id):
		"""
		存入技能
		"""
		res = None
		for i, sk in enumerate(self.skill):
			if sk['id'] == id:
				res = sk
				break
		if res:
			self.skill.remove(res)
		return res
		
	def addItem(self, itemid):
		"""
		添加道具
		"""
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
		"""
		添加多少道具
		"""
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
					its.append(it)
					break
		
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
		"""
		删除道具
		"""
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
		"""
		得到道具
		"""
		for it in self.item:
			if it['id'] == id:
				return it
		return None
		
	def getItemByType(self, itemid):
		"""
		通过类型得到道具
		"""
		for it in self.item:
			if it['itemid'] == itemid:
				return it
		return None
		
	def addMedalChip(self, medalid, chipnum, cnt = 1):
		"""
		添加勋章碎片
		"""
		medalConfig = config.getConfig('medal')		
		medalInfo = medalConfig[medalid]		
		if not self.medal.has_key(medalid):
			self.medal[medalid] = {'level':0, 'chip': [0] * medalInfo['chip'], 'id':medalid, 'gravel':0}			
		self.medal[medalid]['chip'][chipnum] = self.medal[medalid]['chip'][chipnum] + cnt
		return self.medal[medalid]
		
	def delMedalChip(self, medalid, chipnum):
		"""
		删除勋章碎片
		"""
		
		if not self.medal.has_key(medalid):
			return -1		
		if self.medal[medalid]['chip'][chipnum] < 1:
			return -1
		
		self.medal[medalid]['chip'][chipnum] = self.medal[medalid]['chip'][chipnum] - 1
		return self.medal[medalid]

		