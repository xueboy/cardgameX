#coding:utf-8
#!/usr/bin/env python

import random

from gclib.utility import drop, randint
from game.utility.config import config

class stone:
	
	@staticmethod
	def visit(usr, level):
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')
		
		if level > len(usr.stv):
			return {'msg':'svt_too_hight'}
		
		if not usr.stv[level - 1]:
			return {'msg':'svt_not_available'}			
	
		result = []	
		msg = stone.do_visit(usr, level, result, gameConf,stoneProbabilityConf)		
		usr.save()
		inv.save()
		
		if msg:
			return msg		
		data = result[0]
		data['gold'] = usr.gold		
		return data
		
	@staticmethod
	def visit_gem(usr, level):
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')
				
		if level > len(usr.stv):
			return {'msg':'svt_too_hight'}
				
		gemCost = stoneProbabilityConf['visitGem'][level - 1]		
		
		if not gemCost:
			return {'msg':'stone_visit_level_gem_not_allow'}
		if gemCost > usr.gem:
			return {'msg':'gem_not_enough'}
				
		probs = stoneProbabilityConf['visit'][level - 1]['gem']
			
		seed = randint()		
		cndStone = []
						
		for prob in probs:
			p = prob['probability'] 
			if p > seed:
				cndStone = prob['stone']
				break
			else:
				seed = seed - p				
				
		stoneid = random.sample(cndStone, 1)[0]
		stone = inv.addStone(stoneid)	
		
		usr.stv_gem[level - 1] = 0
		if level < len(usr.stv):
			usr.stv_gem[level] = 1
			usr.stv[level] = 1		
				
		usr.gem = usr.gem - gemCost
				
		usr.save()
		inv.save()
		
		return {'stv':usr.stv, 'add_stone':stone, 'gem':usr.gem}
			
	@staticmethod
	def visit_clickonce(usr, count):	
		
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')		
		level = stone.max_available_stv(usr)
		
		result = []		
		for i in range(count):
			msg = stone.do_visit(usr, level, result, gameConf, stoneProbabilityConf)
			if msg:
				break
			level = stone.max_available_stv(usr)		
		usr.save()
		inv.save()
		if result:
			return {'result':result, 'gold':usr.gold}
		return msg			
		
	@staticmethod
	def max_available_stv(usr):
		if usr.stv[4]:
			return 5
		if usr.stv[3]:
			return 4
		if usr.stv[2]:
			return 3
		if usr.stv[1]:
			return 2
		if usr.stv[0]:
			return 1
		
	@staticmethod
	def do_visit(usr, level, result, gameConf,stoneProbabilityConf):
		inv = usr.getInventory()			
		
		goldCost = stoneProbabilityConf['visitGold'][level - 1]		
		
		if goldCost > usr.gold:
			return {'msg':'gold_not_enough'}
		if usr.stv_gem[level - 1]:
			probs = stoneProbabilityConf['visit'][level - 1]['gem']			
		else:
			probs = stoneProbabilityConf['visit'][level - 1]['gold']
			
		seed = randint()		
		cndStone = []
						
		for prob in probs:
			p = prob['probability'] 
			if p > seed:
				cndStone = prob['stone']
				break
			else:
				seed = seed - p				
				
		stoneid = random.sample(cndStone, 1)[0]
		stone = inv.addStone(stoneid)	
				
		if drop(stoneProbabilityConf['visitProb'][level - 1]):
			usr.stv[level] = 1
			usr.stv_gem[level - 1] = 0		
		usr.stv[level - 1] = 0	
		usr.stv[0] = 1				
		usr.gold = usr.gold - goldCost		
		result.append({'stv':usr.stv[:], 'add_stone':stone})
		return {}
		
			
	@staticmethod
	def levelup(usr, dest_stoneid, source_stoneid):
			
		if not source_stoneid:
			return {'msg':'stone_not_specified'}
				
		stoneConf = config.getConfig('stone')
				
		inv = usr.getInventory()		
		dest_stone = inv.getStone(dest_stoneid)	
		if not dest_stone:
			return {'msg':'stone_not_exist'}
		exp = 0
				
		for srcid in source_stoneid:			
			ss = inv.getStone(srcid)			
			if not ss:
				return {'msg':'stone_not_exist'}			
			exp = exp + stone.get_exp(ss, stoneConf[ss['stoneid']])			
			inv.delStone(srcid)				
		
		stone.add_exp(dest_stone, exp, stoneConf[dest_stone['stoneid']])
		inv.save()		
		return {'stone':dest_stone, 'stone_delete_array':source_stoneid}
		
	@staticmethod
	def add_exp(st, exp, stoneInfo):
		stoneLevelConf = config.getConfig('stone_level')		
		
		expdeff = stoneLevelConf[unicode(st['level'] + 1)][stoneInfo['quality'] - 1] - stoneLevelConf[unicode(st['level'])][stoneInfo['quality'] - 1]
		exp = exp + st['exp']
		st['exp'] = 0
		while expdeff < exp:
			st['level'] = st['level'] + 1
			exp = exp - expdeff
			expdeff = stoneLevelConf[unicode(st['level'])][stoneInfo['quality'] - 1] - stoneLevelConf[unicode(st['level'] - 1)][stoneInfo['quality'] - 1]
			
		st['exp'] = exp
			
	@staticmethod
	def get_exp(st, stoneInfo):
		stoneLevelConf = config.getConfig('stone_level')
		exp = st['exp']
		exp = exp + stoneLevelConf[unicode(st['level'])][stoneInfo['quality'] - 1]
		exp = exp + stoneInfo['gravel']
		return exp
		
	@staticmethod
	def make_stv():
		return [1, 0, 0, 0, 0]

	@staticmethod
	def install(usr, teamPosition, slotpos, stoneid):
		
		inv = usr.getInventory()
		
		if not inv.team[teamPosition]:
			return {'msg':'team_position_not_have_member'}				
		card = inv.getCard(inv.team[teamPosition])
		if not card:
			return {'msg': 'card_not_exist'}		
		gameConf = config.getConfig('game')		
		if gameConf['stone_slot_level'][slotpos] > card['level']:
			return {'msg': 'card_level_required'}
		
		if not card.has_key('st_slot'):
			card['st_slot'] = stone.make_st_solt()
	
		stoneConf = config.getConfig('stone')		
		st = {}
		if stoneid:
			st = inv.withdrawStone(stoneid)			
		oldst = card['st_slot'][slotpos]
		if (not oldst) and (not stoneid):
			return {'msg':'stone_not_exist'}
			
		sttype = stoneConf[st['stoneid']][type]			
		for st1 in card['st_slot']:
			if st1 and stoneConf[st1['stoneid']]['type'] == sttype:
				return {'msg':'stone_same_type_installed'}				
		
		card['st_slot'][slotpos] = st		
		if oldst:
			inv.depositStone(oldst)		
		inv.save()			
		data = {}		
		data['st_slot'] = inv.getStSlots()
		if oldst:
			data['add_stone'] = oldst			
		if st:
			data['delete_stone'] = st
			
		return data		
		
	@staticmethod
	def make_st_solt():
		return [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
		
	@staticmethod
	def takeoff(inv, card):
		dst = []
		if card and card.has_key('st_slot'):
			for st in card['st_slot']:
				if st:
					inv.depositStone(st)
					dst.append(st)
			del card['st_slot']

	@staticmethod
	def exchage(inv, fromCard, toCard, gameConf):				
				
		toSlot = None		
		if toCard.has_key('st_slot'):
			toSlot = toCard['st_slot']			
		toCard['st_slot'] = fromCard['st_slot']
		del fromCard['st_slot']
		dst = []
		if toSlot:
			fromCard['st_slot'] = toSlot			
			for i, ts in enumerate(fromCard['st_slot']):
				if ts and gameConf['stone_slot_level'][i] > fromCard['level']:
					inv.depositStone(ts)
					dst.append(ts)
					fromCard['st_slot'][i] = {}
		
		for i, ts in enumerate(toCard['st_slot']):			
			if ts and gameConf['stone_slot_level'][i] > toCard['level']:
					inv.depositStone(ts)
					dst.append(ts)
					toCard['st_slot'][i] = {}		
		return dst