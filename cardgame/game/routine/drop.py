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
				msg = drop.award(usr, d, awd)
				if msg:				
					break				
			elif probablity < rd:
				rd = rd - probablity				
			else:
				msg = drop.award(usr, d, awd)				
				break		
		return awd
		
	@staticmethod
	def roll(dropid, awd):
		dropConf = config.getConfig('drop')
		
		rd = randbigint()
		dropInfo = dropConf[dropid]
		
		awd = {}		
		
		for d in dropInfo:
			probablity = d['probability']			
			msg = None
			if probablity == 1000000:
				msg = drop.award(usr, d, awd)
				if msg:				
					break				
			elif probablity < rd:
				rd = rd - probablity				
			else:
				msg = drop.award(usr, d, awd)				
				break
		return awd
		
	@staticmethod
	def make_award(dropItem, awd):
		if dropItem['type'] == 'st':			
			awd['st'] = awd['st'] + dropItem['count']			
		elif dropItem['type'] == 'gem':			
			awd['gem'] = awd['gem'] + dropItem['count']			
		elif dropItem['type'] == 'gold':			
			awd['gold'] = awd['gold'] + dropItem['count']			
		elif dropItem['type'] == 'sp':			
			awd['sp'] = awd['sp'] + dropItem['count']			
		elif dropItem['type'] == 'exp':			
			awd['exp'] = awd['exp'] + dropItem['count']			
		elif dropItem['type'] == 'stone':			
			if not awd.has_key('add_stone_array'):
				awd['add_stone_array'] = []
			awd['add_stone_array'].append({'id':dropItem['id'], 'count': dropItem['count']})			
		elif dropItem['type'] == 'eq':			
			if not awd.has_key('add_equipment_array'):
				awd['add_equipment_array'] = []
			awd['add_equipment_array'].append({'id':dropItem['id'], 'count':dropItem['count']})
		elif dropItem['type'] == 'card':						
			if not awd.has_key('add_card_array'):
				awd['add_card_array'] = []
			awd['add_card_array'].append({'id':dropItem['id'], 'count':dropItem['count']})
		elif dropItem['type'] == 'sk':			
			if not awd.has_key('add_skill_array'):
				awd['add_skill_array'] = []
			awd['add_skill_array'].append({'id':dropItem['id'], 'count':dropItem['count']})		
		return awd
		
	@staticmethod
	def do_award(usr, awd):
		save_user = False
		save_inv = False
		inv = None
		if awd.has_key('st'):
			usr.chargeStamina(awd['st'])
			awd['st'] = usr.stamina
			save_user = True
		if awd.has_key('gem'):
			usr.gem = usr.gem + awd['gem']
			awd['gem'] = usr.gem
			save_user = True
		if awd.has_key('gold'):
			usr.gold = usr.gold + awd['gold']
			awd['gold'] = usr.gold
			save_user = True
		if awd.has_key('sp'):
			usr.sp = usr.sp + awd['sp']
			awd['sp'] = usr.sp
			save_user = True
		if awd.has_key('exp'):
			usr.gainExp(awd['exp'])
			awd['level'] = usr.level
			awd['exp'] = awd.exp
			save_user = True
		if awd.has_key('stone'):
			if not inv:
				inv = usr.getInventory()
			stone = []
			for a in awd['add_stone_array']:
				stone.extend(inv.addStoneCount(a['id'], a['count']))
			awd['add_stone_array'] = stone
			save_inv = True
		if awd.has_key('eq'):
			if not inv:
				inv = usr.getInventory()
			equipment = []
			for a in awd['add_equipment_array']:
				equipment.extend(inv.addEquipmentCount(a['id'], a['count']))
			awd['add_equipment_array'] = equipment
			save_inv = True
		if awd.has_key('add_card_array'):
			if not inv:
				inv = usr.getInventory()
			card = []
			for a in awd['add_card_array']:
				card.extend(inv.addCardCount(a['id'], a['count']))
			awd['add_card_array'] = card
			save_inv = True
		if awd.has_key('add_skill_array'):
			if not inv:
				inv = usr.getInventory()
			skill = []
			for a in awd['add_skill_array']:
				skill.extend(inv.addSkillCount(a['id'], a['count']))
			awd['add_skill_array'] = skill
			save_inv = True
		if save_user:
			usr.save()
		if save_inv:
			inv.save()
		return awd
			
	
	@staticmethod
	def award(usr, dropItem, awd):
		save_user = False
		save_inv = False
		inv = None
		if dropItem['type'] == 'st':
			usr.chargeStamina(dropItem['count'])
			awd['st'] = usr.stamina
			save_user = True
		elif dropItem['type'] == 'gem':
			usr.gem = usr.gem + dropItem['count']
			awd['gem'] = usr.gem
			save_user = True
		elif dropItem['type'] == 'gold':
			usr.gold = usr.gold + dropItem['count']
			awd['gold'] = usr.gold
			save_user = True
		elif dropItem['type'] == 'sp':
			usr.sp = usr.sp + dropItem['count']
			awd['sp'] = usr.sp
			save_user = True
		elif dropItem['type'] == 'exp':
			usr.gainExp(dropItem['count'])
			awd['level'] = usr.level
			awd['exp'] = usr.exp
			save_user = True
		elif dropItem['type'] == 'stone':
			if not inv:
				inv = usr.getInventory()
			stone = inv.addStoneCount(dropItem['id'], dropItem['count'])
			if not awd.has_key('add_stone_array'):
				awd['add_stone_array'] = []
			awd['add_stone_array'].extend(stone)
			save_inv = True
		elif dropItem['type'] == 'eq':
			if not inv:
				inv = usr.getInventory()
			equipment = inv.addEquipmentCount(dropItem['id'], dropItem['count'])
			if not awd.has_key('add_equipment_array'):
				awd['add_equipment_array'] = []
			awd['add_equipment_array'].extend(equipment)
			save_inv = True
		elif dropItem['type'] == 'card':
			if not inv:
				inv = usr.getInventory()
			card = inv.addCardCount(dropItem['id'], dropItem['count'])
			if not awd.has_key('add_card_array'):
				awd['add_card_array'] = []
			awd['add_card_array'].extend(card)
			save_inv = True
		elif dropItem['type'] == 'sk':
			if not inv:
				inv = usr.getInventory()
			sk = inv.addSkillCount(dropItem['id'], dropItem['count'])
			if not awd.has_key('add_skill_array'):
				awd['add_skill_array'] = []
			awd['add_skill_array'].extend(sk)
			save_inv = True
		if save_user:
			usr.save()
		if save_inv:
			inv.save()
		return None
	     
	
		