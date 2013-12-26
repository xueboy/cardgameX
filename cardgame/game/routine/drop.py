#coding:utf-8
#!/usr/bin/env python

from gclib.utility import randbigint
from game.utility.config import config

class drop:
	@staticmethod
	def open(usr, dropid, awd):
		dropConf = config.getConfig('drop')
		
		rd = randbigint()
		dropInfo = dropConf[dropid]
		
		awd = {}
		
		for d in dropInfo:
			probablity = d['probability']
			msg = None
			if probablity == 1000000:
				msg = drop.award(usr, dropInfo, awd)
				if msg:
					break
			elif probablity < rd:
				rd = rd - probablity
			else:
				msg = drop.award(usr, dropInfo, awd)
				break
		return awd
						
	
	@staticmethod
	def award(usr, dropInfo, awd):		
		if dropInfo['type'] == 'st':
			usr.chargeStamina(dropInfo['count'])
			awd['st'] = usr.stamina
			usr.save()
		elif dropInfo['type'] == 'gem':
			usr.gem = usr.gem + dropInfo['count']
			awd['gem'] = usr.gem
			usr.save()
		elif dropInfo['type'] == 'sp':
			usr.sp = usr.sp + dropInfo['count']
			awd['sp'] = usr.sp
			usr.save()
		elif dropInfo['type'] == 'exp':
			usr.gainExp(dropInfo['count'])
			awd['level'] = usr.level
			awd['exp'] = usr.exp
			usr.save()
		elif dropInfo['type'] == 'stone':
			inv = usr.getInventory()
			stone = inv.addStoneCount(dropInfo['id'], dropInfo['count'])
			if not awd.has_key('add_stone_array'):
				awd['add_stone_array'] = []
			awd['add_stone_array'].extend(stone)
			inv.save()
		elif dropInfo['type'] == 'eq':
			inv = usr.getInventory()
			equipment = inv.addEquipmentCount(dropInfo['id'], dropInfo['count'])
			if not awd.has_key('add_equipment_array'):
				awd['add_equipment_array'] = []
			awd['add_equipment_array'].extend(equipment)
			inv.save()
		elif dropInfo['type'] == 'card':
			inv = usr.getInventory()
			card = inv.addCardCount(dropInfo['id'], dropInfo['count'])
			if not awd.has_key('add_card_array'):
				awd['add_card_array'] = []
			awd['add_card_array'].extend(card)
			inv.save()
		elif dropInfo['type'] == 'sk':
			inv = usr.getInventory()
			sk = inv.addSkillCount(dropInfo['id'], dropInfo['count'])
			if not awd.has_key('add_skill_array'):
				awd['add_skill_array'] = []
			awd['add_skill_array'].extend(sk)
			inv.save()
	
	
		