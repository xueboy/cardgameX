#coding:utf-8
#!/usr/bin/env python

from gclib.utility import randint
from game.utility.config import config


class potential:
	
	@staticmethod
	def onEveryPetLevelup(usr, card, petConf):
		"""
		每次宠物升级时
		"""
	
		petInfo = petConf[card['cardid']]
		potentialConf = config.getConfig('potential')
		
		if not card.has_key('pt_potential'):
			card['pt_potential'] = 0
		if not card.has_key('pd_potential'):
			card['pd_potential'] = 0
		if not card.has_key('md_potential'):
			card['md_potential'] = 0
		potential = potentialConf['point'][petInfo['quality'] - 1]
		card['pt_potential'] = card['pt_potential'] + potential
		card['pd_potential'] = card['pd_potential'] + potential
		card['md_potential'] = card['md_potential'] + potential
		
		
	
	@staticmethod
	def fire(usr ,id, useGem):
		"""
		潜能激发
		"""
		
		inv = usr.getInventory()
	
		card = inv.getCard(id)
		if not card:
			return {'msg':'card_not_exist'}
		
		gameConf = config.getConfig('game')
		
		it = inv.getItemByType(gameConf['potential_item'])
		if not it:
			return {'msg':'item_not_exist'}
		updateIt = inv.delItem(it['id'])
		
		potentialConf = config.getConfig('potential')
				
		pt_point = 0
		pd_point = 0
		md_point = 0
		
		rd = randint()
		for item in potentialConf['probability']:
			if useGem:
				if rd > item['gem_probability']:
					rd = rd - item['gem_probability']
				else:
					pt_point = item['point']
			else:
				if rd > item['probability']:
					rd = rd - item['probability']
				else:
					pt_point = item['point']
		
		rd = randint()
		for item in potentialConf['probability']:
			if useGem:
				if rd > item['gem_probability']:
					rd = rd - item['gem_probability']
				else:
					pd_point = item['point']
			else:
				if rd > item['probability']:
					rd = rd - item['probability']
				else:
					pd_point = item['point']
		
		rd = randint()
		for item in potentialConf['probability']:
			if useGem:
				if rd > item['gem_probability']:
					rd = rd - item['gem_probability']
				else:
					md_point = item['point']
			else:
				if rd > item['probability']:
					rd = rd - item['probability']
				else:
					md_point = item['point']

		if not card.has_key('pt'):
			card['pt'] = 0
		if not card.has_key('pd'):
			card['pd'] = 0
		if not card.has_key('md'):
			card['md'] = 0
			
		if not card.has_key('pt_potential'):
			card['pt_potential'] = 0
		if not card.has_key('pd_potential'):
			card['pd_potential'] = 0
		if not card.has_key('md_potential'):
			card['md_potential'] = 0

		if card['pt_potential'] < pt_point:
			pt_point = card['pt_potential']
		if card['pd_potential'] < pd_point:
			pd_point = card['pd_potential']
		if card['md_potential'] < md_point:
			md_point = card['md_potential']
							
		goldCost = 0
		gemCost = 0		
		
		potentialPriceConf = config.getConfig('potential_price')
		
		if useGem:
			gemCost = gameConf['potential_gem_price']
		else:
			goldCost = potentialPriceConf[usr.level - 1]
			
		if gemCost > usr.gem:
			return {'msg': 'gem_not_enough'}
		if goldCost > usr.gold:
			return {'msg': 'gold_not_enough'}
				
		if not card.has_key('pt'):
			card['pt'] = 0
		if not card.has_key('pd'):
			card['pd'] = 0
		if not card.has_key('md'):
			card['md'] = 0
				
		card['pt_potential'] = card['pt_potential'] - pt_point
		card['pt'] = card['pt'] + pt_point
		card['pd_potential'] = card['pd_potential'] - pd_point
		card['pd'] = card['pd'] + pd_point
		card['md_potential'] = card['md_potential'] - md_point
		card['md'] = card['md'] + md_point
		
		if card['pt'] < 0:
			card['pt'] = 0
		if card['pd'] < 0:
			card['pd'] = 0
		if card['md'] < 0:
			card['md'] = 0
		
		usr.save()
		inv.save()
		if updateIt:
			return {'card_update':card, 'gold':usr.gold, 'gem':usr.gem, 'update_item':updateIt}
		else:
			return {'card_update':card, 'gold':usr.gold, 'gem':usr.gem, 'delete_item':it['id']}
		