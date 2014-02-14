#coding:utf-8
#!/usr/bin/env python

from game.routine.pet import pet
from game.routine.skill import skill
from game.routine.equipment import equipment


class luck:
	
				
	@staticmethod
	def check(usr, card, petConf):
		
		petInfo = petConf[card['cardid']]
			
		luckid = []	
			
		for l in petInfo['luck']:
			luckid, cardid, equipmentid, skillid = luck.analyse(l)
			
			if luck.has_card(usr, cardid):
				if luck.has_equipment(usr, card, equipmentid):
					if luck.has_skill(usr, card, skillid):
						luckid.append(luckid)
						
		return luckid		
		
	@staticmethod
	def analyse(luck):
		luck = luck.split('_')
		cardid = []
		equipmentid = []
		skillid = []
		luckid = ''
		for l in luck:
			if l.startswith('pet'):
				cardid.append(l)
			elif l.startswith('sk'):
				skillid.append(l)
			elif l.startswith('eqp'):
				equipmentid.append(l)
			elif l.startswith('y'):
				luckid = l
		return luckid, cardid, equipmentid, skillid
		
	@staticmethod
	def has_card(usr, cardid):
		inv = usr.getInventory()
		
		teamCardid = []
		
		for cid in inv.team:
			if cid:
				card = inv.getCard(cid)
				teamCardid.append(card['cardid'])
				
		for cid in cardid:
			if cid not in teamCardid:
				return False
		
		return True
		
	@staticmethod
	def has_equipment(usr, card, equipmentid):
		inv = usr.getInventory()
		
		equipid = []
		
		for eq in card['slot']:
			if eq:
				equipid.append(eq['equipmentid'])
		
		for eqid in equipmentid:
			if eqid not in equipid:
				return False
		return True
		
	@staticmethod
	def has_skill(usr, card, skillid):
		inv = usr.getInventory()
		
		skid = []
		
		for sk in card['sk_slot']:
			if sk:
				skid.append(sk['skillid'])
				
		for sid in skillid:
			if sid not in skid:
				return False
		return True
		
				
		
		
		
	
			
				
			
		