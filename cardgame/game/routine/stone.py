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
		
		goldCost = stoneProbabilityConf['visitPrice'][inv.stv]
		
		if goldCost > usr.gold:
			return {'msg':'gold_not_enough'}
		usr.gold = usr.gold - goldCost
		
		probs = {}
		if useGem:
			probs = stoneProbabilityConf['visit'][inv.stv]['gem']
		else:
			probs = stoneProbabilityConf['visit'][inv.stv]['gold']
			
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
		
		if drop(stoneProbabilityConf['visitProb'][inv.stv]):
			inv.stv = inv.stv + 1
		else:
			inv.stv = inv.stv - 1
			if inv.stv < 0:
				inv.stv = 0
		
		