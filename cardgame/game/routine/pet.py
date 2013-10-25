#coding:utf-8
#!/usr/bin/env python

import random
import math
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
		


	@staticmethod
	def training(usr, cardid, trainlevel):
		inv = usr.getInventory()
		
		card = inv.getCard(cardid)
		if not card:
			return {'msg':'card_not_exist'}
			
		cost = None	
		gameConf = config.getConfig('game')
		if trainlevel == '1':
			cost = gameConf['training_price1']
		elif trainlevel == '2':
			cost = gameConf['training_price2']
		elif trainlevel == '3':
			cost = gameConf['training_price3']
		else:
			return {'msg':'level_out_of_expect'}
		
		if cost['gold'] > usr.gold:
			return {'msg':'gold_not_enough'}
		if cost['gem'] > usr.gem:
			return {'msg': 'gem_not_enough'}
		
		
		strrev = 0
		itlrev = 0
		artrev = 0
		if trainlevel == '1':
			strrev = random.randint(-10, int(card['level']))
			itlrev = random.randint(-10, int(card['level'] * 1.5 - strrev))
			artrev = random.randint(-10, int(card['level'] * 1.5 - strrev - itlrev))
		elif trainlevel == '2':
			strrev = random.randint(-10, int(card['level']))
			itlrev = random.randint(-10, int(card['level'] * 2 - strrev))
			artrev = random.randint(-10, int(card['level'] * 2 - strrev - itlrev))
		elif trainlevel == '3':
			strrev = random.randint(-10, int(card['level']))
			itlrev = random.randint(-10, int(card['level'] * 2.5 - strrev))
			artrev = random.randint(-10, int(card['level'] * 2.5 - strrev - itlrev))
		elif trainlevel == '4':
			strrev = random.randint(-10, int(card['level']))
			itlrev = random.randint(-10, int(card['level'] * 3 - strrev))
			artrev = random.randint(-10, int(card['level'] * 3 - strrev - itlrev))
		
		card['strenghth'] = card['strenghth'] + strrev
		card['intelligence'] = card['intelligence'] + itlrev
		card['artifice'] = card['artifice'] + artrev
		
		usr.gold = usr.gold - cost['gold']
		usr.gem = usr.gem - cost['gem']
		
		inv.save()
		usr.save()
		
		return {'training_card':card, 'gold':usr.gold, 'gem':usr.gem}	
		
		
	@staticmethod
	def sell(usr, id):
			
		inv = usr.getInventory()
		card = inv.getCard(id)
		if not card:
			return {'msg':'card_not_exit'}
			
		petConf = config.getConfig('pet')
		gameConf = config.getConfig('game')
			
		param1 = 0
		param2 = 0
			
		cardid = card['cardid']			
			
		if petConf[cardid]['star'] == 1:
			param1 = gameConf['pet_star_1_price_param1']
			param2 = gameConf['pet_star_1_price_param2']
		elif petConf[cardid]['star'] == 2:
			param1 = gameConf['pet_star_2_price_param1']
			param2 = gameConf['pet_star_2_price_param2']
		elif petConf['cardid']['star'] == 3:
			param1 = gameConf['pet_star_3_price_param1']
			param2 = gameConf['pet_star_3_price_param2']
		elif petConf['cardid']['star'] == 4:
			param1 = gameConf['pet_star_4_price_param1']
			param2 = gameConf['pet_star_4_price_param2']
		elif petConf['cardid']['star'] == 5:
			param1 = gameConf['pet_star_5_price_param1']
			param2 = gameConf['pet_star_5_price_param2']
		else: 
			return {'msg':'star_outof_expect'}
				
		price = param1 + param2 * card['level']
		price = int(price - math.fmod(price, 100))
			
		usr.gold = usr.gold + price
			
		inv.delCard(id);
		usr.save()
			
		return {'gold': usr.gold, 'sell_card':id}