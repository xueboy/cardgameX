#coding:utf-8
#!/usr/bin/env python

import random
from gclib.utility import randint
from game.utility.config import config

garcha_prob_table = {
	'garcha_10_free':[8000, 2000, 0, 0, 0],
	'garcha_10':[8000, 2000, 0, 0, 0],
	'garcha_100_free':[0, 8200, 1500, 300, 0],
	'garcha_100':[0, 7500, 2000, 500, 0],
	'garcha_10000_free':[0, 7000, 3000, 1000, 0],
	'garcha_10000':[0, 6500, 4000, 1500, 0]
}

class garcha:
	
	@staticmethod
	def garcha_once(usr, garchaAmount):		
		inv = usr.getInventory()
		garchaConf = config.getConfig('garcha')
		gameConf = config.getConfig('game')
		
		garchaInfo = None
		if garchaAmount == 10:
			garchaInfo = usr.garcha['garcha10']
		elif garchaAmount == 100:
			garchaInfo = usr.garcha['garcha100']
		elif garchaAmount == 10000:
			garchaInfo = usr.garcha['garcha10000']
				
		isFirstTime = (garchaInfo['last_time'] == 0)
		isFree = False
		if garchaAmount == 10:
			isFree = ((garchaInfo['count'] - gameConf['garcha_10_times']) > 0) and ((currentTime() - garchaInfo['last_time']) > gameConf['garcha_10_cooldown'])
		elif garchaAmount == 100:
			isFree = ((garchaInfo['count'] - gameConf['garcha_100_times']) > 0) and ((currentTime() - garchaInfo['last_time']) > gameConf['garcha_100_cooldown'])
		elif garchaAmount == 10000:
			isFree = ((garchaInfo['count'] - gameConf['garcha_10000_times']) > 0) and ((currentTime() - garchaInfo['last_time']) > gameConf['garcha_10000_cooldown'])
			
		garchaCostGold = 0
		garchaCostGem = 0
		garchaType = ''
		if not isFree:
			if garchaAmount == 10:
				garchaCostGold = gameConf['garcha_10_price']['gold']
				garchaCostGem = gameConf['garcha_10_price']['gem']
				garchaType = 'garcha_10'
			elif garchaAmount == 100:
				garchaCostGold = gameConf['garcha_100_price']['gold']
				garchaCostGem = gameConf['garcha_100_price']['gem']
				garchaType = 'garcha_100'
			elif garchaAmount == 10000:
				garchaCostGold = gameConf['garcha_10000_price']['gold']
				garchaCostGem = gameConf['garcha_10000_price']['gem']
				garchaType = 'garcha_10000'
		else:
			if garchaAmount == 10:
				garchaType = 'garcha_10_free'
			elif garchaAmount == 100:
				garchaType = 'garcha_100_free'
			elif garchaAmount == 10000:
				garchaType = 'garcha_10000_free'
		
		if usr.gold < garchaCostGold:
			return {'msg':'gold_not_enough'}
		if usr.gem < garchaCostGem:
			return {'msg':'gem_not_enough'}			
		
		cataConf = None
		if (not isFirstTime) or garchaAmount == 10:
			prob = garcha_prob_table[garchaType]
			cata = garcha.garcha_cata(prob)
			cataConf = garchaConf[cata]
		else:
			if garchaAmount == 100:
				cata = garchaConf[1]
			elif garchaAmount == 10000:
				cata = garchaConf[2]
		
		r = random.randint(0, cataConf['totalProb'] - 1)
		garchaCard = None
		for card in cataConf['card']:
			if r >  card['prob']:
				r = r - card['prob']
			else:
				garchaCard = inv.addCard(card['cardId'], card['level'])
				break;
		
		if not garchaCard:
			return {'msg': 'card_not_exist'}
		
		usr.gold = usr.gold - garchaCostGold
		usr.gem = usr.gem - garchaCostGem
		usr.save()
		inv.save()
		return {'garcha_card':garchaCard, 'gold':usr.gold, 'gem':usr.gem }
	
	@staticmethod	
	def garcha_cata(prob):
		 r = randint()
		 for i in range(len(prob)):
		 	if prob[i] > r:
		 		return i
		 	else: 
		 		r = r - prob[i]		 		
		 return -1	
	
	@staticmethod
	def make():
		return {'garcha10':{'count': 0, 'last_time': 0},'garcha100':{'count': 0, 'last_time': 0},'garcha10000':{'count': 0, 'last_time': 0}}