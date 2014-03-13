#coding:utf-8
#!/usr/bin/env python

import random
import math
from gclib.utility import randint, currentTime
from game.utility.config import config
from game.routine.vip import vip
from game.routine.potential import potential
from game.routine.drop import drop

class pet:
	
	
	@staticmethod
	def make_pet(inv, cardid, level, petConf):
		"""
		制做宠物
		"""
		data = {}
		data['cardid'] = cardid
		data['id'] = inv.generateCardName()
		data['level'] = level
		data['exp'] = 0	
		data['strength'] = petConf[cardid]['strength']
		data['intelligence'] = petConf[cardid]['intelligence']
		data['artifice'] = petConf[cardid]['artifice']		
		data['init_star'] = 1
		for i in range(level):
			potential.onEveryPetLevelup(inv.user, data, petConf)
		return data
	
	@staticmethod
	def isCardAvailable(usr, cardid):
		"""
		是否卡牌有效
		"""
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
		"""
		升级
		"""
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
			if not card:
				return {'msg':'card_not_exist'}
			sourceCard.append(card)		
		
		costMoney = len(sourceCard) * gameConf['pet_levelup_gold_cost']		
		exp = 0
		for card in sourceCard:
			tExp = pet.totalExp(card, petConf, petLevelConf, gameConf) 
			exp = tExp + exp			
			inv.delCard(card['id'])		
		
		pet.gainExp(usr, destCard, exp, petConf, petLevelConf, gameConf)
		inv.save()
		return {'update_card':inv.getClientCard(destCard), 'delete_card':sourceCardid}
		#return {'cardid': destCard['id'], 'exp':destCard['exp'], 'level':destCard['level']}


	@staticmethod
	def gainExp(usr, card, exp, petConf, petLevelConf, gameConf):
		"""
		赢得经验
		"""
		level = card['level']
		id = card['cardid']
		quality = petConf[id]['quality']
		needExp = petLevelConf[str(level + 1)][quality - 1] - petLevelConf[str(level)][quality - 1]
		
		levelLimit = gameConf['pet_level_limit'][quality - 1]
		exp = exp + card['exp']
		card['exp'] = 0
		while (exp > needExp) and (levelLimit > level):
			exp = exp - needExp
			level = level + 1
			potential.onEveryPetLevelup(usr, card, petConf)
			needExp = petLevelConf[str(level + 1)][quality - 1] - petLevelConf[str(level)][quality - 1]			
			
			card['level'] = level			
		card['exp'] = exp	
	

	@staticmethod	
	def totalExp(card, petConf, petLevelConf, gameConf):
		"""
		总经验
		"""
		#total = 0
		petInfo = petConf[card['cardid']]
		quality = petInfo['quality']
		#return petLevelConf[str(card['level'])][quality - 1] + card['exp'] + gameConf['pet_star_base_exp'][quality - 1]
		return int(petLevelConf[str(card['level'])][quality - 1] * 0.75 + gameConf['pet_star_base_exp'][quality - 1])
		

	@staticmethod
	def training(usr, cardid, trainlevel):
		"""
		训练
		"""
		inv = usr.getInventory()
		
		card = inv.getCard(cardid)
		if not card:
			return {'msg':'card_not_exist'}
				
		if trainlevel == '2' and (not vip.canTrainLevel2(usr)):
			return {'msg': 'vip_required'}
			
		if trainlevel == '3' and (not vip.canTrainLevel3(usr)):
			return {'msg': 'vip_required'}
					
		cost = {}	
		gameConf = config.getConfig('game')
		trpProbabilityConf = config.getConfig('trp_probability')
		trpProbabilityInfo = {}
		if trainlevel == 0:
			trpPriceConfig = config.getConfig('trp_price')
			cost = {'trp':trpPriceConfig[usr.level - 1], 'gold':0, 'gem':0}
			trpProbabilityInfo = trpProbabilityConf['training']
		elif trainlevel == 1:
			cost = gameConf['training_price1']
			trpProbabilityInfo = trpProbabilityConf['training1']
		elif trainlevel == 2:
			cost = gameConf['training_price2']
			trpProbabilityInfo = trpProbabilityConf['training2']
		elif trainlevel == 3:
			cost = gameConf['training_price3']
			trpProbabilityInfo = trpProbabilityConf['training3']
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
				
		
		rd = randint()		
		for (i, prob) in  enumerate(trpProbabilityInfo):
			print prob, i
			if rd > prob:
				rd = rd - prob
			else:
				strrev = trpProbabilityConf['point'][i]
				break		
					
		rd = randint()
		for (i, prob) in  enumerate(trpProbabilityInfo):
			if rd > prob:
				rd = rd - prob
			else:
				itlrev = trpProbabilityConf['point'][i]
				break
		
		rd = randint()
		for (i, prob) in  enumerate(trpProbabilityInfo):
			if rd > prob:
				rd = rd - prob
			else:
				artrev = trpProbabilityConf['point'][i]
				break
			
		usr.train_prd['cardid'] = cardid
		usr.train_prd['strength_revision'] = strrev
		usr.train_prd['intelligence_revision'] = itlrev
		usr.train_prd['artifice_revision'] = artrev
		usr.train_prd['trp_level'] = trainlevel
		
		usr.gold = usr.gold - cost['gold']
		usr.gem = usr.gem - cost['gem']
		usr.trp = usr.trp - cost['trp']
		
		usr.save()
		
		prdData = usr.train_prd.copy()
		del prdData['trp_level']
		
		return {'train_prd': prdData, 'gold':usr.gold, 'gem':usr.gem, 'trp':usr.trp}
		
	@staticmethod
	def trainConfirm(usr):
		"""
		确认训练
		"""
		if not usr.train_prd:
			return {'msg':'training_should_before'}				
				
		inv = usr.getInventory()		
		card = inv.getCard(usr.train_prd['cardid'])
		if not card:
			return {'msg':'card_not_exist'}
				
					
		card['strength'] = card['strength'] + usr.train_prd['strength_revision']
		if card['strength'] < 0:
			usr.train_prd['strength_revision'] = usr.train_prd['strength_revision'] + card['strength']
			card['strength'] = 0		
		card['intelligence'] = card['intelligence'] + usr.train_prd['intelligence_revision']
		if card['intelligence'] < 0:
			usr.train_prd['intelligence_revision'] = usr.train_prd['intelligence_revision'] + card['intelligence']
			card['intelligence'] = 0
		card['artifice'] = card['artifice'] + usr.train_prd['artifice_revision']
		if card['artifice'] < 0:
			usr.train_prd['artifice_revision'] = usr.train_prd['artifice_revision'] + card['artifice']
			card['artifice'] = 0
		
		if not card.has_key('strength_ptr'):
			card['strength_ptr'] = 0
		if not card.has_key('intelligence_ptr'):
			card['intelligence_ptr'] = 0
		if not card.has_key('artifice_ptr'):
			card['artifice_ptr'] = 0
		
		total_trp_limit = 0
		if usr.train_prd['trp_level'] == 0:
			total_trp_limit = int(card['level'] * 1.5 + 30.5)
		elif usr.train_prd['trp_level'] == 1:
			total_trp_limit = int(card['level'] * 2 + 40)
		elif usr.train_prd['trp_level'] == 2:
			total_trp_limit = int(card['level'] * 2.5 + 50.5)
		elif usr.train_prd['trp_level'] == 3:
			total_trp_limit = int(card['level'] * 3 + 60)
			
		total_trp = card['strength_ptr'] + card['intelligence_ptr'] + card['artifice_ptr']
		total_over_trp = total_trp - total_trp_limit
		
		is_over_reduce = True
		while total_over_trp > 0 and is_over_reduce:
			is_over_reduce = False
			if usr.train_prd['strength_revision'] > 0:
				usr.train_prd['strength_revision'] = usr.train_prd['strength_revision'] - 1			
				card['strength'] = card['strength'] - 1
				total_over_trp = total_over_trp - 1
				is_over_reduce = True
			if usr.train_prd['intelligence_revision'] >0 and total_over_trp > 0:
				usr.train_prd['intelligence_revision'] = usr.train_prd['intelligence_revision'] - 1
				card['intelligence'] = card['intelligence'] - 1
				total_over_trp = total_over_trp - 1
				is_over_reduce = True
			if usr.train_prd['artifice_revision'] > 0 and total_over_trp > 0:				
				usr.train_prd['artifice_revision'] = usr.train_prd['artifice_revision'] - 1
				card['artifice'] = card['artifice'] - 1
				total_over_trp = total_over_trp - 1
				is_over_reduce = True
				
		petConf = config.getConfig('pet')
		petInfo = petConf[card['cardid']]
				
		card['strength_ptr'] = card['strength_ptr'] + usr.train_prd['strength_revision']
		card['intelligence_ptr'] = card['intelligence_ptr'] + usr.train_prd['intelligence_revision']
		card['artifice_ptr'] = card['artifice_ptr'] + usr.train_prd['artifice_revision']
				
		strength_ptr_limit = petInfo['strength'] + card['level'] + 20
		intelligence_ptr_limit = petInfo['intelligence'] + card['level'] + 20
		artifice_ptr_limit = petInfo['artifice'] + card['level'] + 20
		
		ptr_over = 0
		
		strength_ptr_over = card['strength'] - strength_ptr_limit
		intelligence_ptr_over = card['intelligence'] - intelligence_ptr_limit
		artifice_ptr_over = card['artifice'] - artifice_ptr_limit
		
		if strength_ptr_over > 0:
			card['strength_ptr'] = card['strength_ptr'] - strength_ptr_over
			card['strength'] = card['strength'] - strength_ptr_over
			ptr_over = ptr_over + strength_ptr_over
		if intelligence_ptr_over > 0:
			card['intelligence_ptr'] = card['intelligence_ptr'] - intelligence_ptr_over
			card['intelligence'] = card['intelligence'] - intelligence_ptr_over
			ptr_over = ptr_over + intelligence_ptr_over
		if artifice_ptr_over > 0:
			card['artifice_ptr'] = card['artifice_ptr'] - artifice_ptr_over
			card['artifice'] = card['artifice'] - artifice_ptr_over
			ptr_over = ptr_over + artifice_ptr_over
		
		if ptr_over > 0:
			if strength_ptr_over < 0:
				if ptr_over <= (-strength_ptr_over):
					card['strength_ptr'] = card['strength_ptr'] + ptr_over
					card['strength'] = card['strength'] + ptr_over
					ptr_over = 0
				else:
					card['strength_ptr'] = card['strength_ptr'] - strength_ptr_over
					card['strength'] = card['strength'] - strength_ptr_over
					ptr_over = ptr_over + strength_ptr_over
			if (intelligence_ptr_over < 0) and (ptr_over > 0):
				if ptr_over <= (-intelligence_ptr_over):
					card['intelligence_ptr'] = card['intelligence_ptr'] + ptr_over
					card['intelligence'] = card['intelligence'] + ptr_over
					ptr_over = 0
				else:
					card['intelligence_ptr'] = card['intelligence_ptr'] - intelligence_ptr_over
					card['intelligence'] = card['intelligence_ptr'] - intelligence_ptr_over
					ptr_over = ptr_over + intelligence_ptr_over
			if (artifice_ptr_over < 0) and (ptr_over > 0):
				if ptr_over <= (-artifice_ptr_over):
					card['artifice_ptr'] = card['artifice_ptr'] + ptr_over
					card['artifice'] = card['artifice'] + ptr_over
					ptr_over = 0
				else:
					card['artifice_ptr'] = card['artifice_ptr'] - artifice_ptr_over
					card['artifice'] = card['artifice'] - artifice_ptr_over
					ptr_over = ptr_over + artifice_ptr_over				
					
			
		usr.train_prd = {}
		
		inv.save()
		usr.save()
		return {'training_card':inv.getClientCard(card)}
	
	
	@staticmethod		
	def decompose(usr, cardids):
		"""
		分解
		"""
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
			if inv.delCard(cardid) != 1:
				return {'msg':'decompose_faild'}
			
		usr.trp = usr.trp + total_trp
		
		usr.save()
		inv.save()
		return {'trp':usr.trp, 'delete_card_array':cardids}
			
		
		
	@staticmethod
	def sell(usr, id):
		"""
		出售
		"""	
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
		"""
		转生
		"""
		
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
		if not card:
			return {'msg':'card_not_exist'}
		
		rebornInfo = None
		for r in rebornConf:
			if r['star_max'] > card['init_star']:
				rebornInfo = r
				break
			if not card.has_key('reborn_level'):
				card['reborn_level'] = 0
			if r['level'] > card['reborn_level']:
				rebornInfo = r
				break
		
		if not rebornInfo:
			return {'msg':'reborn_can_not'}
				
		if rebornInfo['level'] > card['level']:
			return {'msg':'reborn_level_required'}
			
		if not card.has_key('reborn_level'):
			card['reborn_level'] = 0
		if not card.has_key('reborn_count'):
			card['reborn_count'] = 0
				
		card['init_star'] = card['init_star'] = pet.reborn_inc_star(rebornInfo)
		card['reborn_level'] = rebornInfo['level']
		card['reborn_count'] = card['reborn_count'] + 1
		usr.gold = usr.gold - costGold
		inv.save()
		usr.save()
		
		return {'update_card': inv.getClientCard(card), 'gold':usr.gold}		
				
	@staticmethod
	def reborn_inc_star(rebornInfo):
		"""
		转身增加星数
		"""
		rn = randint()
		
		for pb in rebornInfo['star']:
			if rn > pb['probability']:
				rn = rn - pb['probability']
			else: 
				return pb['star']
		return 0

	@staticmethod
	def assembly(usr, cardid):
		"""
		组装
		"""
		
		inv = usr.getInventory()
		
		if not inv.card_chip.has_key(cardid):
			return {'msg':'card_chip_not_enough'}
		
		petConf = config.getConfig('pet')
		
		if not petConf.has_key(cardid):
			return {'msg':'card_chip_not_exist'}
		
		petInfo = petConf[cardid]
		
		if inv.card_chip[cardid] < petInfo['chip']:
			return {'msg':'card_chip_not_enough'}
				
		inv.card_chip[cardid] = inv.card_chip[cardid] - petInfo['chip']
		if inv.card_chip[cardid] == 0:
			del inv.card_chip[cardid]
		card = inv.addCard(cardid)
		inv.save()
		
		if inv.card_chip.has_key(cardid):
			return {'card_chip':{cardid: inv.card_chip[cardid]}, 'add_card':card}
		else:
			return {'card_chip':{cardid: 0}, 'add_card':card}
		
	@staticmethod
	def make_born_card():
		"""
		制做出生卡
		"""
		return {'cardid':'', 'born_time':0}
		
	
	@staticmethod
	def select_born_pet(usr, cardid):
		"""
		选择出生宠物
		"""
		
		gameConf = config.getConfig('game')		
		if cardid not in gameConf['pet_born_candidate']:
			return {'msg': 'card_not_born_card'}				
		if usr.born_card['cardid']:
			return {'msg': 'card_already_get_born_card'}
		
		#awd = {}		
		#awd = drop.open(usr, dropid, awd)
		
		#data = drop.makeData(awd, {})
		inv = usr.getInventory()
		card = inv.addCard(cardid)
		
		usr.born_card['cardid'] = cardid
		usr.born_card['born_time'] = currentTime()		
		
		usr.save()
		
		return {'add_card': card}
		
		
		
			
		
		
		
		