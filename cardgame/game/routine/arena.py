#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import is_same_day, currentTime, randint
from cardgame.settings import ARENE_SERVER, SIGLE_SERVER
from game.utility.config import config
from game.routine.drop import drop
from game.routine.vip import vip


#from game.models.user import user


class arena:
	@staticmethod
	def stand_ladder(usr):
		"""
		站上天梯
		"""
		if SIGLE_SERVER:
			from arenarank.routine.arena import arena as arenaR
			return arenaR.stand(str(usr.roleid))
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/stand_ladder/', None, {'roleid':str(usr.roleid)}))

	@staticmethod
	def show_all():
		"""
		显示所有
		"""
		if SIGLE_SERVER:
			from arenarank.routine.arena import arena as arenaR
			return arenaR.show_all()
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/show_all/', None, {}))

	@staticmethod
	def remove(roleid):
		"""
		移除
		"""
		if SIGLE_SERVER:
			from arenarank.routine.arena import arena as arenaR
			return arenaR.remove(str(roleid))
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/remove/', None, {'roleid':roleid}))

	@staticmethod
	def set_avatar_id(roleid, avatar_id):
		"""
		设置avatar id
		"""
		if SIGLE_SERVER:
			from arenarank.routine.arena import arena as arenaR
			return arenaR.set_avatar_id(str(roleid), avatar_id)
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/set_avatar_id/', None, {'roleid':roleid, 'avatar_id':avatar_id}))
	
	@staticmethod
	def show(usr):	
		"""
		显示
		"""	
		if SIGLE_SERVER:
			from arenarank.routine.arena import arena as arenaR
			return arenaR.show(str(usr.roleid))
		else: 
			return json.loads(curl.url(ARENE_SERVER + '/arena/show/', None, {'roleid': usr.roleid}))
					
	@staticmethod
	def score(roleid):
		"""
		分数
		"""
		if SIGLE_SERVER:
			from arenarank.routine.arena import arena as arenaR
			return arenaR.score(str(roleid))
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/score/', None, {'roleid':roleid}))

	@staticmethod
	def make():
		"""
		制做
		"""
		return {'times':0, 'last_chellage_time':0, 'last_update_time':0, 'rank_award':{}}
			
	@staticmethod
	def award_score(roleid, awardScore):
		"""
		分数奖励
		"""
		if SIGLE_SERVER:
			from arenarank.routine.arena import arena as arenaR
			return arenaR.award_score(str(roleid), awardScore)
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/award_score/', None, {'roleid':roleid, 'award_score': awardScore}))

	@staticmethod
	def challenge(usr, defenceRoleid):
		"""
		挑战
		"""
		defenceRole = usr.get(defenceRoleid)
		if not defenceRole:
			return {'msg':'user_not_exist'}
		
		gameConf = config.getConfig('game')			
		arena.arena_update(usr)
		
				
		if usr.arena['times'] >= vip.arenaTimes(usr):
			return {'msg':'arena_max_time'}
				
		gameConf = config.getConfig('game')
				
		if usr.costSp(gameConf['arena_sp_cost']) < 0:
			return {'msg': 'sp_not_enough'}
				
		usr.arena['times'] = usr.arena['times'] + 1
		usr.arena['last_chellage_time'] = currentTime()
					
		usr.arena['challenge_roleid'] = defenceRole.roleid		
		
		arenaLootConf = config.getConfig('arena_loot')
		gameConf = config.getConfig('game')
		arenaLootInfo = arenaLootConf[usr.level - 1]		

		usr.arena['loot'] = drop.roll(arenaLootConf[usr.level - 1]['drop'], {})		

		data = {}
		data['sp'] = usr.sp
		data.update(drop.makeAwardData(usr.arena['loot'], {}))
		data['defence'] = defenceRole.pvpProperty()
		data['arena_times'] = usr.arena['times']
		
		usr.save()
		return data

	@staticmethod
	def arena_update(usr):
		"""
		竞技场更新
		"""
		if not is_same_day(usr.arena['last_update_time'], currentTime()):		
			usr.arena['times'] = 0
		usr.arena['last_update_time'] = currentTime()
		

	@staticmethod
	def defeate(usr):
		"""
		击败
		"""
		res = None
		if usr.arena.has_key('challenge_roleid'):
			
			if SIGLE_SERVER:
				from arenarank.routine.arena import arena as arenaR
				return arenaR.defeat(str(usr.roleid), str(usr.arena['challenge_roleid']))
			else:
				res = json.loads(curl.url(ARENE_SERVER +  '/arena/defeat/', None, {'offence_roleid':usr.roleid, 'defence_roleid':usr.arena['challenge_roleid']}))
			
			arenaLootConf = config.getConfig('arena_loot')
			gameConf = config.getConfig('game')
						
			if res.has_key('msg'):
				return res
				
			alreadyReach = False
			for item in gameConf['arena_rank_award']:
				if item['rank'] >= res['position'] and (not usr.arena['rank_award'].has_key(item['rank'])):
					usr.arena['rank_award'][item['rank']] = True
					
				
			arenaLootInfo = arenaLootConf[usr.level - 1]
			challengeRole = usr.__class__.get(usr.arena['challenge_roleid'])
			challengeRole.gold = challengeRole.gold - arenaLootInfo['gold']
			if challengeRole.gold < 0:
				challengeRole.gold = 0
			challengeRole.notify_gold()
			challengeRole.save()
			del usr.arena['challenge_roleid']
			card = None
			gold = 0
			skl = None			
			data = {}
			if usr.arena.has_key('loot'):
				data = drop.do_award(usr, usr.arena['loot'], data)
				data = drop.makeData(data, res, 'award')
				
			usr.gainExp(arenaLootInfo['exp'])
			usr.gold = usr.gold + arenaLootInfo['gold']
			data['exp'] = usr.exp
			data['level'] = usr.level
			data['gold'] = usr.gold
			usr.save()
			return data			
		return {'msg':'arena_ladder_have_not_chellenge'}
			
	@staticmethod
	def convert(usr, mediumCount):
		"""
		况换
		"""
		gameConf = config.getConfig('game')
		pointConsume = mediumCount * gameConf['arena_medium_price']
		
		if SIGLE_SERVER:
			from arenarank.routine.arena import arena as arenaR
			res = arenaR.convert(str(usr.roleid), pointConsume)
		else:
			res = json.loads(curl.url(ARENE_SERVER +  '/arena/convert/', None, {'roleid':usr.roleid, 'score':pointConsume}))
				
		if res.has_key('msg'):
			return res

		mediumId = gameConf['arena_medium_id']
		inv = usr.getInventory()
		updateIt, newIt = inv.addItemCount(mediumId, mediumCount)
		inv.save()

		data = res
		
		data['drop'] = []
		if updateIt:
			for it in updateIt:
				data['drop'].append({'id' :it['itemid'], 'insId' : it['id'], 'type': 4, 'count':it['count']})
		if newIt:
			for it in newIt:
				data['drop'].append({'id' :it['itemid'], 'insId' : it['id'], 'type': 4, 'count':it['count']})
	
		#if updateIt:
		#	data['update_item_array'] = updateIt
		#if newIt:
		#	data['add_item_array'] = newIt
		return data
			
			
	@staticmethod
	def rank_award(usr, rk):
		"""
		排名奖励
		"""
		if not usr.arena['rank_award'].has_key(rk):
			return {'msg':'arena_rank_award_not_exist'}
		if not usr.arena['rank_award'][rk]:
			return {'msg':'arena_rank_award_already_have'}
		
		gameConf = config.getConfig('game')
		
		for item in gameConf['arena_rank_award']:
			if item['rank'] == int(rk):				
				#res = arena.award_score(usr.roleid, item['point'])
				data = {}
				awd = drop.open(usr, item['drop'], {})
				data = drop.makeData(awd, {})
				usr.arena['rank_award'][rk] = False				
				usr.save()
				return data				
		return {'msg':'arena_rank_award_not_exist'}
		
	