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
		
		return {'stv':usr.stv, 'stone':stone, 'gold':usr.gold}
		
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
		
		return {'stv':usr.stv, 'stone':stone, 'gem':usr.gem}
			
		
	def levelup(usr, ds, mt):
		
		for mtid in mt:
			
		
		