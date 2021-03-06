﻿#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import is_same_day, currentTime, randint
from cardgame.settings import ARENE_SERVER, SIGLE_SERVER
from game.models.network import network
from game.utility.config import config
from game.routine.drop import drop
from game.routine.vip import vip

class infection:
	
	@staticmethod
	def dungeon_encounter(usr):
		"""
		感染地下城遇敌
		"""
		rd = randint()
		gameConf = config.getConfig('game')
		print rd, gameConf['infection_dungeon_probability']
		if rd < gameConf['infection_dungeon_probability']:
			res = infection.Encount(usr)
			if not res.has_key('msg'):
				return res							
		return {}
		
	@staticmethod
	def explore_encounter(usr, gameConf):
		"""
		感染探索遇敌
		"""
		rd = randint()
		if rd < gameConf['infection_explore_probability']:
			res = infection.Encount(usr)
			if not res.has_key('msg'):
				return res
		return {}
				
	@staticmethod
	def encounter(usr):
		"""
		遇敌
		"""
		return infection.Encount(usr)
		
	@staticmethod
	def beat(usr, battle_roleid, damage):
		"""
		击败
		"""
		gameConf = config.getConfig('game')		
		if usr.costIp(gameConf['infection_point_cost']) < 0:
			return {'msg' : 'ip_not_enough'}			
		
		res = infection.Beat(usr, battle_roleid, damage)		
		if res.has_key('msg'):
			return res
		data = res
		data['ip'] = usr.ip
		usr.save()
		return data
				
	@staticmethod
	def Beat(usr, battle_roleid, damage):		
		"""
		击败
		"""
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
		"""
		招唤
		"""
		nw = usr.getNetwork()		
		friend = nw.friend.items()
		res = infection.Call(usr, friend)
		if res.has_key('msg'):
			return res
		return res
	
	@staticmethod
	def get_battle(usr):
		"""
		得到战斗
		"""
		return infection.GetBattle(usr)
		
	@staticmethod
	def Encount(usr):
		"""
		遇敌
		"""
		if SIGLE_SERVER:
			from arenarank.routine.infection import infection as infectionR
			return infectionR.encounter(str(usr.roleid), usr.name)
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_encounter/', None, {'roleid':str(usr.roleid), 'rolename': usr.name}))
			
	@staticmethod
	def BattleAward(usr, battleRoleid, create_time):
		"""
		站斗奖励
		"""
		if SIGLE_SERVER:
			from arenarank.routine.infection import infection as infectionR
			return infectionR.award(str(usr.roleid), battleRoleid, create_time)
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_battle_award/', None, {'roleid':str(usr.roleid), 'battle_roleid': battleRoleid, 'create_time':create_time}))
			
	@staticmethod
	def Call(usr, friend):
		"""
		呼叫援军
		"""
		if SIGLE_SERVER:
			from arenarank.routine.infection import infection as infectionR
			return infectionR.call_relief(str(usr.roleid), friend)
		else:
			data = {}
			for (i, f) in enumerate(friend):
				data['friendid' + str(i)] = f[0]
				data['friendname' + str(i)] = f[1]['name']
			data['roleid'] = usr.roleid
			return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_call_relief/', None, data))
		
	@staticmethod
	def Ladder(usr, tp):
		"""
		天梯
		"""
		if SIGLE_SERVER:
			from arenarank.routine.infection import infection as infectionR
			return infectionR.ladder(tp, str(usr.roleid))
		else:			
			return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_ladder/', None, {'type':tp, 'rolelevel': usr.level}))
			
	@staticmethod
	def GetBattle(usr):
		"""
		得到战斗
		"""
		if SIGLE_SERVER:
			from arenarank.routine.infection import infection as infectionR
			return infectionR.get_battle(str(usr.roleid))
		else: 
			return json.loads(curl.url(ARENE_SERVER +  '/arena/infection_get_battle/', None, {'roleid':usr.roleid}))
				
	@staticmethod
	def PrestigeAward(usr):
		"""
		声望奖励
		"""
		if SIGLE_SERVER:
			from arenarank.routine.infection import infection as infectionR
			return infectionR.prestige_award(str(usr.roleid), usr.level)
		else:
			return json.loads(curl.url(ARENE_SERVER + '/arena/infiection_prestige_award/', None, {'roleid':usr.roleid, 'rolelevel': usr.level}))
	
	@staticmethod
	def Info(usr):
		"""
		感染信息
		"""
		if SIGLE_SERVER:
			from arenarank.routine.infection import infection as infectionR
			return infectionR.user_info(str(usr.roleid))
		else: 
			return json.loads(curl.url(ARENE_SERVER + '/arena/infection_info/', None, {'roleid':usr.roleid}))
				
	@staticmethod
	def ResetPrestigeScore(usr):
		"""
		重置声望分数
		"""
		if SIGLE_SERVER:
			from arenarank.routine.infection import infection as infectionR
			return infectionR.reset_prestige_score(str(usr.roleid))
		else: 
			return json.loads(curl.url(ARENE_SERVER + '/arena/infection_reset_prestige_score/', None, {'roleid':usr.roleid}))
	
	@staticmethod
	def make():
		"""
		制做
		"""
		return {'prestige_score_reset_count':0}
		
	@staticmethod
	def getClientData(usr):
		"""
		得到 client data
		"""
		return {}
		
	@staticmethod
	def damage_ladder(usr):
		"""
		伤害天梯
		"""
		return infection.Ladder(usr, 'damage')
		
	@staticmethod
	def prestige_ladder(usr):
		"""
		声望天梯
		"""
		return infection.Ladder(usr, 'prestige')
		
		
	@staticmethod
	def battle_award(usr, battleRoleid, create_time):
		"""
		战斗奖励
		"""
		res = infection.BattleAward(usr, battleRoleid, create_time)
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
		
	@staticmethod
	def prestige_award(usr):
		"""
		声望奖励
		"""
		res = infection.PrestigeAward(usr)
		if res.has_key('msg'):
			return res
		
		awd = {}
		for dropid in res['award']:
			awd = drop.open(usr, dropid, awd)
		data = drop.makeData(awd, {})
		
		return data
		
	@staticmethod
	def info(usr):
		"""
		感染信息
		"""
		return infection.Info(usr)
		
	@staticmethod
	def reset_prestige_score(usr):	
		"""
		重置声望分数
		"""
		usr.infection['prestige_score_reset_count'] = usr.infection['prestige_score_reset_count'] + 1
		if not vip.canResetInfectionPrestigeScoreCount(usr):
			return {'msg':'vip_required'}
		usr.save()
		return {'infection_prestige_score_reset_count': usr.infection['prestige_score_reset_count']}