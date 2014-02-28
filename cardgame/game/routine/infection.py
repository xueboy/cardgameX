#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import is_same_day, currentTime, randint
from cardgame.settings import ARENE_SERVER
from game.models.network import network
from game.utility.config import config
from game.routine.drop import drop


class infection:
	
	
	@staticmethod
	def dungeon_encounter(usr):
		if not usr.infection['is_infection']:			
			rd = randint
			gameConf = config.getConfig('game')
			if rd < gameConf['infection_dungeon_probability']:
				res = infection.Encount(usr)
				if not res.has_key('msg'):
					return res							
		return {}
		
		
	@staticmethod
	def encounter(usr):
		return infection.Encount(usr)
		
	@staticmethod
	def beat(usr, battle_roleid, damage):
		
		res = infection.Beat(usr, battle_roleid, damage)		
		if res.has_key('msg'):
			return res
		data = res
		return data
				
	@staticmethod
	def Beat(usr, battle_roleid, damage):
		
		data = {}
		data['roleid'] = usr.roleid
		data['rolename'] = usr.name
		data['rolelevel'] = usr.level	
		data['battle_roleid'] = battle_roleid
		data['damage1'] = damage[0]
		data['damage2'] = damage[1]
		data['damage3'] = damage[2]
		data['damage4'] = damage[3]
		data['damage5'] = damage[4]
		data['damage6'] = damage[5]
		
		
		return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_beat/', None, data))
		
	@staticmethod
	def call(usr):		
		nw = usr.getNetwork()		
		friend = nw.friend.items()
		res = infection.Call(usr, friend)
		if res.has_key('msg'):
			return res
		return res
	
	@staticmethod
	def get_battle(usr):
		return infection.GetBattle(usr)
		
	@staticmethod
	def Encount(usr):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_encounter/', None, {'roleid':str(usr.roleid), 'rolename': usr.name}))
			
	@staticmethod
	def Award(usr, battleRoleid, create_time):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_award/', None, {'roleid':str(usr.roleid), 'battle_roleid': battleRoleid, 'create_time':create_time}))
			
	@staticmethod
	def Call(usr, friend):
		data = {}
		for (i, f) in enumerate(friend):
			data['friendid' + str(i)] = f[0]
			data['friendname' + str(i)] = f[1]['name']
		data['roleid'] = usr.roleid
		return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_call_relief/', None, data))
		
	@staticmethod
	def Ladder(usr, tp):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_ladder/', None, {'type':tp, 'rolelevel': usr.level}))
			
	@staticmethod
	def GetBattle(usr):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_get_battle/', None, {'roleid':usr.roleid}))
			
	@staticmethod
	def make():
		return {}
		
	@staticmethod
	def getClientData(usr):
		return {}
		
	@staticmethod
	def damage_ladder(usr):
		return infection.Ladder(usr, 'damage')
		
	@staticmethod
	def prestige_ladder(usr):
		return infection.Ladder(usr, 'prestige')
		
		
	@staticmethod
	def award(usr, battleRoleid, create_time):
		
		res = infection.Award(usr, battleRoleid, create_time)
		if res.has_key('msg'):
			return res
		
		awd = {}
		if res.has_key('call_dropid'):
			awd = drop.open(usr, res['call_dropid'], awd)
		if res.has_key('last_hit_dropid'):
			awd = drop.open(usr, res['last_hit_dropid'], awd)
		if res.has_key('hit_dropid'):
			awd = drop.open(usr, res['hit_dropid'], awd)			
		data = drop.makeData(awd, {})
		
		return data