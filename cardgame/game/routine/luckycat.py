﻿#coding:utf-8
#!/usr/bin/env python

import random
from gclib.utility import is_expire, currentTime, hit, randint, dayTime, drop, is_same_day
from game.utility.config import config
from game.routine.vip import vip


class luckycat:
	@staticmethod
	def make():
		"""
		制做
		"""
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
		"""
		招财
		"""
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		luckycatProfitConf = config.getConfig('luckycat_profit')
		gameConf = config.getConfig('game')
		luckycat.updateBeckon(usr)
		
		gameConf = config.getConfig('game')		 
		
		if usr.luckycat['beckon_count'] >= gameConf['luckycat_beckon_count_base']	and (not useGem):
			return {'msg':'luckycat_beckon_max_free_count'}
				
		if usr.luckycat['beckon_count'] >= gameConf['luckycat_beckon_count_base'] + vip.value(usr, 'gem_beckon'):
			return {'msg':'luckycat_beckon_max_count'}
				
		if usr.luckycat['beckon_cooldown'] > gameConf['luckycat_cooldown_max'] and (not useGem):
			return {'msg':'luckycat_beckon_in_cooldown'}
			
		costGem = 0	
		if useGem:
			costGem = gameConf['luckycat_beckon_gem_base'] + gameConf['luckycat_beckon_gem_delta'] * usr.luckycat['beckon_gem_count']
			if usr.gem < costGem:
				return {'msg':'gem_not_enough'}
		
		luckycatBlessConf = config.getConfig('luckycat_bless')
		
		beckonGold = luckycatProfitConf[usr.level - 1]['beckonProfit']
		
		beckonCritical, blessid = luckycat.beckon_once(usr, useGem, beckonGold,  luckycatBlessConf, gameConf)
		
		usr.save()
		return {'gold':usr.gold, 'luckycat_beckon_count':usr.luckycat['beckon_count'], 'luckycat_beckon_cooldown':usr.luckycat['beckon_cooldown'], 'beckon_critical':beckonCritical, 'gem':usr.gem, 'bless':blessid}	
			
	@staticmethod
	def beckon_clickonce(usr):
		"""
		一键招财
		"""
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		
		if not vip.value(usr, 'beckon_clickonce'):
			return {'msg':'vip_required'}
				
		luckycatProfitConf = config.getConfig('luckycat_profit')
		gameConf = config.getConfig('game')
		luckycat.updateBeckon(usr)
		
		gameConf = config.getConfig('game')		 
		
		if usr.luckycat['beckon_count'] >= gameConf['luckycat_beckon_count_base']	and (not useGem):
			return {'msg':'luckycat_beckon_max_free_count'}
				
		if usr.luckycat['beckon_count'] >= gameConf['luckycat_beckon_count_base'] + vip.value(usr, 'gem_beckon'):
			return {'msg':'luckycat_beckon_max_count'}
				
		if usr.luckycat['beckon_cooldown'] > gameConf['luckycat_cooldown_max'] and (not useGem):
			return {'msg':'luckycat_beckon_in_cooldown'}
				
		costGem = gameConf['luckycat_beckon_gem_base'] + gameConf['luckycat_beckon_gem_delta'] * usr.luckycat['beckon_gem_count']
		if usr.gem < costGem:
			return {'msg':'gem_not_enough'}
		
		luckycatBlessConf = config.getConfig('luckycat_bless')
		
		beckonGold = luckycatProfitConf[usr.level - 1]['beckonProfit']
		
		for i in range(10):
			if usr.gem < costGem:				
				break
			beckonCritical, blessid = luckycat.beckon_once(usr, costGem, beckonGold,  luckycatBlessConf, gameConf)
		
		usr.save()
		return {'gold':usr.gold, 'luckycat_beckon_count':usr.luckycat['beckon_count'], 'luckycat_beckon_cooldown':usr.luckycat['beckon_cooldown'], 'gem':usr.gem}	
		
		
	@staticmethod
	def beckon_once(usr, costGem, beckonGold, luckycatBlessConf, gameConf):
		"""
		招财一次
		"""
		blessid = []
		for i in range(3):
			bid = luckycat.rollBeckonBless(usr, luckycatBlessConf)
			if bid:
				blessid.append(bid)		
		beckonGold, gem, beckonCount, beckonCD = luckycat.beckonBless(usr, beckonGold, blessid, luckycatBlessConf)		
		usr.luckycat['beckon_count'] = beckonCount
		usr.luckycat['beckon_cooldown'] = beckonCD
		
		beckonGold = beckonGold * luckycat.currentLuckycatFortune()
		beckonCritical = False
		if luckycat.isCritical(usr):
			beckonGold = beckonGold * 2		
			beckonCritical = True
		usr.gold = usr.gold + beckonGold
		usr.gem = usr.gem - costGem
		usr.gem = usr.gem + gem
		
		if costGem:
			usr.luckycat['beckon_count'] = usr.luckycat['beckon_count'] + 1
			usr.luckycat['fatigue'] = usr.luckycat['fatigue'] + 1
			if usr.luckycat['fatigue'] > gameConf['luckycat_fatigue_max']:
				usr.luckycat['fatigue'] = gameConf['luckycat_fatigue_max']
			usr.luckycat['beckon_cooldown'] = int(usr.luckycat['beckon_cooldown'] + (gameConf['luckycat_cooldown_base'] * (1 + usr.luckycat['fatigue'] / 9.4)))
			usr.luckycat['beckon_last_update_time'] = currentTime()
		return beckonCritical, blessid
	
	@staticmethod
	def beckonBless(usr, beckonGold, blessid, luckycatBlessConf):
		"""
		招财祝福
		"""			
		gold = beckonGold
		gem = 0
		beckonCount = usr.luckycat['beckon_count']
		beckonCD = usr.luckycat['beckon_cooldown']
		
		for b in blessid:
			luckycatBlessInfo = luckycatBlessConf[b]
			
			if luckycatBlessInfo['blessTypeStr'] == 'rubyluck':
				gem = gem + luckycatBlessInfo['value']
			elif luckycatBlessInfo['blessTypeStr'] == 'freepc':
				beckonCount = usr.luckycat['beckon_count'] - 1
			elif luckycatBlessInfo['blessTypeStr'] == 'increase':
				gold = gold * luckycatBlessInfo['value']
			elif luckycatBlessInfo['blessTypeStr'] == 'reducecd':
				beckonCD = beckonCD - luckycatBlessInfo['value']
				
		return gold, gem, beckonCount, beckonCD		
	
	@staticmethod
	def beckon_reset(usr):
		"""
		重置招财
		"""
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
		"""
		招财冷却
		"""
		now = currentTime()
		if usr.luckycat['beckon_cooldown'] + usr.luckycat['beckon_last_update_time'] > now:			
			return usr.luckycat['beckon_cooldown'] + usr.luckycat['beckon_last_update_time'] - currentTime()		
		return 0
	
	@staticmethod
	def beckonCooldownCleanup(usr):
		"""
		清除招财冷却时间
		"""
		gemCost = usr.luckycat['beckon_cooldown'] / 10
		usr.gem = usr.gem - gemCost
		usr.save()
		return {'gem':usr.gem, 'luckycat_beckon_cooldown':0}
		
	@staticmethod
	def feed(usr, target):
		"""
		喂养
		"""
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		luckycat.updateFeed(usr)
		gameConf = config.getConfig('game')
		requiredLevel = 0
		now = currentTime()
		
		if (target.roleid in usr.luckycat['feed_request_list']) or (usr.roleid in target.luckycat['feed_candidate_list']) :
			return {'msg':'luckycat_already_feed'}
				
		if gameConf['luckycat_feed_other_required_level'] > usr.level:
			return {'msg':'luckycat_feed_level_required'}
	
		if usr.luckycat['feed_self_count'] >= (gameConf['luckycat_feed_self_count_max'] + vip.value(usr, 'feed_extra')):
			return {'msg':'luckycat_feed_max_time'}	
		
		luckycat.updateFeed(usr)
		usr.luckycat['feed_self_count'] = usr.luckycat['feed_self_count'] + 1
		usr.luckycat['feed_self_last_time'] = now
		
				
		spreadBlessid = ''

		if not target.luckycat:
			return {'msg':'luckycat_not_available'}		
						
		usr.luckycat['feed_request_list'].append(int(target.roleid))
		target.luckycat['feed_candidate_list'].append(int(usr.roleid))
		
		luckycat.notify_candidate_add(target, usr.roleid)
		
		usr.save()		
		target.save()
		
		return {'add_luckycat_request':target.roleid, 'luckycat_feed_self_count': usr.luckycat['feed_self_count']}
		
	@staticmethod
	def agreeFeed(usr, friendid):
		"""
		同意喂养
		"""
		
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		
		if friendid not in usr.luckycat['feed_candidate_list']:
			return {'msg':'luckycat_request_not_exist'}
				
		gameConf = config.getConfig('game')
				
		luckycat.updateFeed(usr)
		if usr.luckycat['feed_other_count'] >= gameConf['luckycat_feed_other_count_max']:
			return {'msg':'luckycat_agree_request_max_time'}
		
		usr.luckycat['feed_candidate_list'].remove(friendid)
		friend = usr.__class__.get(friendid)
		if not friend:
			usr.save()
			return {'msg':'usr_not_exist'}
		
		friend.luckycat['feed_request_list'].remove(usr.roleid)
		luckycat.notify_request_list_remove(friend, usr.roleid)
		
		if not friend.luckycat:
				return {'msg':'luckycat_not_available'}
		
		now = currentTime()
		
		usr.luckycat['feed_other_count'] = usr.luckycat['feed_other_count'] + 1
		usr.luckycat['feed_self_last_time'] = now
		luckycat.updateBless(usr)
		luckycat.updateBless(friend)
		allSpreadBlessid = []
		for blessid in usr.luckycat['bless']:
			if usr.luckycat['bless'][blessid].has_key('spread'):
				allSpreadBlessid.append(blessid)
			
		for blessid in friend.luckycat['bless']:
			if blessid in allSpreadBlessid:
				allSpreadBlessid.remove(blessid)
					
		spreadBlessid = ''
		if allSpreadBlessid:
			spreadBlessid = random.sample(allSpreadBlessid, 1)[0]
			friend.luckycat['bless'][spreadBlessid] = {}
			friend.luckycat['bless'][spreadBlessid]['blessid'] = spreadBlessid
			
		
		luckycat.notify_bless(friend, spreadBlessid)
		luckycatProfitConf = config.getConfig('luckycat_profit')
		
		usrAwardGold = luckycatProfitConf[usr.level - 1]['agreeProfit']
		friendAwardGold = luckycatProfitConf[friend.level - 1]['blessProfit']
		
		usr.gold = usr.gold + usrAwardGold
		friend.gold = friend.gold + friendAwardGold
		
		usr.save()
		friend.save()		
		return {'gold':usr.gold, 'luckycat_bless':spreadBlessid, 'luckycat_feed_other_count':usr.luckycat['feed_other_count']}
		
	@staticmethod
	def disagreeFeed(usr, friendid):
		"""
		不同意喂养
		"""
		if friendid not in usr.luckycat['feed_candidate_list']:
			return {'msg':'luckycat_candidate_not_exist'}
		
		usr.luckycat['feed_candidate_list'].remove(friendid)
		usr.luckycat['feed_self_count'] = usr.luckycat['feed_self_count'] + 1
		friend = usr.__class__.get(friendid)
		if not friend:
			usr.save()
			return {'msg':'usr_not_exist'}
		
		if usr.roleid in friend.luckycat['feed_request_list']:		
			friend.luckycat['feed_request_list'].remove(usr.roleid)
			luckycat.notify_request_list_remove(friend, usr.roleid)
			friend.save()
		usr.save()
		return {'delete_luckycat_candidate': friendid, 'feed_self_count':usr.luckycat['feed_self_count']}
				
	@staticmethod
	def cancelRequest(usr, friendid):
		"""
		取消请求
		"""
		if friendid not in usr.luckycat['feed_request_list']:
			return {'msg':'luckycat_request_not_exist'}

				
		luckycat.updateFeed(usr)
		now = currentTime()
		usr.luckycat['feed_self_count'] = usr.luckycat['feed_self_count'] - 1
		usr.luckycat['feed_self_last_time'] = now
		
		usr.luckycat['feed_request_list'].remove(friendid)
		
		friend = usr.__class__.get(friendid)
		if not friend:
			usr.save()
			return {'msg':'usr_not_exist'}
				
		if usr.roleid in friend.luckycat['feed_candidate_list']:
			friend.luckycat['feed_candidate_list'].remove(usr.roleid)
			friend.save()
		usr.save()				
		return {'delete_luckycat_request':friendid, 'luckycat_feed_self_count': usr.luckycat['feed_self_count']}
					
	
	@staticmethod
	def rollBeckonBless(usr, luckycatBlessConf):
		"""
		抽取招财祝福
		"""
		#luckycat.updateBless(usr)
		#luckycatBlessConf = config.getConfig('luckycat_bless')		
		
		roll = randint()
		blessConf = {}
		for blessid in luckycatBlessConf:
			b = luckycatBlessConf[blessid] 
			if b['probability'] < roll:
				roll = roll - b['probability']
			else:
				if usr.luckycat['bless'].has_key(blessid):
					return blessid
				return None
		return None
		
	
	@staticmethod
	def rollBless(usr, isUseGem):
		"""
		抽取祝福
		"""
		if not usr.luckycat:
			return {'msg':'luckycat_not_available'}
		
		if isUseGem and (not vip.canBuyLuckycatBless(usr)):
			return {'msg':'luckycat_vip_required'}
						
		luckycat.updateBless(usr)
		luckycatBlessConf = config.getConfig('luckycat_bless')
		now = currentTime()		
		if is_same_day(now, usr.luckycat['bless_roll_last_time']):
			if not isUseGem:
				return {'msg':'luckycat_roll_bless_already_today'}
		else: 
			if isUseGem:
				return {'msg':'gem_not_necessary'}
				
		roll = randint()		
		blessConf = {}
		for blessid in luckycatBlessConf:
			b = luckycatBlessConf[blessid] 
			if b['probability'] < roll:
				roll = roll - b['probability']				
			else:
				blessConf = b
				break
		
		blessid = blessConf['blessid']
		if not usr.luckycat['bless'].has_key(blessid):
			usr.luckycat['bless'][blessid] = {}
			usr.luckycat['bless'][blessid]['blessid'] = blessid
			if luckycat.isCycleDay(usr) or isUseGem:
				usr.luckycat['bless'][blessid]['spread'] = True
				
		usr.luckycat['bless_roll_last_time'] = now
		usr.save()
		return {'luckycat_roll_bless':blessid, 'luckycat_roll_bless_spread':usr.luckycat['bless'][blessid].has_key('spread')}
		
	@staticmethod	
	def updateBless(usr):
		"""
		更新祝福
		"""
		now = currentTime()
		gameConf = config.getConfig('game')
		if usr.luckycat['bless_cycle_begin_time'] and (day_diff(usr.luckycat['bless_cycle_begin_time'], now) > gameConf['luckycat_bless_cycle_day']):
			usr.luckycat['bless_cycle_begin_time'] = 0
			
	@staticmethod	
	def isCycleDay(usr):
		"""
		是否循环天
		"""
		return is_same_day(usr.luckycat['bless_cycle_begin_time'], currentTime()) or (usr.luckycat['bless_cycle_begin_time'] == 0)
					
	@staticmethod
	def getClientData(usr, gameConf):
		"""
		得到client data
		"""
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
		data['feed_candidate_list'] = usr.luckycat['feed_candidate_list']
		data['feed_request_list'] = usr.luckycat['feed_request_list']
		return data
				
	@staticmethod
	def isCritical(usr):
		"""
		是否爆击
		"""
		criticalPoint = sum(usr.luckycat['critical_point_list'])
		probability = criticalPoint / usr.luckycat['level'] * 25
		return drop(probability)
		
	@staticmethod
	def updateBeckon(usr):		
		"""
		更新招财
		"""
		gameConf = config.getConfig('game')
		now = currentTime()
		if is_expire(gameConf['luckycat_beckon_count_reset_time'], usr.luckycat['beckon_last_update_time']):
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
		"""
		更新喂养
		"""
		gameConf = config.getConfig('game')		
		now = currentTime()
		if is_expire(gameConf['luckycat_beckon_count_reset_time'], usr.luckycat['feed_self_last_time']):
			usr.luckycat['feed_self_count'] = 0
			usr.luckycat['feed_self_last_time'] = currentTime()
		if is_expire(gameConf['luckycat_beckon_count_reset_time'], usr.luckycat['feed_other_last_time']):
			usr.luckycat['feed_other_count'] = 0
			usr.luckycat['feed_oter_last_time'] = currentTime()
				
	@staticmethod
	def onLeveup(usr):
		"""
		升级喂养
		"""
		nw = usr.getNetwork()
		nw.updateFriendData()		
		
	@staticmethod
	def onEveryLeveup(usr):
		"""
		每次升级
		"""
		gameConf = config.getConfig('game')
		luckycatLevelConf = config.getConfig('luckycat_level')
		if gameConf['luckycat_level_critical_itme'].count(usr.luckycat['level']):
			usr.luckycat['critical_point_list'].append(hit(gameConf['luckycat_critical_point_probability']))		
		awardGold = luckycatLevelConf[usr.luckycat['level']]['levelupGold']		
		awardGem = 0
		return awardGold, awardGem	
			
	@staticmethod
	def freshCritical(usr, itemIndex):
		"""
		更新暴击
		"""
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
	def currentLuckycatFortune():
		"""
		当前财运
		"""
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
		"""
		提示祝福
		"""
		if not usr.notify.has_key('add_luckycat_bless'):
			usr.notify['add_luckycat_bless'] = []
		usr.notify['add_luckycat_bless'].append(blessid)
		
			
	@staticmethod
	def notify_request_list_remove(usr, friendid):
		"""
		提示请求移除
		"""
		if not usr.notify.has_key('delete_luckcat_request'):			
			usr.notify['delete_luckcat_request'] = []
		usr.notify['delete_luckcat_request'].append(friendid)
		
	@staticmethod
	def notify_candidate_add(usr, friendid):
		"""
		提示添加候选菜单
		"""
		if not usr.notify.has_key('add_luckycat_candidate'):
			usr.notify['add_luckycat_candidate'] = []
		usr.notify['add_luckycat_candidate'].append(friendid)