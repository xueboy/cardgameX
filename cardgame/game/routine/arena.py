#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import is_same_day, currentTime
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
	def make():
		return {'times':0, 'last_chellage_time':0, 'last_update_time':0}

	@staticmethod
	def challenge(usr, defenceRoleid):
		defenceRole = usr.get(defenceRoleid)
		if not defenceRole:
			return {'msg':'user_not_exist'}
				
		arena.arena_update(usr)
				
		if usr.arena['times'] <= 0:
			return {'msg':'arena_max_time'}
				
		usr.arena['times'] = usr.arena['times'] - 1
		usr.arena['last_chellage_time'] = currentTime()
		
			
		usr.arena['challenge_roleid'] = defenceRole.roleid
		usr.save()
		return {'defence':defenceRole.getBattleData(), 'arena_time':usr.arena['times']}

	@staticmethod
	def arena_update(usr):		
		if not is_same_day(usr.arena['last_update_time'], currentTime()):
			gameConf = config.getConfig('game')			
			usr.arena['times'] = gameConf['arena_times']
		usr.arena['last_update_time'] = currentTime()
