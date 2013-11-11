#coding:utf-8
#!/usr/bin/env python

import random

from gclib.utility import drop, randint
from game.utility.config import config

class stone:
	
	def visit(usr, useGem):
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')
		
		goldCost = stoneProbabilityConf['visitPrice'][usr.stv]
		
		if goldCost > usr.gold:
			return {'msg':'gold_not_enough'}
		usr.gold = usr.gold - goldCost
		
		probs = {}
		if useGem:
			probs = stoneProbabilityConf['visit'][usr.stv]['gem']
		else:
			probs = stoneProbabilityConf['visit'][usr.stv]['gold']
			
		seed = randint()		
		cndStone = []
		
		for prob in probs:
			p = prob['probability'] 
			if p > seed:
				cndStones = prob['stone']
				break
			else:
				seed = seed - p				
				
		stoneid = random.simple(cndStone, 1)		
		stone = inv.addStone(stoneid)	
		
		if drop(stoneProbabilityConf['visitProb'][usr.stv]):
			inv.stv = usr.stv + 1
		else:
			inv.stv = usr.stv - 1
			if inv.stv < 0:
				inv.stv = 0
				
		usr.save()
		inv.save()
		return {'stv':usr.stv, 'gold':usr.gold, 'stone':stone}
		
		