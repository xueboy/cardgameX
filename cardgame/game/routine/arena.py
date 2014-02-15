#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import is_same_day, currentTime, randint
from cardgame.settings import ARENE_SERVER
from game.utility.config import config
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
		return {'times':0, 'last_chellage_time':0, 'last_update_time':0}

	@staticmethod
	def challenge(usr, defenceRoleid):
		defenceRole = usr.get(defenceRoleid)
		if not defenceRole:
			return {'msg':'user_not_exist'}
		
		gameConf = config.getConfig('game')			
		arena.arena_update(usr)
		
				
		if usr.arena['times'] >= gameConf['arena_times']:
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
		del usr.arena['challenge_roleid']
		card = None
		gold = 0
		skl = None
		rd = randint()
		rd = rd - gameConf['arena_loot_gold_probability']
		if rd <= 0:
			gold = arenaLootInfo['glod']
		else:
			rd = rd - gameConf['arena_loot_pet_probability']
			if rd <= 0:
				card = {'id':arenaLootInfo['cardid'], 'level':arenaLootInfo['cardlevel']}				
			else:
				skl = {'id':arenaLootInfo['skillid'], 'level':arenaLootConf['skilllevel']}				
		
		if gold or card or skl:			
			usr.arena['loot'] = {}
			if gold:
				usr.arena['loot']['glod'] = gold
			if card:
				usr.arena['loot']['card'] = card
			if skl:
				usr.arena['loot']['skill'] = skl

		data = {}
		
		
		if gold:
			data['gold'] = usr.gold
		if card:
			data['add_card'] = card			
		if skl:
			data['add_skill'] = skl
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
		if usr.arena.has_key('challenge_roleid'):
			res = curl.url(ARENE_SERVER +  '/arena/defeat/', None, {'offence_roleid':str(usr.roleid), 'defence_roleid':usr.arena['challenge_roleid']})
		
			arenaLootConf = config.getConfig('arena_loot')
			gameConf = config.getConfig('game')
			arenaLootInfo = arenaLootConf[usr.level - 1]
			del usr.arena['challenge_roleid']
			card = None
			gold = 0
			skl = None
			
			data = {}
			if usr.arena.has_key('loot'):
				if usr.arena.has_key('gold'):				
					usr.gold = usr.gold + arenaLootInfo['glod']
				if usr.arena.has_key('card'):					
						inv = usr.getInventory()
						card =inv.addCard( usr.arena['loot']['card']['id'], usr.arena['loot']['card']['level'])
				if usr.arena.has_key('skill'):
						inv = usr.getInventory()
						skl = inv.addSkill( usr.arena['loot']['card']['id'], usr.arena['loot']['card']['level'])

			
				if gold:
					data['gold'] = usr.gold

				if card:
					data['add_card'] = card
					inv.save()
				if skl:
					data['add_skill'] = skl
					inv.save()
			usr.save()
			return data			
		return {'msg':'arena_ladder_have_not_chellenge'}