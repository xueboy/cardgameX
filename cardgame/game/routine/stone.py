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
		
		usr.save()
		inv.save()
		
		return {'stv':usr.stv, 'add_stone':stone, 'gold':usr.gold}
		
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
		
	def set_stone(usr, cardid, soltpos, stoneid):
		
		gameConf = config.getConfig('game')
		inv = usr.getInventory()
		
		p = inv.getCard(cardid)
		
		if gameConf['stone_slot_level'][soltpos] > p['level']:
			return {'msg':'card_level_required'}
		
		if (not p.has_key('st_solt')) and (not stoneid):
			p['st_solt'] = sonte.make_st_solt()
		
		oldst = p['st_solt'][soltpos]
		st = None
		if stoneid:		
			st = inv.getStone(stoneid)
			if not st:
				return {'msg':'stone_not_exist'}
			inv.delStone(st['id'])
			p['st_solt'][soltpos] = st			
		else:
			emp = True
			for s in p['st_solt']:
				if s:
					emp = False
			if emp:
				del p['st_solt']				
		
		if oldst:
				inv.depositStone(oldst)
				
		inv.save()
				
		data = {}
		data['card'] = p
		if oldst:
			data['add_stone'] = oldst
		if st:
			data['stone'] = st
		return data	
		
	@staticmethod
	def make_st_solt():
		return [{}, {}, {}, {}, {}, {}, {}, {}, {}, {},]
		
			