#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config

class skill:
	
	@staticmethod
	def levelup(usr, destSkill_id, sourceSkill_id):
		
		inv = usr.getInventory()
		skillConf = config.getConfig('skill')
		skillLevelConf = config.getConfig('skill_level')
		
		destSkill = inv.getSkill(destSkill_id)
		if not destSkill:
			return {'msg':'skill_not_exist'}
		
		exp = 0		
		
		for skillid in sourceSkill_id:
			sk = inv.getSkill(skillid)
			if not sk:
				return {'msg':'skill_not_exist'}			
			exp = exp + skill.get_exp(sk, skillLevelConf)
			inv.delSkill(sk['id'])
			
		skill.gain_exp(destSkill, exp, skillConf, skillLevelConf)
		inv.save()
		return {'update_skill': destSkill, 'delete_skill_array': sourceSkill_id}

	@staticmethod
	def get_exp(sk, skillLevelConf):
		return skillLevelConf[sk['level'] - 1] + sk['exp']
		
	@staticmethod
	def gain_exp(sk, exp, skillConf, skillLevelConf):
		
		skillInfo = skillConf[sk['skillid']]
		exp = sk['exp'] + exp
		sk['exp'] = 0
		print exp
		while skillInfo['maxLevel'] >= sk['level'] and skillLevelConf[sk['level']] < exp:
			exp = exp - skillLevelConf[sk['level']]
			sk['level'] = sk['level'] + 1
					
		if sk['level'] == skillInfo['maxLevel']:
			sk['exp'] = 0
		else:
			sk['exp'] = exp
			
		