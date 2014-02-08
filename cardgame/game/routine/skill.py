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
	def install(usr, teamPosition, ownerTeamPosition, slotpos, skill_id):
		inv = usr.getInventory()
		
		if not inv.team[teamPosition]:
			return {'msg':'team_position_not_have_member'}
		card = inv.getCard(inv.team[teamPosition])
		if not card:
			return {'msg': 'card_not_exist'}
		
		gameConf = config.getConfig('game')
		if usr.level < gameConf['skill_slot_level'][slotpos]:
			return {'msg':'level_required'}
		
		if not card.has_key('sk_slot'):
			card['sk_slot'] = skill.make_sk_slot()
			
		oldsk = card['sk_slot'][slotpos]
		
		sk = None
		owner = None
		if ownerTeamPosition < 0:
			sk = inv.withdrawSkill(skill_id)
		else:
			ownerid = inv.team[ownerTeamPosition]
			if not ownerid:
				return {'msg':'team_position_not_have_member'}
			owner = inv.getCard(ownerid)
			if not owner:
				return {'msg': 'card_not_exist'}
			for i, s in enumerate(owner['sk_slot']):
				if s and s['id'] == skill_id:
					sk = s
					owner['sk_slot'][i] = {}
					break			
		
		if not sk:
			return {'msg':'skill_not_exist'}
				
		card['sk_slot'][slotpos] = sk
		
		if oldsk:
			inv.depositSkill(oldsk)	
		
		inv.save()		
		data = {}
		#data['sk_slot'] = inv.getSkSlots()
		#if not owner:
		#	data['delete_skill'] = skill_id
		#if oldsk:
		#	data['add_skill'] = oldsk
	
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
		return [{}, {}, {}, {}]		
	
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
		
	@staticmethod		
	def decompose(usr, skillids):
		
		cards = []
		inv = usr.getInventory()
		trpConfig = config.getConfig('trp')
		
		total_trp = 0		
		for skillid in skillids:
			sk = inv.getSkill(skillid)
			if not sk:
				return {'msg':'skill_not_exist'}
			trp = trpConfig[sk['level'] - 1]['skill']
			total_trp = total_trp + trp
			if inv.delSkill(skillid) != 1:
				return {'msg':'decompose_faild'}
			
		usr.trp = usr.trp + total_trp
		
		usr.save()
		inv.save()
		return {'trp':usr.trp, 'delete_skill_array':skillids}
			