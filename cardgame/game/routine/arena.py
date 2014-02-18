#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import is_same_day, currentTime, randint
from cardgame.settings import ARENE_SERVER
from game.utility.config import config
from game.routine.drop import drop
from game.routine.vip import vip
#from game.models.user import user


class arena:
	@staticmethod
	def stand_ladder(usr):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/stand_ladder/', None, {'roleid':str(usr.roleid)}))

	@staticmethod
	def show_all():
		return json.loads(curl.url(ARENE_SERVER +  '/arena/show_all/', None, {}))

	@staticmethod
	def remove(roleid):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/remove/', None, {'roleid':roleid}))

	@staticmethod
	def set_avatar_id(roleid, avatar_id):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/set_avatar_id/', None, {'roleid':roleid, 'avatar_id':avatar_id}))
			
	@staticmethod
	def score(roleid):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/score/', None, {'roleid':roleid}))

	@staticmethod
	def make():
		return {'times':0, 'last_chellage_time':0, 'last_update_time':0, 'rank_award':{}}
			
	@staticmethod
	def award_score(roleid, awardScore):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/award_score/', None, {'roleid':roleid, 'award_score': awardScore}))

	@staticmethod
	def challenge(usr, defenceRoleid):
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
		if not is_same_day(usr.arena['last_update_time'], currentTime()):		
			usr.arena['times'] = 0
		usr.arena['last_update_time'] = currentTime()
		

	@staticmethod
	def defeate(usr):
		res = None
		print usr.arena		
		if usr.arena.has_key('challenge_roleid'):
			
			res = json.loads(curl.url(ARENE_SERVER +  '/arena/defeat/', None, {'offence_roleid':str(usr.roleid), 'defence_roleid':usr.arena['challenge_roleid']}))
			
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
		gameConf = config.getConfig('game')
		pointConsume = mediumCount * gameConf['arena_medium_price']

		res = curl.url(ARENE_SERVER +  '/arena/convert/', None, {'roleid':str(usr.roleid), 'score':pointConsume})
		
		res = json.loads(res)
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
		print usr.arena['rank_award']
		print rk
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
		