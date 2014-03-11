#coding:utf-8
#!/usr/bin/env python

import random
from gclib.utility import randint, currentTime, is_same_day
from game.utility.config import config
from game.routine.drop import drop
from game.routine.vip import vip


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
		"""
		一次求将
		"""
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
		garchaDropid1 = ''
		garchaDropid2 = ''
		garchaDropid3 = ''
		time_score = 0
		luck_score = 0
		petConf = config.getConfig('pet')
		
		if not isFree:
			if garchaAmount == 10:
				garchaCostGold = gameConf['garcha_10_price']['gold']
				garchaCostGem = gameConf['garcha_10_price']['gem']
				garchaType = 'garcha_10'
				garchaDropid1 = gameConf['garcha_10_dropid1']				
			elif garchaAmount == 100:
				garchaCostGold = gameConf['garcha_100_price']['gold']
				garchaCostGem = gameConf['garcha_100_price']['gem']
				garchaType = 'garcha_100'
				garchaDropid2 = gameConf['garcha_100_dropid2']
				garchaDropid1 = gameConf['garcha_100_dropid1']
				garchaDropid3 = gameConf['garcha_100_dropid3']
				time_score = garchaConf[vip.level(usr)]['garcha_100_free_time_score']
				luck_score = garchaConf[vip.level(usr)]['garcha_100_free_luck_score']
				if not garchaInfo.has_key('time_score'):
					garchaInfo['time_score'] = 0
				if not garchaInfo.has_key('luck_score'):
					garchaInfo['luck_score'] = 0					
				
			elif garchaAmount == 10000:
				garchaCostGold = gameConf['garcha_10000_price']['gold']
				garchaCostGem = gameConf['garcha_10000_price']['gem']
				garchaDropid1 = gameConf['garcha_10000_dropid1']
				garchaDropid2 = gameConf['garcha_10000_dropid2']
				garchaDropid3 = gameConf['garcha_10000_dropid3']
				time_score = garchaConf[vip.level(usr)]['garcha_10000_free_time_score']
				luck_score = garchaConf[vip.level(usr)]['garcha_10000_free_luck_score']
				if not garchaInfo.has_key('time_score'):
					garchaInfo['time_score'] = 0
				if not garchaInfo.has_key('luck_score'):
					garchaInfo['luck_score'] = 0
				garchaType = 'garcha_10000'
			if inv.CountCardByQuality(5, petConf) > 0:			 
					time_score = int(time_score / 2)
		else:
			if garchaAmount == 10:
				garchaType = 'garcha_10_free'
				garchaDropid1 = gameConf['garcha_10_dropid1']		
			elif garchaAmount == 100:
				garchaType = 'garcha_100_free'
				garchaDropid2 = gameConf['garcha_100_dropid2']
				garchaDropid1 = gameConf['garcha_100_dropid1']
				garchaDropid3 = gameConf['garcha_100_dropid3']
				time_score = garchaConf[vip.level(usr)]['garcha_100_time_score']
				luck_score = garchaConf[vip.level(usr)]['garcha_100_luck_score']
				if not garchaInfo.has_key('time_score'):
					garchaInfo['time_score'] = 0
				if not garchaInfo.has_key('luck_score'):
					garchaInfo['luck_score'] = 0
			elif garchaAmount == 10000:
				garchaType = 'garcha_10000_free'
				garchaDropid1 = gameConf['garcha_10000_dropid1']
				garchaDropid2 = gameConf['garcha_10000_dropid2']
				garchaDropid3 = gameConf['garcha_10000_dropid3']
				time_score = garchaConf[vip.level(usr)]['garcha_10000_time_score']
				luck_score = garchaConf[vip.level(usr)]['garcha_10000_luck_score']
				if not garchaInfo.has_key('time_score'):
					garchaInfo['time_score'] = 0
				if not garchaInfo.has_key('luck_score'):
					garchaInfo['luck_score'] = 0
			fatigue = inv.CountCardByQuality(5, petConf)
			if fatigue > 5:
				fatigue = 5
			time_score = int(time_score / (1 + fatigue))
		if usr.gold < garchaCostGold:
			return {'msg':'gold_not_enough'}
		if usr.gem < garchaCostGem:
			return {'msg':'gem_not_enough'}			

		awd = {}
		if garchaAmount == 10:			
			awd = drop.open(usr, garchaDropid1, awd)
		else:
			awd = {}
			if garchaInfo['time_score'] >= 800:
				rd = randint()
				if (rd <= 300) or (garchaInfo['time_score'] >= 1200):
					if garchaInfo['luck_score'] < 96:
						awd = drop.open(usr, garchaDropid2, awd)
					else:
						rd = randint()
						if rd < 5000:
							awd = drop.open(usr, garchaDropid3, awd)
						else:
							awd = drop.open(usr, garchaDropid2, awd)	
					garchaInfo['time_score'] = 0
					garchaInfo['luck_score'] = 0
					time_score = 0
					luck_score = 0
				else:
					awd = drop.open(usr, garchaDropid1, awd)
			else: 
				awd = drop.open(usr, garchaDropid1, awd)	
					
		data = drop.makeData(awd, {})
				
		usr.gold = usr.gold - garchaCostGold
		usr.gem = usr.gem - garchaCostGem
		if isFree:
			garchaInfo['last_time'] = now
			garchaInfo['count'] = garchaInfo['count'] + 1
		
		if time_score or luck_score:
			garchaInfo['time_score'] = garchaInfo['time_score'] + time_score
			garchaInfo['luck_score'] = garchaInfo['luck_score'] + luck_score
			
		duration = now - garchaInfo['last_time']
		cooldown = cooldownConf - duration		
		data['gold'] = usr.gold
		data['gem'] = usr.gem	
		
		data['garcha'] = {}
		data['garcha']['count'] = garchaInfo['count']
		data['garcha']['cooldown'] = cooldown
		
		usr.save()
		inv.save()
		return data
	
	@staticmethod	
	def garcha_cata(prob):
		"""
		求将分类
		"""
		r = randint()
		for i in range(len(prob)):
			if prob[i] > r:
		 		return i
			else: 
		 		r = r - prob[i]		 		
		return -1	
	
	@staticmethod
	def make():
		"""
		制做
		"""
		return {'garcha10':{'count': 0, 'last_time': 0},'garcha100':{'count': 0, 'last_time': 0, 'time_score':0, 'luck_score':0},'garcha10000':{'count': 0, 'last_time': 0, 'time_score':0, 'luck_score':0}}
			
	@staticmethod
	def update_garcha(usr, now):
		"""
		更新求将
		"""
		if not is_same_day(now, usr.garcha['garcha10']['last_time']):
			usr.garcha['garcha10']['count'] = 0
		if not is_same_day(now, usr.garcha['garcha100']['last_time']):
			usr.garcha['garcha100']['count'] = 0
		if not is_same_day(now, usr.garcha['garcha10000']['last_time']):
			usr.garcha['garcha10000']['count'] = 0			
		usr.save()
		
	@staticmethod
	def getClientData(usr, gameConf):
		"""
		得到客户端数据
		"""
		data = {}
		data['garcha'] = {}
		cooldown = 0
		now = currentTime()
		data['garcha']['10'] = {}
		data['garcha']['10']['count'] = usr.garcha['garcha10']['count']
		cooldown = gameConf['garcha_10_times'] - (now - usr.garcha['garcha10']['last_time'])
		data['garcha']['10']['cooldown'] = cooldown
		if cooldown < 0:
			data['garcha']['10']['cooldown'] = 0
		data['garcha']['100'] = {}
		data['garcha']['100']['count'] = usr.garcha['garcha100']['count']
		cooldown = gameConf['garcha_100_times'] - (now - usr.garcha['garcha100']['last_time'])
		data['garcha']['100']['cooldown'] = cooldown
		if cooldown < 0:
			data['garcha']['100']['cooldown'] = 0
		data['garcha']['10000'] = {}
		data['garcha']['10000']['count'] = usr.garcha['garcha10000']['count']
		cooldown = gameConf['garcha_10000_times'] - (now - usr.garcha['garcha10000']['last_time'])
		data['garcha']['10000']['cooldown'] = cooldown
		if cooldown < 0:
			data['garcha']['10000']['cooldown'] = 0
		return data
		
	@staticmethod
	def garcha_skill10(usr):
		"""
		求技能10次
		"""
		
		gameConf = config.getConfig('game')
		
		goldCost = gameConf['garcha_skill_10_price']['gold']
		gemCost = gameConf['garcha_skill_10_price']['gem']
		
		if usr.gold < goldCost:
			return {'msg':'gold_not_enough'}
		if usr.gem < gemCost:
			return {'msg':'gem_not_enough'}	
				
		awd = {}
		awd = drop.open(usr, gameConf['garcha_skill_10_dropid1'], awd)
		
		for i in range(9):
			awd = drop.open(usr, gameConf['garcha_skill_10_dropid2'], awd)
					
		data = drop.makeData(awd, {})
		
		usr.gold = usr.gold - goldCost
		usr.gem = usr.gem - gemCost
		
		usr.save()
		
		data['gold'] = usr.gold
		data['gem'] = usr.gem
		return data
				
		
	@staticmethod
	def garcha_skill(usr, nature):
		"""
		求技能
		"""
		gameConf = config.getConfig('game')
		
		if (nature > len(gameConf['garcha_skill_dropid'])) or (nature < 0):
			return {'msg':'parameter_bad'}
				
		goldCost = gameConf['garcha_skill_price'][nature - 1]['gold']
		gemCost = gameConf['garcha_skill_price'][nature - 1]['gem']
		
		if int(goldCost) == 0 and int(gemCost) == 0:
			return {'msg':'parameter_bad'}
		
		if usr.gold < goldCost:
			return {'msg':'gold_not_enough'}
		if usr.gem < gemCost:
			return {'msg':'gem_not_enough'}	
				
		awd = {}
		awd = drop.open(usr, gameConf['garcha_skill_dropid'][nature - 1], awd)	
			
		data = drop.makeData(awd, {})
		
		usr.gold = usr.gold - goldCost
		usr.gem = usr.gem - gemCost
		
		data['gold'] = usr.gold
		data['gem'] = usr.gem
		return data