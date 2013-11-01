#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config
from gclib.utility import currentTime

class equipment:

	@staticmethod
	def strengthen(usr, id, isUseGem):
		inv = usr.getInventory()
		
		equipment = inv.getEquipment(id)
		if not equipment:
			return {'msg':'equipment_not_found'}
				
		usr.updateFatigue()
		usr.updateEquipmentStrengthCooldown()
		goldCost = 0
		gemCost = 0
		
		gameConf = config.getConfig('game')
		
		if gameConf['equipment_strength_cooldown_cumulate_max'] < usr.equipment_strength_cooldown:
			return {'msg':'equipment_strength_cooldown_max'}
		
		
		
		equipmentConf = config.getConfig('equipment')[equipment['equipmentid']]
		strengthenPriceConf = config.getConfig('strength_price')
		
		equipmentQuality = equipmentConf['quality']
		strengthLevel = equipment['strengthLevel']
		strengthenProbability = 0
		if strengthLevel >= gameConf['equipment_max_level']:
			return {'msg':'equipment_level_max'}
			
		if strengthLevel > gameConf['equipment_strength_fix_probablity_level']:
			strengthenProbability = equipment.getStrengthCurrentProbability()
		else:
			strengthenProbability = gameConf['equipment_strength_fix_probablity']
		
		goldCost = strengthenPriceConf[equipmentQuality][strengthLevel]['price']
		
		if isUseGem:
			gemCost = gemCost + gameConf['equipment_strength_extra_gem_price']
			
		if usr.gold < goldCost:
			return {'msg':'gold_not_enough'}
		if usr.gem < gemCost:
			return {'msg':'gem_not_enough'}
				
		usr.equipment_strength_cooldown = usr.equipment_strength_cooldown + (gameConf['equipment_strength_cooldown_base'] * (1 + usr.fatigue / 2))
		usr.equipment_strength_last_time = currentTime()
		usr.fatigue = usr.fatigue + 1
		usr.fatigue_last_time = currentTime()
		
		equipment['strengthLevel'] = strengthLevel + 1
		
		usr.gold = usr.gold - goldCost
		usr.gem = usr.gem - gemCost
		
		inv.save()		
		usr.save()
		data = {}
		data['equipment_strength'] = equipment
		data['equipment_strength_cooldown'] = usr.equipment_strength_cooldown
		if goldCost:
			data['gold'] = usr.gold
		if gemCost:
			data['gem'] = usr.gem
		return data
		
			
	@staticmethod		
	def getStrengthCurrentProbability():
		strengthProbabilityConf = config.getConfig('strength_probability')
		now = currentTime()
		daysecond = dayTime()
		
		selItem = None
		for item in strengthenPriceConf:
			if item[0] < daysecond:
				selItem = item
			else:
				break				
		return (selItem[1][0] + selItem[1][2]) / 2
		
	@staticmethod
	def equip(usr, id):
		inv = usr.getInventory()
		equipment = inv.getEquipment(id)
		if not equipment:
			{'msg':'equipment_not_exist'}
		
		equipmentConf = config.getConfig('equipment')
		equipmentInfo = equipmentConf[equipment['equipmentid']]
		
		
		oldEquipment = inv.slot[equipmentInfo['position']]
		
		if oldEquipment:
			inv.depositEquipment(oldEquipment)
		inv.slot[equipmentInfo['position']] = equipment
		inv.equipment.remove(equipment)
		inv.save()
		
		return{'solt':inv.slot, 'equipment_delete':id}
		
		
	def unequip(usr, id):
		inv = usr.getInventory()
		
		slotEquipment = None
		
		for i in range(len(inv.slot)):
			pass
		
		
		if not slotEquipment:
			return {'msg': 'equipment_not_exist'}
		
		inv.depositEquipment(slotEquipment)
		