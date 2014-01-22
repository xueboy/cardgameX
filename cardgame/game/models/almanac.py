#coding:utf-8
#!/usr/bin/env python


from gclib.object import object
from game.utility.config import config

class almanac(object):
	
	
	def __init__(self):
		object.__init__(self)
		self.card = set()
		self.equipment = set()
		self.skill = set()
		self.combine = []		
		self.user = None		
		return
	
	def init(self):
		pass
		
	def install(self, roleid):
		object.install(self, roleid)
	
	def load(self, roleid, data):
		object.load(self, roleid, data)
		self.roleid = roleid
		self.card = set(data['card'])
		self.equipment = set(data['equipment'])
		self.skill = set(data['skill'])		
		self.combine = data['combine']		
		
	def getData(self):
		data = object.getData(self)
		data['card'] = list(self.card)
		data['equipment'] = list(self.equipment)
		data['skill'] = list(self.skill)
		data['combine'] = self.combine		
		
		return data
		
	def getClientData(self):
		data = {}
		data['almanac_card'] = list(self.card)
		data['almanac_skill'] = list(self.skill)
		data['almanac_equipment'] = list(self.equipment)
		data['almanac_combine'] = self.combine
		
		return data
	
	def addCard(self, cardid):						
		if cardid in self.card:
			return
		self.card.add(cardid)
		self.notifyCard(cardid)
		self.save()
		return
	
	def addSkill(self, skillid):
		if skillid in self.skill:
			return
		self.skill.add(skillid)
		self.notifySkill(skillid)
		self.save()
		return
		
	def addEquipment(self, eqiupmentid):
		if equipmentid in self.equipment:
			return
		self.card.add(equipmentid)
		self.notifyEquipment(equipmentid)
		self.save()
		return
		
	def award(self, cmbid):
		combinaionConf = config.getConfig('almanac_combination')
		
		if cmbid in self.combine:
			return {'msg':'almanac_combine_already_get'}
		
		if not combinaionConf.has_key(cmbid):
			return {'msg':'almanac_combination_not_exist'}
		
		combinationInfo = combinaionConf[cmbid]
		
		isCombine = True
		for cid in combinationInfo['combin_cardid']:
			 if cid not in self.card:
			 	isCombine = False
			
		for sid in combinationInfo['combin_skillid']:
			if sid not in self.skill:
				isCombine = False
		
		for eid in combinationInfo['combin_equipmentid']:
			if eid not in self.equipment:
				isCombine = False
				
		if not isCombine:
			return {'msg':'almanac_not_combine'}
			
		data = {}
		
		self.combinaion.append(cmbid)			
		if combinationInfo['dropid']:			
			drop.open(self.user, combinationInfo['dropid'], data)			
		data['add_almanac_combine'] = cmbid
			
		return data			
				
	def notifyCard(self, cardid):
		usr = self.user
		if not usr.notify.has_key('almanac_notify'):
			usr.notify['almanac_notify'] = {}				
		if not usr.notify['almanac_notify'].has_key('card'):
			usr.notify['almanac_notify']['card'] = []				
		usr.notify['almanac_notify'].append(cardid)
		usr.save()
			
	def notifySkill(self, skillid):
		usr = self.user
		if not usr.notify.has_key('almanac_notify'):
			usr.notify['almanac_notify'] = {}				
		if not usr.notify['almanac_notify'].has_key('skill'):
			usr.notify['almanac_notify']['skill'] = []				
		usr.notify['almanac_notify'].append(skillid)
		usr.save()

			
	def notifyEquipment(self, equipmentid):
		usr = self.user
		if not usr.notify.has_key('almanac_notify'):
			usr.notify['almanac_notify'] = {}				
		if not usr.notify['almanac_notify'].has_key('equipment'):
			usr.notify['almanac_notify']['equipment'] = []				
		usr.notify['almanac_notify'].append(equipmentid)
		usr.save()

	