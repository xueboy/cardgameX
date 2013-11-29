#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from game.utility.config import config

class almanac(object):
	
	
	def __init__(self):
		object.__init__(self)
		self.card = {}
		self.combinaion = []
		return
	
	def init(self):
		pass
	
	def load(self, roleid, data):
		object.load(self, roleid, data)
		self.roleid = roleid
		self.card = data['card']
		self.combinaion = data['combinaion']
		
	def getData(self):
		data = {}
		data['card'] = self.card
		data['combinaion'] = self.combinaion
		return data
		
	def getClientData(self):
		data = {}
		data['almanac_card'] = self.card
		data['almanac_combinaion'] = self.combinaion
		return data
	
	def insert(self, cardid):
		if self.card.has_key(cardid):
			return					
		usr = self.user
		inv = usr.getInventory()
		self.card[cardid] = {}
		newCom, aw  = self.update(cardid)		
		data = {}
		if newCom:
			data['new_almanac_combination'] = newCom
		if aw['gold']:
			usr.gold = usr.gold + aw['gold']
			data['gold'] = usr.gold
		if aw['gem']:
			usr.gem = usr.gem + aw['gem']
			data['gem'] = usr.gem
		if aw['card']:
			newCard = inv.addAllCard(aw['card'])
			data['new_card_array'] = newCard
		if aw['skill']:
			newSkill = inv.addAllSkill(aw['skill'])
			data['new_skill_array'] = newSkill
		if aw['item']:
			newItem = inv.addAllItem(aw['item'])
			data['new_item_array'] = newItem
		
		if data:
			usr.notify['almanac_notify'] = data
		self.save()
		usr.save()		
		inv.save()
		return
			
		
	def update(self, cardid):
		
		almanacCombinationConf = config.getConfig('almanac_combination')
		usr = self.user
		inv = usr.getInventory()
		
		newComb = []
		aw = {'gold':0, 'gem':0, 'item':[], 'card':[], 'skill':[], 'item':[]}		
		
		for confKey in almanacCombinationConf:
			if confKey not in self.combinaion:
				isAbsence = False
				for cid in almanacCombinationConf[confKey]['combin_cardid']:
					if not inv.getFirstCardType(cid):
						isAbsence = True						
						break				
				if not isAbsence:
					newComb.append(confKey)
					almanac.award(confKey, aw, almanacCombinationConf)		
		return newComb, aw
		
	@staticmethod
	def award(acid, aw, almanacCombinationConf):
		almanacCombinationInfo = almanacCombinationConf[acid]		
		aw['gold'] = aw['gold'] + almanacCombinationInfo['gold']
		aw['gem'] = aw['gem'] + almanacCombinationInfo['gem']
		if almanacCombinationInfo['itemid']:
			aw['item'].append(almanacCombinationInfo['itemid'])
		if almanacCombinationInfo['cardid']:
			aw['card'].append(almanacCombinationInfo['cardid'])
		if almanacCombinationInfo['skillid']:
			aw['skill'].append(almanacCombinationInfo['skillid'])
	