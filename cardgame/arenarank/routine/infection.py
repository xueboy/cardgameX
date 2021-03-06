﻿#coding:utf-8
#!/usr/bin/env python

from arenarank.models.infection_arena import infection_arena

class infection:
	
	@staticmethod
	def encounter(roleid, rolename):
		"""
		遭遇战斗
		"""
		ia = infection_arena.instance()	
		return ia.encounter(roleid, rolename)
		
	@staticmethod
	def beat(roleid, rolelevel, rolename, battleRoleid, damage):
		"""
		击败
		"""
		ia = infection_arena.instance()
		return ia.beat(roleid, rolelevel, rolename, battleRoleid, damage)
		
	@staticmethod
	def battle_award(roleid, battleRoleid, create_time):
		"""
		战斗反馈
		"""
		ia = infection_arena.instance()
		return ia.get_battle_award(roleid, battleRoleid, create_time)
		
	@staticmethod
	def prestige_award(roleid, rolelevel):
		"""
		声望回馈
		"""
		ia = infection_arena.instance()
		return ia.get_prestige_award(roleid, rolelevel)
		
	@staticmethod
	def get_battle(roleid):
		"""
		得到战斗
		"""
		ia = infection_arena.instance()
		return ia.get_infection_battle(roleid)
		
	@staticmethod
	def call_relief(roleid, friendid):
		"""
		援军
		"""
		ia = infection_arena.instance()
		return ia.call_relief(roleid, friendid)
		
	@staticmethod
	def get_infection_battle(roleid):
		"""
		得到感染战斗
		"""
		ia = infection_arena.instance()
		return ia.get_infection_battle(roleid)
		
	@staticmethod
	def ladder(pt, rolelevel):
		"""
		天梯
		"""
		ia = infection_arena.instance()
		if tp == 'damage':
			return ia.damdage_ladder_list(rolelevel)
		elif tp == 'prestige':
			return ia.prestige_ladder_list(rolelevel)
		return {'msg':'infection_bad_ladder_type'}
			
	@staticmethod
	def user_info(roleid):
		"""
		用户信息
		"""
		ia = infection_arena.instance()
		return ia.user_info(roleid)
		
	@staticmethod
	def reset_prestige_score(roleid):
		"""
		重置声望分数
		"""
		ia = infection_arena.instance()
		return ia.reset_prestige_score(roleid)