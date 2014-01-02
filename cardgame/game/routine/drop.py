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
		
		print dropInfo
		for d in dropInfo:
			probablity = d['probability']
			print d
			msg = None
			if probablity == 1000000:
				msg = drop.award(usr, d, awd)
				if msg:
					print msg.a
					break
			elif probablity < rd:
				rd = rd - probablity
			else:
				msg = drop.award(usr, d, awd)
				break
		return awd
						
	
	@staticmethod
	def award(usr, dropItem, awd):		
		if dropItem['type'] == 'st':
			usr.chargeStamina(dropItem['count'])
			awd['st'] = usr.stamina
			usr.save()
		elif dropItem['type'] == 'gem':
			usr.gem = usr.gem + dropItem['count']
			awd['gem'] = usr.gem
			usr.save()
		elif dropItem['type'] == 'sp':
			usr.sp = usr.sp + dropItem['count']
			awd['sp'] = usr.sp
			usr.save()
		elif dropItem['type'] == 'exp':
			usr.gainExp(dropItem['count'])
			awd['level'] = usr.level
			awd['exp'] = usr.exp
			usr.save()
		elif dropItem['type'] == 'stone':
			inv = usr.getInventory()
			stone = inv.addStoneCount(dropItem['id'], dropItem['count'])
			if not awd.has_key('add_stone_array'):
				awd['add_stone_array'] = []
			awd['add_stone_array'].extend(stone)
			inv.save()
		elif dropItem['type'] == 'eq':
			inv = usr.getInventory()
			equipment = inv.addEquipmentCount(dropItem['id'], dropItem['count'])
			if not awd.has_key('add_equipment_array'):
				awd['add_equipment_array'] = []
			awd['add_equipment_array'].extend(equipment)
			inv.save()
		elif dropItem['type'] == 'card':
			inv = usr.getInventory()
			card = inv.addCardCount(dropItem['id'], dropItem['count'])
			if not awd.has_key('add_card_array'):
				awd['add_card_array'] = []
			awd['add_card_array'].extend(card)
			inv.save()
		elif dropItem['type'] == 'sk':
			inv = usr.getInventory()
			sk = inv.addSkillCount(dropItem['id'], dropItem['count'])
			if not awd.has_key('add_skill_array'):
				awd['add_skill_array'] = []
			awd['add_skill_array'].extend(sk)
			inv.save()
		return None
	
	
		