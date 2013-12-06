#coding:utf-8
#!/usr/bin/env python

import random
from gclib.utility import randint, currentTime, is_same_day
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
		
		now = currentTime()
		garcha.update_garcha(usr, now)
		
		garchaInfo = None
		if garchaAmount == 10:
			garchaInfo = usr.garcha['garcha10']
		elif garchaAmount == 100:
			garchaInfo = usr.garcha['garcha100']
		elif garchaAmount == 10000:
			garchaInfo = usr.garcha['garcha10000']
				
		isFirstTime = (garchaInfo['last_time'] == 0)
		isFree = False
		duration = now - garchaInfo['last_time']
		cooldownConf = 0
		cooldown = 0
		isCooldown = False
		if garchaAmount == 10:
			cooldownConf = gameConf['garcha_10_cooldown']
		if garchaAmount == 100:
			cooldownConf = gameConf['garcha_100_cooldown']
		if garchaAmount == 10000:
			cooldownConf = gameConf['garcha_10000_cooldown']
		
		cooldown = cooldownConf - duration
		
		if cooldown > 0:
			isCooldown = True
		else:
			isCooldown = False
			cooldown = 0
		
		if garchaAmount == 10:
			isFree = ((gameConf['garcha_10_times'] - garchaInfo['count']) > 0) and not isCooldown
		elif garchaAmount == 100:
			isFree = ((gameConf['garcha_100_times'] - garchaInfo['count']) > 0) and not isCooldown
		elif garchaAmount == 10000:
			isFree = ((gameConf['garcha_10000_times'] - garchaInfo['count']) > 0) and not isCooldown
			
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
		cata = 0
		if (not isFirstTime) or garchaAmount == 10:
			prob = garcha_prob_table[garchaType]
			cata = garcha.garcha_cata(prob)			
		else:
			if garchaAmount == 100:
				cata = 1				
			elif garchaAmount == 10000:
				cata = 2
		cataConf = garchaConf[cata]
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
		if isFree:
			garchaInfo['last_time'] = now
			garchaInfo['count'] = garchaInfo['count'] + 1
			
		duration = now - garchaInfo['last_time']		
		cooldown = cooldownConf - duration
		data = {}
		data['garcha_card'] = garchaCard
		data['gold'] = usr.gold
		data['gem'] = usr.gem		
	
		if garchaAmount == 10:
			data['garcha10'] = {}
			data['garcha10']['count'] = garchaInfo['count']
			data['garcha10']['cooldown'] = cooldown			
		elif garchaAmount == 100:
			data['garcha100'] = {}
			data['garcha100']['count'] = garchaInfo['count']
			data['garcha100']['cooldown'] = cooldown			
		elif garchaAmount == 10000:
			data['garcha10000'] = {}
			data['garcha10000']['count'] = garchaInfo['count']
			data['garcha10000']['cooldown'] = cooldown
		
		usr.save()
		inv.save()
		return data
	
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
			
	@staticmethod
	def update_garcha(usr, now):
		
		if not is_same_day(now, usr.garcha['garcha10']['last_time']):
			usr.garcha['garcha10']['count'] = 0
		if not is_same_day(now, usr.garcha['garcha100']['last_time']):
			usr.garcha['garcha100']['count'] = 0
		if not is_same_day(now, usr.garcha['garcha10000']['last_time']):
			usr.garcha['garcha10000']['count'] = 0
			
		usr.save()