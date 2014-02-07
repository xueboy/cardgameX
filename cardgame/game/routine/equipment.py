﻿#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config
from gclib.utility import currentTime

class equipment:

	@staticmethod
	def strengthen(usr, id, isUseGem):
		inv = usr.getInventory()
		
		equipment = inv.getEquipment(id)
		if not equipment:
			return {'msg':'equipment_not_exist'}
				
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
		strengthenProbability = 0
		strengthLevel = 0
		if equipment.has_key('strengthLevel'):
			strengthLevel = equipment['strengthLevel']
		
		if strengthLevel >= gameConf['equipment_max_level']:
			return {'msg':'equipment_level_max'}
			
		if strengthLevel > gameConf['equipment_strength_fix_probablity_level']:
			strengthenProbability = equipment.currentStrengthCurrentProbability()
		else:
			strengthenProbability = gameConf['equipment_strength_fix_probablity']
		
		goldCost = strengthenPriceConf[str(equipmentQuality)][strengthLevel]['price']
		
		if isUseGem:
			gemCost = gemCost + gameConf['equipment_strength_extra_gem_price']
			
		if usr.gold < goldCost:
			return {'msg':'gold_not_enough'}
		if usr.gem < gemCost:
			return {'msg':'gem_not_enough'}
				
		usr.equipment_strength_cooldown = usr.equipment_strength_cooldown + (gameConf['equipment_strength_cooldown_base'] * (1 + usr.fatigue / 6))
		usr.equipment_strength_last_time = currentTime()
		usr.fatigue = usr.fatigue + 1
		if usr.fatigue > gameConf['equipment_strength_fatigue_max']:
			usr.fatigue = gameConf['equipment_strength_fatigue_max']
		usr.fatigue_last_time = currentTime()
		
		equipment['strengthLevel'] = strengthLevel + 1
		
		usr.gold = usr.gold - goldCost
		usr.gem = usr.gem - gemCost
		
		inv.save()		
		usr.save()
		data = {}
		data['equipment_strength_level'] = equipment['strengthLevel']
		data['equipment_strength_cooldown'] = usr.equipment_strength_cooldown
		if goldCost:
			data['gold'] = usr.gold
		if gemCost:
			data['gem'] = usr.gem
		return data
		
	@staticmethod
	def strengthen_reset(usr):
		
		if usr.equipment_strength_cooldown <= 0:
			return {'msg':'equipment_strength_not_in_cooldown'}
		
		
		gameConf = config.getConfig('game')
		
		gemCost = int(usr.equipment_strength_cooldown * gameConf['equipment_strength_cooldown_reset_price_N'])
		
		if usr.gem < gemCost:
			return {'msg':'gem_not_enough'}
				
		usr.gem = usr.gem - gemCost
		usr.equipment_strength_cooldown = 0
		return {'equipment_strength_cooldown':usr.equipment_strength_cooldown, 'gem':usr.gem}
		
		
					
	@staticmethod		
	def currentStrengthCurrentProbability():
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
	def equip(usr, teamPosition, ownerTeamPosition, equipmentid):
		inv = usr.getInventory()
		
		cardid = inv.team[teamPosition]
		
		if not cardid:
			return {'msg': 'team_position_not_have_member'}
		
		equipment = None
		owner = None
		if ownerTeamPosition >= 0:
			ownerCardid = inv.team[ownerTeamPosition]
			if not ownerCardid:
				return {'msg': 'team_position_not_have_member'}
			owner = inv.getCard(ownerCardid)
			if not owner:
				return {'msg':'card_not_exist'}
			for equip in owner['slot']:
				if equip and equip['id'] == equipmentid:
					equipment = equip
					break			
		else:
			equipment = inv.getEquipment(equipmentid)			
			
		if not equipment:
			return {'msg':'equipment_not_exist'}		
		
		equipmentConf = config.getConfig('equipment')
		equipmentInfo = equipmentConf[equipment['equipmentid']]
				
		card = inv.getCard(cardid)
		if not card:
			return {'msg':'card_not_exist'}
		
		if not card.has_key('slot'):
			card['slot'] = equipment.make_slot()
		
		oldEquipment = card['slot'][equipmentInfo['position'] - 1]
		
		if oldEquipment:
			inv.depositEquipment(oldEquipment)
			if oldEquipment['id'] == equipmentid:
				card['slot'][equipmentInfo['position'] - 1] = {}
				inv.save()
				return {}
		card['slot'][equipmentInfo['position'] - 1] = equipment
		if owner:
			owner['slot'][equipmentInfo['position'] - 1] = {}
		else:
			inv.equipment.remove(equipment)
		inv.save()		
		data = {}
		#data['slot'] = inv.getSlots()
		#if not owner:
		#	data['equipment_delete'] = equipmentid		
		return data
			
	@staticmethod
	def make_slot():
		return [{}, {}, {}, {}, {}]
	
			
	@staticmethod
	def sell(usr, equipmentid):
		inv = usr.getInventory()		
		equipment = inv.getEquipment(equipmentid)
		
		if not equipment:
			return {'msg':'equipment_not_exist'}
		
		equipmentConf = config.getConfig('equipment')
		equipmentInfo = equipmentConf[equipment['equipmentid']]
		
		sellGold = equipmentInfo['price']		
		usr.gold = usr.gold + sellGold		
		inv.delEquipment(equipmentid)
		inv.save()
		usr.save()
		
		return {'gold':usr.gold, 'delete_equipment':equipmentid}		
		
	@staticmethod
	def takeoff(inv, card):
		deq = []
		if card and card.has_key('slot'):
			for equip in card['slot']:
				if equip:
					deq.append(equip)
					inv.depositEquipment(equip)
		del card['slot']
		return deq

	@staticmethod
	def exchage(inv, fromCard, toCard, gameConf):
		
		toSlot = None
		if toCard.has_key('slot'):
			toSlot = toCard['slot']			
		toCard['slot'] = fromCard['slot']
		del fromCard['slot']
		if toSlot:
			fromCard['slot'] = toSlot
		return []		
			
			
			
	@staticmethod
	def pvpProperty(card, slot, equipmentConf):
		
		equipment = card['slot'][slot]
		if not equipment:
			return {}
		
		equipmentInfo = equipmentConf[equipment['equipmentid']]
		
		ppData = {}
		ppData['attack'] = 0
		if equipment.has_key('strengthLevel'):
			ppData['hp'] = equipmentInfo['hp'] + equipmentInfo['hpgrowth'] * equipment['strengthLevel']			
			ppData['pa'] = equipmentInfo['pa'] + equipmentInfo['pagrowth'] * equipment['strengthLevel']
			ppData['ma'] = equipmentInfo['ma'] + equipmentInfo['magrowth'] * equipment['strengthLevel']
			ppData['pd'] = equipmentInfo['pd'] + equipmentInfo['pdgrowth'] * equipment['strengthLevel']
			ppData['md'] = equipmentInfo['md'] + equipmentInfo['mdgrowth'] * equipment['strengthLevel']
			ppData['pt'] = equipmentInfo['pt'] + equipmentInfo['ptgrowth'] * equipment['strengthLevel']
			ppData['mt'] = equipmentInfo['mt'] + equipmentInfo['mtgrowth'] * equipment['strengthLevel']
		else:
			ppData['hp'] = equipmentInfo['hp']
			ppData['pa'] = equipmentInfo['pa']
			ppData['ma'] = equipmentInfo['ma']
			ppData['pd'] = equipmentInfo['pd']
			ppData['md'] = equipmentInfo['md']
			ppData['pt'] = equipmentInfo['pt']
			ppData['mt'] = equipmentInfo['mt']
					
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0				
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0
		ppData['mi'] = 0
		return data
		
	@staticmethod
	def degradation(usr, equipmentid):
		inv = usr.getInventory()
		equipment = inv.getEquipment(equipmentid)
		
		if not equipment:
			return {'msg':'equipment_not_exist'}
		
		if not equipment.has_key('strengthLevel'):
			return {'msg':'strength_level_required'}
				
		gameConf = config.getConfig('game')
		strengthenPriceConf = config.getConfig('strength_price')
		equipmentConf = config.getConfig('equipment')
		equipmentInfo = equipmentConf[equipment['equipmentid']]
		equipmentQuality = equipmentInfo['quality']		
		goldGain = int(strengthenPriceConf[str(equipmentQuality)][equipment['strengthLevel']]['price'] * gameConf['equipment_degradation_price_rate'])
		
		equipment['strengthLevel'] = equipment['strengthLevel'] - 1
		if equipment['strengthLevel'] <= 0:
			del equipment['strengthLevel']
		
		usr.gold = usr.gold + goldGain
		
		inv.save()
		usr.save()
		
		return {'gold':usr.gold, 'equipment_degradation':equipment}
		
		