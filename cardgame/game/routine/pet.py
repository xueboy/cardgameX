#coding:utf-8
#!/usr/bin/env python

import random
import math
from gclib.utility import randint
from game.utility.config import config

class pet:
	
	
	@staticmethod
	def make_pet(inv, cardid, level, cardConf):
		data = {}
		data['cardid'] = cardid
		data['id'] = inv.generateCardName()
		data['level'] = level
		data['exp'] = 0	
		data['strength'] = cardConf[cardid]['strength']
		data['intelligence'] = cardConf[cardid]['intelligence']
		data['artifice'] = cardConf[cardid]['artifice']
		data['reborn_level'] = 0
		data['init_start'] = 1
		return data
	
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
		if not sourceCardid:
			return {'msg':'card_not_exist'}
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		petLevelConf = config.getConfig('pet_level')
		petConf = config.getConfig('pet')
		destCard = inv.getCard(destCardid)
		sourceCard = []
		
		for cardid in sourceCardid:
			if not pet.isCardAvailable(usr, cardid):
				return {'msg':'card_not_available'}
			card = inv.getCard(cardid)			
			sourceCard.append(card)		
		
		costMoney = len(sourceCard) * gameConf['pet_levelup_gold_cost']		
		exp = 0
		for card in sourceCard:
			exp = pet.totalExp(card, petConf, petLevelConf, gameConf) + exp
			inv.delCard(card['id'])
		
		exp = int(exp * 0.5)
		pet.gainExp(destCard, exp, petConf, petLevelConf, gameConf)
		inv.save()
		return {'update_card':destCard, 'delete_card':sourceCardid}


	@staticmethod
	def gainExp(card, exp, petConf, petLevelConf, gameConf):
		level = card['level']
		id = card['cardid']
		quality = petConf[id]['quality']
		needExp = petLevelConf[str(level + 1)][quality - 1] - petLevelConf[str(level)][quality - 1]
		levelLimit = gameConf['pet_level_limit'][quality - 1]
		exp = exp + card['exp']
		card['exp'] = 0
		while exp > needExp and levelLimit > level:			
			exp = exp - needExp
			needExp = petLevelConf[str(level + 1)][quality - 1] - petLevelConf[str(level)][quality - 1]
			level = level + 1			
			card['level'] = level			
		card['exp'] = exp	
	

	@staticmethod	
	def totalExp(card, petConf, petLevelConf, gameConf):	
		total = 0
		petInfo = petConf[card['cardid']]
		quality = petInfo['quality']
		return petLevelConf[str(card['level'])][quality - 1] + card['exp'] + gameConf['pet_star_base_exp'][quality - 1]
		

	@staticmethod
	def training(usr, cardid, trainlevel):
		inv = usr.getInventory()
		
		card = inv.getCard(cardid)
		if not card:
			return {'msg':'card_not_exist'}
			
		cost = {}	
		gameConf = config.getConfig('game')
		if trainlevel == '0':
			trpPriceConfig = config.getConfig('trp_price')
			cost = {'trp':trpPriceConfig[usr.level - 1], 'gold':0, 'gem':0}
		elif trainlevel == '1':
			cost = gameConf['training_price1']
		elif trainlevel == '2':
			cost = gameConf['training_price2']
		elif trainlevel == '3':
			cost = gameConf['training_price3']
		else:
			return {'msg':'parameter_bad'}
	
		if cost['gold'] > usr.gold:
			return {'msg':'gold_not_enough'}
		if cost['gem'] > usr.gem:
			return {'msg': 'gem_not_enough'}
		if cost['trp'] > usr.trp:
			return {'msg': 'trp_not_enough'}
				
		strrev = 0
		itlrev = 0
		artrev = 0
		if trainlevel == '0':
			strrev = random.randint(-10, int(card['level']))
			itlrev = random.randint(-10, int(card['level'] * 1.5 - strrev))
			artrev = random.randint(-10, int(card['level'] * 1.5 - strrev - itlrev))
		elif trainlevel == '1':
			strrev = random.randint(-10, int(card['level']))
			itlrev = random.randint(-10, int(card['level'] * 2 - strrev))
			artrev = random.randint(-10, int(card['level'] * 2 - strrev - itlrev))
		elif trainlevel == '2':
			strrev = random.randint(-10, int(card['level']))
			itlrev = random.randint(-10, int(card['level'] * 2.5 - strrev))
			artrev = random.randint(-10, int(card['level'] * 2.5 - strrev - itlrev))
		elif trainlevel == '3':
			strrev = random.randint(-10, int(card['level']))
			itlrev = random.randint(-10, int(card['level'] * 3 - strrev))
			artrev = random.randint(-10, int(card['level'] * 3 - strrev - itlrev))
				
		usr.train_prd['cardid'] = cardid
		usr.train_prd['strength_revision'] = strrev
		usr.train_prd['intelligence_revision'] = itlrev
		usr.train_prd['artifice_revision'] = artrev
		
		usr.gold = usr.gold - cost['gold']
		usr.gem = usr.gem - cost['gem']
		usr.trp = usr.trp - cost['trp']
		
		usr.save()
		
		return {'train_prd': usr.train_prd, 'gold':usr.gold, 'gem':usr.gem, 'trp':usr.trp}	
		
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
				
		usr.train_prd = {}
		
		inv.save()
		usr.save()
		return {'training_card':card}
	
	
	@staticmethod		
	def decompose(usr, cardids):
		
		cards = []
		inv = usr.getInventory()
		trpConfig = config.getConfig('trp')
		
		total_trp = 0		
		for cardid in cardids:
			card = inv.getCard(cardid)
			if not card:
				return {'msg':'card_not_exist'}
			trp = trpConfig[card['level'] - 1]['card']
			total_trp = total_trp + trp
			inv.delCard(cardid)
			
		usr.trp = usr.trp + total_trp
		
		usr.save()
		inv.save()
		return {'trp':usr.trp, 'delete_card_array':cardids}
			
		
		
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
			
		if petConf[cardid]['quality'] == 1:
			param1 = gameConf['pet_star_1_price_param1']
			param2 = gameConf['pet_star_1_price_param2']
		elif petConf[cardid]['quality'] == 2:
			param1 = gameConf['pet_star_2_price_param1']
			param2 = gameConf['pet_star_2_price_param2']
		elif petConf['cardid']['quality'] == 3:
			param1 = gameConf['pet_star_3_price_param1']
			param2 = gameConf['pet_star_3_price_param2']
		elif petConf['cardid']['quality'] == 4:
			param1 = gameConf['pet_star_4_price_param1']
			param2 = gameConf['pet_star_4_price_param2']
		elif petConf['cardid']['quality'] == 5:
			param1 = gameConf['pet_star_5_price_param1']
			param2 = gameConf['pet_star_5_price_param2']
		else:
			return {'msg':'star_outof_expect'}
				
		price = param1 + param2 * card['level']
		price = int(price - math.fmod(price, 100))			
		usr.gold = usr.gold + price			
		inv.delCard(id);
		inv.save()
		usr.save()
		
		return {'gold': usr.gold, 'sell_card':id}
			
			
	@staticmethod
	def reborn(usr, id):
		
		gameConf = config.getConfig('game')
		rebornConf = config.getConfig('reborn')
		
		costGold = gameConf['pet_reborn_price']['gold']
		costGem = gameConf['pet_reborn_price']['gem']
		
		if usr.gold < costGold:
			return {'msg':'gold_not_enough'}
		if usr.gem < costGem:
			return {'msg':'gem_not_enough'}			
		
		inv = usr.getInventory()		
		card = inv.getCard(id)
		
		rebornInfo = None
		for r in rebornConf:
			if r['star_max'] > card['init_start']:
				rebornInfo = r
				break			
			if r['level'] > card['reborn_level']:
				rebornInfo = r
				break
		
		if not rebornInfo:
			return {'msg':'reborn_can_not'}
				
		if rebornInfo['level'] > card['level']:
			return {'msg':'reborn_level_required'}
				
		card['init_start'] = card['init_start'] = pet.reborn_inc_star(rebornInfo)
		card['reborn_level'] = rebornInfo['level']
		usr.gold = usr.gold - costGold
		inv.save()
		usr.save()
		
		return {'update_card': card, 'gold':usr.gold}		
				
	@staticmethod
	def reborn_inc_star(rebornInfo):
		rn = randint()
		
		for pb in rebornInfo['star']:
			if rn > pb['probability']:
				rn = rn - pb['probability']
			else: 
				return pb['star']
		return 0