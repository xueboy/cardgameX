#coding:utf-8
#!/usr/bin/env python

from gclib.utility import is_expire, currentTime, hit, randint, dayTime, drop, is_same_day
from game.utility.config import config


class luckycat:
	@staticmethod
	def make():
		data = {}
		data['level'] = 1
		data['exp'] = 0
		data['critical_point_list'] = []
		data['beckon_count'] = 0
		data['beckon_gem_count'] = 0
		data['beckon_last_update_time'] = currentTime()
		data['beckon_cooldown'] = 0
		data['critical_point_list'] = []
		data['feed_self_count'] = 0
		data['feed_self_last_time'] = 0
		data['feed_other_count'] = 0
		data['feed_other_last_time'] = 0		
		data['fatigue'] = 0
		data['bless_roll_last_time'] = 0
		data['bless_cycle_begin_time'] = 0
		data['bless'] = {}
		data['record'] = []
		data['feed_candidate_list'] = []
		data['feed_request_list'] = []
		return data
		
		
	@staticmethod
	def beckon(usr, useGem):
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		luckycatProfitConf = config.getConfig('luckycat_profit')
		gameConf = config.getConfig('game')
		luckycat.updateBeckon(usr)
		if usr.luckycat['beckon_count'] > luckycat.beckonMaxCount(usr) and (not useGem):
			return {'msg':'luckycat_beckon_max_count'}
				
		if usr.luckycat['beckon_cooldown'] > gameConf['luckycat_cooldown_max'] and (not useGem):
			return {'msg':'luckycat_beckon_in_cooldown'}
			
		costGem = 0	
		if useGem:
			costGem = gameConf['luckycat_beckon_gem_base'] + gameConf['luckycat_beckon_gem_delta'] * usr.luckycat['beckon_gem_count']
			if usr.gem < costGem:
				return {'msg':'gem_not_enough'}		
		
		beckonGold = luckycatProfitConf[usr.level - 1]['luckyGold']		
		beckonGold = beckonGold * luckycat.currentLuckycatFortune()
		beckonCritical = False
		if luckycat.isCritical(usr):
			beckonGold = beckonGold * 2		
			beckonCritical = True
		usr.gold = usr.gold + beckonGold
		usr.gem = usr.gem - costGem
		if not useGem:
			usr.luckycat['beckon_count'] = usr.luckycat['beckon_count'] + 1
			usr.luckycat['fatigue'] = usr.luckycat['fatigue'] + 1
			if usr.luckycat['fatigue'] > gameConf['luckycat_fatigue_max']:
				usr.luckycat['fatigue'] = gameConfig['luckycat_fatigue_max']
			usr.luckycat['beckon_cooldown'] = int(usr.luckycat['beckon_cooldown'] + (gameConf['luckycat_cooldown_base'] * (1 + usr.luckycat['fatigue'] / 9.4)))
			usr.luckycat['beckon_last_update_time'] = currentTime()
		rcd = {}
		rcd['type'] = 'beckon'
		rcd['create_time'] = currentTime()
		rcd['income'] = {'gold':beckonGold, 'gem':-costGem}
		usr.luckycat['record'].append(rcd)
		usr.save()
		return {'gold':usr.gold, 'luckycat_beckon_count':usr.luckycat['beckon_count'], 'luckycat_beckon_cooldown':usr.luckycat['beckon_cooldown'], 'beckon_critical':beckonCritical}	
	
	@staticmethod
	def beckon_reset(usr):
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		
		gameConf = config.getConfig('game')
		costGem = gameConf['luckycat_beckon_reset_price']['gem']
		costGold = gameConf['luckycat_beckon_reset_price']['gold']
		
		if usr.gem < costGem:
			return {'msg':'gem_not_enough'}
		if usr.gold < costGold:
			return {'msg':'gold_not_enough'}
				
		usr.gem = usr.gem - costGem
		usr.gold = usr.gold - costGold
		
		usr.luckycat['beckon_cooldown'] = 0
		usr.luckycat['beckon_last_update_time'] = currentTime()
		
		usr.save()
		return {'gold':usr.gold, 'gem':usr.gem, 'luckycat_beckon_cooldown': luckycat.beckon_cooldown(usr)}	
			
	@staticmethod
	def beckon_cooldown(usr):
		now = currentTime()
		if usr.luckycat['beckon_cooldown'] + usr.luckycat['beckon_last_update_time'] > now:			
			return usr.luckycat['beckon_cooldown'] + usr.luckycat['beckon_last_update_time'] - currentTime()		
		return 0
		
	@staticmethod
	def feed_self_cooldown(usr, gameConf):
		now = currentTime()
		if usr.luckycat['feed_self_last_time'] + gameConf['luckycat_feed_self_cooldown'] > now:
			return  usr.luckycat['feed_self_last_time'] + gameConf['luckycat_feed_self_cooldown'] - currentTime()
		return 0
		
	@staticmethod
	def feed_other_cooldown(usr, gameConf):		
		now = currentTime()
		if usr.luckycat['feed_other_last_time'] + gameConf['luckycat_feed_other_cooldown'] > now:
			return usr.luckycat['feed_other_last_time'] + gameConf['luckycat_feed_other_cooldown'] - now
		return 0
	
	@staticmethod
	def beckonCooldownCleanup(usr):
		gemCost = usr.luckycat['beckon_cooldown'] / 10
		usr.gem = usr.gem - gemCost
		usr.save()
		return {'gem':usr.gem, 'luckycat_beckon_cooldown':0}
		
	@staticmethod
	def feed(usr, target):
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		luckycat.updateFeed(usr)
		gameConf = config.getConfig('game')
		requiredLevel = 0
		feedCountMax = 0
		feedCount = 0
		now = currentTime()
					
		feedCountMax = gameConf['luckycat_feed_other_count_max']
		feedCount = usr.luckycat['feed_other_count']											
			
		if requiredLevel > usr.level:
			return {'msg':'luckycat_feed_level_required'}
		
		if feedLastTime + feedCooldown > now:
			return {'msg':"luckycat_feed_in_cooldown"}
				
		if not (feedCount < feedCountMax):
			return {'msg':'luckycat_feed_max_time'}					
				
		spreadBlessid = ''
		#luckycatLevelConf = config.getConfig('luckycat_level')

		if not target.luckycat:
			return {'msg':'luckycat_not_available'}
				
		usr.luckycat['feed_request_list'].append(target.roleid)
		target.luckycat['feed_candidate_list'].append(usr.roleid)
		luckycat.notify_candidate_add(target, usr.roleid)
		
		usr.save()		
		target.save()
		
		data = {}
		data['luckycat'] = luckycat.getClientData(target, gameConf)
		if awardGold:
			data['gold'] = usr.gold
		
		data['spread_bless'] = spreadBlessid	
		return data
		
	@staticmethod
	def agreeFeed(usr, friendid):
		
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		
		if friendid not in usr.luckycat['feed_candidate_list']:
			return {'msg':'request_not_exist'}
		
		usr.luckycat['feed_candidate_list'].remove(friendid)
		friend = usr.__class__.get(friendid)
		if not friend:
			usr.save()
			return {'msg':'usr_not_exist'}
		
		friend.luckycat['feed_request_list'].remove(usr.roleid)
		luckycat.notify_request_list_remove(friend, usr.roleid)
		
		if not friend.luckycat:
				return {'msg':'luckycat_not_available'}
		luckycat.updateBless(usr)
		luckycat.updateBless(friend)
		allSpreadBlessid = []
		for blessid in target.luckycat['bless']:
			if target.luckycat['bless'][blessid].has_key('spread'):
				allSpreadBlessid.append(blessid)
			
		for blessid in usr.luckycat['bless']:
			if blessid in spreadBlessid:
				allSpreadBlessid.remove(blessid)
					
		spreadBlessid = ''
		if allSpreadBlessid:
			spreadBlessid = random.sample(allSpreadBlessid, 1)[0]			
			usr.luckycat['bless'][spreadBlessid]['blessid'] = spreadBlessid
			
		
		luckycat.notify_bless(usr, spreadBlessid)
		luckycatProfitConf = config.getConfig('luckycat_profit')
		
		usrAwardGold = luckycatProfitConf[usr.level - 1]['agreeProfit']
		friendAwardGold = luckycatProfitConf[friend.level - 1]['blessProfit']
		
		usr.gold = usr.gold + usrAwardGold
		friend.gold = friend.gold + friendAwardGold
		
		usr.save()
		friend.save()		
		return {'gold':usr.gold, 'luckycat_bless':spreadBlessid}
		
	@staticmethod
	def disagreeFeed(usr, friendid):
		if friendid not in usr.luckycat['feed_candidate_list']:
			return {'msg':'luckycat_candidate_not_exist'}
		
		usr.luckycat['feed_candidate_list'].remove(friendid)
		friend = usr.__class__.get(friendid)
		if not friend:
			usr.save()
			return {'msg':'usr_not_exist'}
		
		if usr.roleid in friend.luckycat['feed_request_list']:		
			friend.luckycat['feed_request_list'].remove(usr.roleid)
			luckycat.notify_request_list_remove(friend, usr.roleid)
			friend.save()
		usr.save()
		return {'delete_luckycat_candidate': friendid}
				
	@staticmethod
	def cancelRequest(usr, friendid):
		if friendid not in usr.luckycat['feed_request_list']:
			return {'msg':'luckycat_request_not_exist'}
		
		usr.luckycat['feed_request_list'].remove(friendid)
		
		friend = usr.__class__.get(friendid)
		if not friend:
			usr.save()
			return {'msg':'usr_not_exist'}
				
		if usr.roleid in friend.luckycat['feed_candidate_list']:
			friend.luckycat['feed_candidate_list'].remove(usr.roleid)
			friend.save()
		usr.save()				
		return {'delete_request':friendid}
					
	@staticmethod
	def rollBless(usr):
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		luckycat.updateBless(usr)
		luckycatBlessConf = config.getConfig('luckycat_bless')
		now = currentTime()		
		if is_same_day(now, usr.luckycat['bless_roll_last_time']):
			return {'msg':'roll_bless_already_today'}
		
		roll = randint()
		blessConf = {}
		for blessid in luckycatBlessConf:
			b = luckycatBlessConf[blessid] 
			if b['probability'] < roll:
				roll = roll - b['probability']
			else:
				blessConf = b		
		
		blessid = blessConf['blessid']
		if not usr.luckycat['bless'].has_key(blessid):
			usr.luckycat['bless'][blessid] = {}
			usr.luckycat['bless'][blessid]['blessid'] = blessid
			if luckycat.isCycleDay(usr):
				usr.luckycat['bless'][blessid]['spread'] = True				
		return {'luckycat_roll_bless':blessid, 'luckycat_roll_bless_spread':usr.luckycat['bless'][blessid].has_key('spread')}
			
	@staticmethod
	def buyBless(usr, blessid):		
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		luckycat.updateBless(usr)
		if usr.luckycat['bless'].has_key(blessid) and usr.luckycat['bless'][blessid].has_key('spread'):
			return {'msg':'luckycat_bless_spread_already_exist'}
		
		luckycatBlessConf = config.getConfig('luckycat_bless')
		blessConf = luckycatBlessConf[blessid]
		
		if not usr.luckycat['bless'].has_key(blessid):
			usr.luckycat['bless'][blessid] = {}
			usr.luckycat['bless'][blessid]['blessid'] = blessid			
		usr.luckycat['bless'][blessid]['spread'] = True
		return {'luckycat_roll_bless':blessid, 'luckycat_roll_bless_spread':True}		
	
	@staticmethod	
	def updateBless(usr):
		now = currentTime()
		gameConf = config.getConfig('game')
		if usr.luckycat['bless_cycle_begin_time'] and (day_diff(usr.luckycat['bless_cycle_begin_time'], now) > gameConf['luckycat_bless_cycle_day']):
			usr.luckycat['bless_cycle_begin_time'] = 0
			
	@staticmethod	
	def isCycleDay(usr):
		return is_same_day(usr.luckycat['bless_cycle_begin_time'], currentTime()) or (usr.luckycat['bless_cycle_begin_time'] == 0)
					
	@staticmethod
	def getClientData(usr, gameConf):		
		data = {}
		data['level'] = usr.luckycat['level']
		data['exp'] = usr.luckycat['exp']
		data['critical_point_list'] = usr.luckycat['critical_point_list']
		data['beckon_count'] = usr.luckycat['beckon_count']
		data['beckon_gem_count'] = usr.luckycat['beckon_gem_count']		
		data['beckon_cooldown'] = luckycat.beckon_cooldown(usr)
		data['critical_point_list'] = usr.luckycat['critical_point_list']
		data['feed_self_count'] = usr.luckycat['feed_self_count']
		#data['feed_self_cooldown'] = luckycat.feed_self_cooldown(usr, gameConf)
		data['feed_other_count'] = usr.luckycat['feed_other_count']
		#data['feed_other_cooldown'] = luckycat.feed_other_cooldown(usr, gameConf)
		data['bless_roll_last_time'] = usr.luckycat['bless_roll_last_time']
		data['bless_cycle_begin_time'] = usr.luckycat['bless_cycle_begin_time']
		data['bless'] = usr.luckycat['bless']
		#data['record'] = usr.luckycat['record']		
		return data
				
	@staticmethod
	def isCritical(usr):
		criticalPoint = sum(usr.luckycat['critical_point_list'])
		probability = criticalPoint / usr.luckycat['level'] * 25
		return drop(probability)
		
	@staticmethod
	def updateBeckon(usr):		
		gameConf = config.getConfig('game')
		now = currentTime()
		if is_expire(gameConf['luckycat_beckon_count_reset_time'], usr.luckycat['beckon_count']):
			usr.luckycat['beckon_count'] = 0
			usr.luckycat['beckon_cooldown'] = 0
			usr.luckycat['beckon_last_update_time'] = now
			return
		
		elapse = now - usr.luckycat['beckon_last_update_time']		
		usr.luckycat['beckon_cooldown'] = usr.luckycat['beckon_cooldown'] - elapse
		if usr.luckycat['beckon_cooldown'] < 0:
			usr.luckycat['beckon_cooldown'] = 0
		usr.luckycat['beckon_last_update_time'] = now
			
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
		nw = usr.getNetwork()
		nw.updateFriendData()		
		
	@staticmethod
	def onEveryLeveup(usr):
		gameConf = config.getConfig('game')
		luckycatLevelConf = config.getConfig('luckycat_level')
		if gameConf['luckycat_level_critical_itme'].count(usr.luckycat['level']):
			usr.luckycat['critical_point_list'].append(hit(gameConf['luckycat_critical_point_probability']))		
		awardGold = luckycatLevelConf[usr.luckycat['level']]['levelupGold']		
		awardGem = 0
		return awardGold, awardGem	
			
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
		return (selItem[1][0] + selItem[1][1]) / 2
			
	@staticmethod
	def notify_bless(usr, blessid):
		if not usr.notify.has_key('add_luckycat_bless'):
			usr.notify['add_luckycat_bless'] = []
		usr.notify['add_luckycat_bless'].append(blessid)
		
			
	@staticmethod
	def notify_request_list_remove(usr, friendid):
		if not usr.notify.has_key('delete_luckcat_request'):			
			usr.notify['delete_luckcat_request'] = []
		usr.notify['delete_luckcat_request'].append(friendid)
		
	@staticmethod
	def notify_candidate_list_add(usr, friendid):
		if not usr.notify.has_key('add_luckycat_candidate'):
			usr.notify['add_luckycat_candidate'] = []
		usr.notify['add_luckycat_candidate'].append(friendid)