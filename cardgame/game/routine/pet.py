#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config

class pet:
	
	@staticmethod
	def isCardAvailable(usr, cardid):
		inv = usr.getInventory()
		if cardid == inv.team[0]:
			return False
		if cardid == inv.team[1]:
			return False
		if cardid == inv.team[2]:
			return False
		if cardid == inv.team[3]:
			return False
		if cardid == inv.team[4]:
			return False
		return True

	
	@staticmethod
	def levelup(usr, destCardid, sourceCardid):
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		petLevelConf = config.getConfig('pet_level')
		petConf = config.getConfig('pet')
		destCard = inv.getCard(destCardid)
		sourceCard = []
		for cardid in sourceCardid:
			if not pet.isCardAvailable(usr, cardid):
				return destCard,[]
			card = inv.getCard(cardid)			
			sourceCard.append(card)
		
		costMoney = len(sourceCard) * gameConf['pet_levelup_gold_cost']
		
		exp = 0
		for card in sourceCard:
			exp = pet.totalExp(card) + exp
		
		exp = int(exp * 0.5)
		onePetConf = petConf[card['cardid']]	
		star = onePetConf['star']	
		levelLimit = gameConf['pet_level_limit'][star - 1]	
		needExp = petLevelConf[str(destCard['level'])][star]
		while exp > needExp:
			exp = exp - needExp
			destCard['level'] = destCard['level'] + 1
			needExp = petLevelConf[str(destCard['level'])][stra]
		destCard['exp'] = exp
		if destCard['level'] >= levelLimit:
			destCard['level'] = levelLimit
			destCard['exp'] = 0
		inv.save()
		return destCard, sourceCardid
				

	@staticmethod	
	def totalExp(card):
		petLevelConf = config.getConfig('pet_level')		
		total = 0	
		for i in range(1, card['level'] - 1):		
			total = petLevelConf[str(i)][star - 1] + total
		total += card['exp']
		return total
		

		