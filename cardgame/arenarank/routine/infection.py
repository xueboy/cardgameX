#coding:utf-8
#!/usr/bin/env python

from arenarank.models.infection_arena import infection_arena

class infection:
	
	@staticmethod
	def encounter(roleid, rolename):
		ia = infection_arena.instance()	
		return ia.encounter(roleid, rolename)
		
	@staticmethod
	def beat(roleid, rolelevel, rolename, battleRoleid, damage):
		ia = infection_arena.instance()
		return ia.beat(roleid, rolelevel, rolename, battleRoleid, damage)
		
	@staticmethod
	def award(roleid, battleRoleid, create_time):
		ia = infection_arena.instance()
		return ia.get_battle_award(roleid, battleRoleid, create_time)
		
	@staticmethod
	def get_battle(roleid):
		ia = infection_arena.instance()
		return ia.get_infection_battle(roleid)
		
	@staticmethod
	def call_relief(roleid, friendid):
		ia = infection_arena.instance()
		return ia.call_relief(roleid, friendid)
		
	@staticmethod
	def get_infection_battle(roleid):
		ia = infection_arena.instance()
		return ia.get_infection_battle(roleid)
		
	@staticmethod
	def ladder(pt, rolelevel):
		ia = infection_arena.instance()
		if tp == 'damage':
			return ia.damdage_ladder_list(rolelevel)
		elif tp == 'prestige':
			return ia.prestige_ladder_list(rolelevel)
		return {'msg':'infection_bad_ladder_type'}
			
	