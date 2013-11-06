#coding:utf-8
#!/usr/bin/env python

from gclib.utility import is_expire, currentTime, hit, randint
from game.utility import config


class luckycat:
	@staticmethod
	def make():
		data = {}
		data['level'] = 1
		data['exp']
		data['critical'] = []
		data['beckon_count'] = 0
		data['beckon_last_time'] = 0
		data['beckon_cooldown'] = 0
		data['critical_point_list'] = []
		data['feed_self_count'] = 0
		data['feed_self_last_time'] = 0
		data['feed_other_count'] = 0
		data['feed_other_last_time'] = 0		
		data['fatigue'] = 0
		data['bless_roll_last_time'] = 0
		data['bless_cycle_time'] = 0
		data['bless'] = {}
		return data
		
		
	@staticmethod
	def beckon(usr):
		luckycatLevelConf = config.getConfig('luckycat_level')
		gameConf = config.getConfig('game')
		luckycat.updateBeckon(usr)
		if usr.luckycat['beckon_count'] > beckonMaxCount():
			return {'msg':'luckycat_beckon_max_count'}
				
		if usr.luckycat['beckon_cooldown'] > gameConf['luckycat_cooldown_max']:
			return {'msg':'luckycat_beckon_cooldown'}		
		
		
		beckonGold = luckycatLevelConf[usr.luckycat['level'] - 1]['luckyGold']		
		beckonGold = beckonGold * currentLuckycatFortune()		
		if luckycat.isCritical(usr):
			beckonGold = beckonGold * 2		
		usr.gold = usr.gold + beckonGold
		usr.luckycat['beckon_count'] = usr.luckycat['beckon_count'] + 1
		usr.luckycat['fatigue'] = usr.luckycat['fatigue'] + 1
		if usr.luckycat['fatigue'] > gameConfig['luckycat_fatigue_max']:
			usr.luckycat['fatigue'] = gameConfig['luckycat_fatigue_max']
		usr.luckycat['beckon_cooldown'] = usr.luckycat['beckon_cooldown'] + (gameConfig['luckycat_cooldown_base'] * (1 + usr.luckycat['fatigue'] / 2))
		usr.save()
		return {'gold':usr.gold, 'luckycat_beckon_count':usr.luckycat['beckon_count']}	
	
	@staticmethod
	def beckonCooldownCleanup(usr):
		gemCost = usr.luckycat['beckon_cooldown'] / 10
		usr.gem = usr.gem - gemCost
		usr.save()
		return {'gem':usr.gem, 'luckycat_beckon_cooldown':0}
		
	@staticmethod
	def feed(usr, target):
		luckycat.updateFeed()
		gameConf = config.getConfig('game')
		requiredLevel = 0
		feedCountMax = 0
		feedCount = 0
		feedLastTime = 0
		feedCooldown = 0
		feedExp = 0
		feedSelf = False
		now = currentTime()
		feed
		if target:
			requiredLevel = gameConf['luckycat_feed_self_required_level']
			feedCountMax = gameConf['luckycat_feed_self_count_max']
			feedCount = usr.luckycat['feed_self_count']
			feedLastTime = usr.luckycat['feed_self_last_time']
			feedCooldown = gameConf['luckycat_feed_self_cooldown']
			feedExp = gameConf['luckycat_feed_self_exp']
			feedSelf = False
		else:
			requiredLevel = gameConf['luckycat_feed_other_required_level']
			feedCountMax = gameConf['luckycat_feed_other_count_max']
			feedCount = usr.luckycat['feed_other_count']
			feedLastTime = usr.luckycat['feed_other_last_time']
			feedCooldown = usr.luckycat['luckycat_feed_other_cooldown']
			feedExp = gameConf['luckycat_feed_other_exp']
			feedSelf = True
			
		if requiredLevel > usr.luckycat['level']:
			return {'msg':'luckycat_feed_level_required'}
		
		if feedLastTime + feedCooldown > now:
			return {'msg':"luckycat_feed_in_cooldown"}
				
		if not (feedCount < feedCountMax):
			return {'msg':'luckycat_feed_max_time'}					
				
		luckycatLevelConf = config.getConfig('luckycat_level')
		if not target:
			target = usr
			
		target.luckycat['exp'] = target.luckycat['exp'] + feedExp
		
		while target.luckycat['level'] < gameConf['luckycat_max_level'] and luckycatLevelConf[target.luckycat['level'] - 1]['exp'] <= target.luckycat['exp']:
			target['exp'] = target['exp'] - luckycatLevelConf[target.luckycat['level'] - 1]
			target['level'] = target['level'] + 1
		
		awardGold = 0
		awardGem = 0	
		
		if isCritical(usr):
			awardGold = gameConf['luckycat_feed_critical_award']['gold']
			awardGem = gameConf['luckycat_feed_critical_award']['gem']
			
		usr.gold = usr.gold + awardGold
		usr.gem = usr.gem + awardGem		
		
		return {'luckycat': luckycat.getClientData(target), 'gold': usr.gold, 'gem':usr.gem}
			
	@staticmethod
	def rollBless(usr):
		luckycatBlessConf = config.getConfig('luckycat_bless')
		now = currentTime()
		if is_same_day(now, usr.luckycat['bless_roll_last_time']):
			return {'msg':'roll_bless_already_today'}
		
		roll = randint()
		bless = {}
		for blessid in luckycatBlessConf:
			b = luckycatBlessConf[blessid] 
			if b['probability'] < roll:
				roll = roll - b['probability']
			else:
				bless = b
			
		
		
		
		
		
		
	@staticmethod
	def getClientData(usr):
		data = {}
		data['level'] = usr.luckycat['level']
		data['exp'] = usr.luckycat['exp']
		return data
		
	@staticmethod
	def isCritical(usr):
		criticalPoint = sum(usr.luckycat['critical_point_list'])
		probability = criticalPoint / usr.luckycat['level'] * 25
		return drop(probability)
		
	@staticmethod
	def updateBeckon(usr):		
		gameConf = config.getConfig('game')
		if is_expire(gameConf['luckycat_beckon_count_reset_time'], usr.luckycat['beckon_count']):
			usr.luckycat['beckon_count'] = 0
			usr.luckycat['beckon_last_time'] = currentTime()
			
		now = currentTime()
		elapse = now - usr.luckycat['beckon_cooldown']
		usr.luckycat['beckon_cooldown'] = usr.luckycat['beckon_cooldown'] - elapse
		if usr.luckycat['beckon_cooldown'] < 0:
			usr.luckycat['beckon_cooldown'] = 0
			
	@staticmethod
	def updateFeed(usr):
		gameConf = config.getConfig('game')		
		if is_expire(gameConf['luckycat_beckon_count_reset_time'], usr.luckycat['feed_self_last_time']):
			usr.luckycat['feed_self_count'] = 0
			usr.luckycat['feed_self_last_time'] = currentTime()
		if is_expire(gameConf['luckycat_beckon_count_reset_time'], usr.luckycat['feed_other_last_time']):
			usr.luckycat['feed_other_count'] = 0
			usr.luckycat['feed_oter_last_time'] = currentTime()
				
	@staticmethod
	def onLeveup(usr):
		gameConf = config.getConfig('game')
		luckycatLevelConf = config.getConfig('luckycat_level')
		if gameConf['gameConf'].count(usr.luckycat['level']):
			usr.luckycat['critical_point_list'].append(hit(gameConf['luckycat_critical_point_probability']))		
		usr.gold = usr.gold + luckycatLevelConf[usr.luckycat['level']]['levelupGold']
			
			
	@staticmethod
	def freshCritical(usr, itemIndex):
		gameConf = config.getConfig('game')
		goldCost = gameConf['luckycat_critical_item_fresh_price']['gold']
		gemCost = gameConf['luckycat_critical_item_fresh_price']['gem']
		
		if usr.gold < goldCost:
			return {'msg':'gold_not_enough'}
		if usr.gem < gemCost:
			return {'msg':'gem_not_enough'}
				
		usr.gold = usr.gold - goldCost
		usr.gem = usr.gem - gemCost		
		usr.luckycat['critical_point_list'][itemIndex] = hit(gameConf['luckycat_critical_point_probability'])
		
			
	@staticmethod
	def beckonMaxCount(usr):
		gameConf = config.getConfig('game')
		return gameConf['luckycat_beckon_count_base']
		
		
	@staticmethod		
	def currentLuckycatFortune():
		luckycatFortuneConf = config.getConfig('luckycat_fortune')
		now = currentTime()
		daysecond = dayTime()		
		selItem = None
		for item in luckycatFortuneConf:
			if item[0] < daysecond:
				selItem = item
			else:
				break				
		return (selItem[1][0] + selItem[1][2]) / 2