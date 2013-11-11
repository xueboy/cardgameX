#coding:utf-8
#!/usr/bin/env python

import random

from gclib.utility import drop, randint
from game.utility.config import config

class stone:
	
	@staticmethod
	def visit(usr):
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')
		
		goldCost = stoneProbabilityConf['visitGold'][usr.stv]		
		
		
		if goldCost > usr.gold:
			return {'msg':'gold_not_enough'}
		if usr.stv_gem_level != -1:
			probs = stoneProbabilityConf['visit'][usr.stv]['gem']			
		else:
			probs = stoneProbabilityConf['visit'][usr.stv]['gold']
			
		seed = randint()		
		cndStone = []
						
		for prob in probs:
			p = prob['probability'] 
			if p > seed:
				cndStone = prob['stone']
				break
			else:
				seed = seed - p				
				
		stoneid = random.sample(cndStone, 1)		
		stone = inv.addStone(stoneid[0])	
		
		if drop(stoneProbabilityConf['visitProb'][usr.stv]):
			usr.stv = usr.stv + 1
		else:
			usr.stv = usr.stv - 1
			if usr.stv < 0:
				usr.stv = 0
		
		usr.gold = usr.gold - goldCost		
		usr.stv_gem_level = -1					
		usr.save()
		inv.save()
		
		return {'stv':usr.stv, 'stone':stone, 'gold':usr.gold}
		
	@staticmethod
	def visit_level(usr, level):
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')
				
		gemCost = stoneProbabilityConf['visitGem'][level]		
		
		if not gemCost:
			return {'msg':'stone_visit_level_gem_not_allow'}
		if gemCost > usr.gem:
			return {'msg':'gem_not_enough'}
		usr.stv_gem_level = usr.stv		
		
		probs = stoneProbabilityConf['visit'][usr.stv]['gem']
			
		seed = randint()		
		cndStone = []
						
		for prob in probs:
			p = prob['probability'] 
			if p > seed:
				cndStone = prob['stone']
				break
			else:
				seed = seed - p				
				
		stoneid = random.sample(cndStone, 1)		
		stone = inv.addStone(stoneid[0])	
		
		usr.stv_gem_level = usr.stv
		usr.stv = level + 1
		if usr.stv > len(probs):
			usr.stv = len(probb)
				
		usr.gem = usr.gem - gemCost
				
		usr.save()
		inv.save()
		
		return {'stv':usr.stv, 'stone':stone, 'gem':usr.gem}
		
		