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
	def install(usr, teamPosition, slotpos, skill_id):
		inv = usr.getInventory()
		
		if not inv.team[teamPosition]:
			return {'msg':'team_position_not_have_member'}				
		card = inv.getCard(inv.team[teamPosition])
		if not card:
			return {'msg': 'card_not_exist'}
		if not card.has_key('sk_slot'):
			card['sk_slot'] = skill.make_sk_slot()
			
		oldsk = card['sk_slot'][slotpos]
		sk = inv.withdrawSkill(skill_id)
		
		if not sk:
			return {'msg':'skill_not_exist'}
				
		card['sk_slot'][slotpos] = sk
		
		if oldsk:
			inv.depositSkill(oldsk)
		
		inv.save()
		
		data = {}
		data['sk_slot'] = inv.getSkSlots()
		if oldsk:
			data['add_skill'] = oldsk
	
		return data
	

	@staticmethod
	def get_exp(sk, skillLevelConf):
		return skillLevelConf[sk['level'] - 1] + sk['exp']
		
	@staticmethod
	def gain_exp(sk, exp, skillConf, skillLevelConf):
		
		skillInfo = skillConf[sk['skillid']]
		exp = sk['exp'] + exp
		sk['exp'] = 0
		while skillInfo['maxLevel'] >= sk['level'] and skillLevelConf[sk['level']] < exp:
			exp = exp - skillLevelConf[sk['level']]
			sk['level'] = sk['level'] + 1
					
		if sk['level'] == skillInfo['maxLevel']:
			sk['exp'] = 0
		else:
			sk['exp'] = exp
	
	@staticmethod
	def make_sk_slot():
		return [{}, {}, {}]		
	
	@staticmethod
	def getClientData():
		pass
		
	@staticmethod
	def takeoff(inv, card):
		dst = []
		if card and card.has_key('sk_slot'):
			for st in card['sk_slot']:
				if st:
					inv.depositStone(st)
					dst.append(st)
			del card['sk_slot']
		return dst

	@staticmethod
	def exchage(inv, fromCard, toCard, gameConf):				
				
		toSlot = None		
		if toCard.has_key('sk_slot'):
			toSlot = toCard['sk_slot']			
		toCard['sk_slot'] = fromCard['sk_slot']
		del fromCard['sk_slot']
		dst = []
		if toSlot:
			fromCard['sk_slot'] = toSlot		
		return dst	