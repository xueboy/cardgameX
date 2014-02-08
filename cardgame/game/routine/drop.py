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
				msg = drop.make_award(d, awd)
				if msg:				
					break
			elif probablity < rd:
				rd = rd - probablity				
			else:
				msg = drop.make_award(d, awd)				
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
		elif dropItem['type'] == 'item':
			if not awd.has_key('add_item_array'):
				awd['add_item_array'] = []
			awd['add_item_array'].append({'id':dropItem['id'], 'count':dropItem['count']})
		return awd
		
	@staticmethod
	def do_award(usr, awd, data):
		save_user = False
		save_inv = False
		inv = None
		if awd.has_key('st'):
			usr.chargeStamina(awd['st'])
			data['st'] = usr.stamina
			save_user = True
		if awd.has_key('gem'):
			usr.gem = usr.gem + awd['gem']
			data['gem'] = usr.gem
			save_user = True
		if awd.has_key('gold'):
			usr.gold = usr.gold + awd['gold']
			data['gold'] = usr.gold
			save_user = True
		if awd.has_key('sp'):
			usr.sp = usr.sp + awd['sp']
			data['sp'] = usr.sp
			save_user = True
		if awd.has_key('exp'):
			usr.gainExp(awd['exp'])
			data['level'] = usr.level
			data['exp'] = awd.exp
			save_user = True
		if awd.has_key('stone'):
			if not inv:
				inv = usr.getInventory()
			stone = []
			for a in awd['add_stone_array']:
				stone.extend(inv.addStoneCount(a['id'], a['count']))
			if not data.has_key('add_stone_array'):
				data['add_stone_array'] = []
			data['add_stone_array'].extend(stone)
			save_inv = True
		if awd.has_key('eq'):
			if not inv:
				inv = usr.getInventory()
			equipment = []
			for a in awd['add_equipment_array']:
				equipment.extend(inv.addEquipmentCount(a['id'], a['count']))
			if not data.has_key('add_equipment_array'):
				data['add_equipment_array'] = []
			data['add_equipment_array'].extend(equipment)			
			save_inv = True
		if awd.has_key('add_card_array'):
			if not inv:
				inv = usr.getInventory()
			card = []
			for a in awd['add_card_array']:
				card.extend(inv.addCardCount(a['id'], a['count']))
			if not data.has_key('add_card_array'):
				data['add_card_array'] = []
			data['add_card_array'].extend(card)
			save_inv = True
		if awd.has_key('add_skill_array'):
			if not inv:
				inv = usr.getInventory()
			skill = []
			for a in awd['add_skill_array']:
				skill.extend(inv.addSkillCount(a['id'], a['count']))
			if not data.has_key('add_skill_array'):
				data['add_card_array'] = []
			data['add_card_array'].extend(skill)
			save_inv = True
		if awd.has_key('add_item_array'):
			if not inv:
				inv = usr.getInventory()
			updateItem = []
			newItem = []
			for a in awd['add_item_array']:
				updateIt , newIt = inv.addItemCount(a['id'], a['count'])
				updateItem.extend(updateIt)
				newItem.extend(newIt)
			if not data.has_key('add_item_array'):
				data['add_card_array'] = []
			if not data.has_key('update_item_array'):
				data['update_item_array'] = []
			data['add_item_array'].extend(newItem)
			data['update_item_array'].extend(updateItem)			
			save_inv = True
		if save_user:
			usr.save()
		if save_inv:
			inv.save()
		return data
			
	
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
		elif dropItem['type'] == 'item':
			if not inv:
				inv = usr.getInventory()
			updateIt, newIt = inv.addItemCount(dropItem['id'], dropItem['count'])
			if (not awd.has_key('add_item_array')) and newIt:
				awd['add_item_array'] = []
			if (not awd.has_key('update_item_array')) and updateIt:
				awd['update_item_array'] = []			
			if newIt:
				awd['add_item_array'].extend(newIt)
			if updateIt:
				awd['update_item_array'].extend(updateIt)
			save_inv = True
		if save_user:
			usr.save()
		if save_inv:
			inv.save()
		return None
		
		
	@staticmethod
	def makeData(awd):		
		dropData = []
		if awd.has_key('st'):
			dropData.append({'type':11, 'count':awd['st']})
		if awd.has_key('gem'):
			dropData.append({'type':6, 'count':awd['gem']})
		if awd.has_key('gold'):
			dropData.append({'type':10, 'count':awd['gold']})
		if awd.has_key('sp'):
			dropData.append({'type':8, 'count':awd['sp']})	  	
		if awd.has_key('exp'):
			dropData.append({'type':9, 'count':awd['exp']})
			dropData.append({'type':12, 'count':awd['level']})
		if awd.has_key('add_stone_array'):
			for st in awd['add_stone_array']:
				dropData.append({'type':5, 'count':1, 'insId':st['id'], 'id':st['stoneid']})	  				
		if awd.has_key('add_equipment_array'):
			for eq in awd['add_equipment_array']:
				dropData.append({'type':3, 'count':1, 'insId':eq['id'], 'id':eq['equipmentid']})
		if awd.has_key('add_card_array'):
			for card in awd['add_card_array']:
				dropData.append({'type':1, 'count':1, 'insId':card['id'], 'id':card['cardid']})
		if awd.has_key('add_skill_array'):
			for sk in awd['add_skill_array']:
				dropData.append({'type':2, 'count':1, 'insId':sk['id'], 'id':sk['skillid']})
		if awd.has_key('add_item_array'):
			for it in awd['add_item_array']:
				dropData.append({'type':4, 'count':it['count'], 'insId':it['id'], 'id':it['itemid']})
		if awd.has_key('update_item_array'):
			for it in awd['update_item_array']:
				dropData.append({'type':4, 'count':it['count'], 'insId':it['id'], 'id':it['itemid']})		
		return {'drop':dropData}
		