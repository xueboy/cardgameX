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
		
		onePetConf = petConf[card['cardid']]	
		
		costMoney = len(sourceCard) * gameConf['pet_levelup_gold_cost']
		
		exp = 0
		for card in sourceCard:
			exp = pet.totalExp(card['exp'], card['level'], onePetConf['star']) + exp
			inv.delCard(card['id'])
		
		exp = int(exp * 0.5)

		star = onePetConf['star']	
		levelLimit = gameConf['pet_level_limit'][star - 1]	
		needExp = petLevelConf[str(destCard['level'])][star]
		while exp > needExp:
			exp = exp - needExp
			destCard['level'] = destCard['level'] + 1
			needExp = petLevelConf[str(destCard['level'])][star]
		destCard['exp'] = exp
		if destCard['level'] >= levelLimit:
			destCard['level'] = levelLimit
			destCard['exp'] = 0
		inv.save()
		return destCard, sourceCardid
				

	@staticmethod	
	def totalExp(exp, cardLevel, cardStar):
		petLevelConf = config.getConfig('pet_level')		
		total = 0			
		for i in range(1, cardLevel - 1):		
			total = petLevelConf[str(i)][cardStar - 1] + total
		total += exp
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

		
		if usr.train_prd['cost']['gold'] > usr.gold:
			return {'msg':'gold_not_enough'}
		if usr.train_prd['cost']['gem'] > usr.gem:
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
		
		usr.train_prd['cardid'] = cardid
		usr.train_prd['strength_revision'] = strrev
		usr.train_prd['intelligence_revision'] = itlrev
		usr.train_prd['artifice_revision'] = artrev
		
		usr.gold = usr.gold - cost['gold']
		usr.gem = usr.gem - cost['gem']
		
		usr.save()
		
		return {'train_prd': usr.train_prd, 'gold':usr.gold, 'gem':usr.gem}	
		
	@staticmethod
	def trainConfirm(usr):
		
		if not usr.train_prd:
			return {'msg':'training_should_before'}				
				
		inv = usr.getInventory()		
		card = inv.getCard(usr.train_prd['cardid'])
		if not card:
			return {'msg':'card_not_exist'}
				
		card['strength'] = card['strength'] + usr.train_prd['strength_revision']
		card['intelligence'] = card['intelligence'] + usr.train_prd['intelligence_revision']
		card['artifice'] = card['artifice'] + usr.train_prd['artifice_revision']
				
		usr.train_prd = None
		
		inv.save()
		usr.save()
		return {'training_card':card}
		
		
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