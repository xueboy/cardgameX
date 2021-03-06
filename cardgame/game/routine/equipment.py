﻿#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config
from gclib.utility import currentTime, dayTime, drop
from game.routine.vip import vip

class equipment:

	@staticmethod
	def strengthen(usr, id, ownerTeamPosition, isUseGem):
		"""
		强化
		"""
		inv = usr.getInventory()
		equip = None
		owner = None
		if ownerTeamPosition >= 0:
			ownerCardid = inv.team[ownerTeamPosition]
			if not ownerCardid:
				return {'msg': 'team_position_not_have_member'}
			owner = inv.getCard(ownerCardid)
			if not owner:
				return {'msg':'card_not_exist'}
			for e in owner['slot']:
				if e and e['id'] == id:
					equip = e
					break			
		else:
			equip = inv.getEquipment(id)		
		if not equip:
			return {'msg':'equipment_not_exist'}
				
		usr.updateFatigue()
		usr.updateEquipmentStrengthCooldown()
		goldCost = 0
		gemCost = 0
		
		gameConf = config.getConfig('game')
		
		if gameConf['equipment_strength_cooldown_cumulate_max'] < usr.equipment_strength_cooldown:
			return {'msg':'equipment_strength_cooldown_max'}
		equipmentConf = config.getConfig('equipment')
		equipmentInfo = equipmentConf[equip['equipmentid']]
		strengthenPriceConf = config.getConfig('strength_price')
		
		equipmentQuality = equipmentInfo['quality']
		strengthenProbability = 0
		strengthLevel = 0
		if equip.has_key('strengthLevel'):
			strengthLevel = equip['strengthLevel']
		
		if strengthLevel >= usr.level:
			return {'msg':'level_required'}
		
		if strengthLevel >= gameConf['equipment_max_level']:
			return {'msg':'equipment_level_max'}
			
		if strengthLevel > gameConf['equipment_strength_fix_probablity_level']:
			strengthenProbability = equipment.currentStrengthCurrentProbability()
		else:
			strengthenProbability = gameConf['equipment_strength_fix_probablity']
		
		goldCost = strengthenPriceConf[str(equipmentQuality)][strengthLevel]
		
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
		
		point = 0
		if isUseGem or drop(strengthenProbability):
			point = 1		
			if vip.canStrengthEquipmentCritical(usr):
				rd = randint()
				for (i, prob) in enumerate(gameConf['equipment_strength_critical_probability']):
					if prob > rd:
						rd = rd - prob
					else:
						point = i
						break
		
		equip['strengthLevel'] = strengthLevel + point
		
		usr.gold = usr.gold - goldCost
		usr.gem = usr.gem - gemCost
		
		inv.save()		
		usr.save()
		data = {}
		data['equipment_strength_level'] = equip['strengthLevel']
		data['equipment_strength_cooldown'] = usr.equipment_strength_cooldown
		if goldCost:
			data['gold'] = usr.gold
		if gemCost:
			data['gem'] = usr.gem
		return data
		
	@staticmethod
	def strengthen_reset(usr):
		"""
		重置强化
		"""
		if usr.equipment_strength_cooldown <= 0:
			return {'msg':'equipment_strength_not_in_cooldown'}
		
		
		gameConf = config.getConfig('game')
		
		gemCost = int(usr.equipment_strength_cooldown / gameConf['equipment_strength_cooldown_reset_price_N'] + 1)
		
		if usr.gem < gemCost:
			return {'msg':'gem_not_enough'}
				
		usr.gem = usr.gem - gemCost
		usr.equipment_strength_cooldown = 0
		return {'equipment_strength_cooldown':usr.equipment_strength_cooldown, 'gem':usr.gem}
				
					
	@staticmethod		
	def currentStrengthCurrentProbability():
		"""
		当前的强化概率
		"""
		strengthProbabilityConf = config.getConfig('strength_probability')
		now = currentTime()
		daysecond = dayTime()
		
		selItem = None
		for item in strengthProbabilityConf:
			if item[0] < daysecond:
				selItem = item
			else:
				break				
		return (selItem[1][0] + selItem[1][1]) / 2
		
	@staticmethod
	def equip(usr, teamPosition, ownerTeamPosition, equipmentid):
		"""
		装备
		"""
		inv = usr.getInventory()
		
		cardid = inv.team[teamPosition]
		
		if not cardid:
			return {'msg': 'team_position_not_have_member'}
		
		equipment1 = None
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
					equipment1 = equip
					break			
		else:
			equipment1 = inv.getEquipment(equipmentid)
			
		if not equipment1:
			return {'msg':'equipment_not_exist'}		
		
		equipmentConf = config.getConfig('equipment')
		equipmentInfo = equipmentConf[equipment1['equipmentid']]
				
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
		card['slot'][equipmentInfo['position'] - 1] = equipment1
		if owner:
			owner['slot'][equipmentInfo['position'] - 1] = {}
		else:
			inv.equipment.remove(equipment1)
		inv.save()		
		data = {}
		#data['slot'] = inv.getSlots()
		#if not owner:
		#	data['equipment_delete'] = equipmentid		
		return data
			
	@staticmethod
	def make_slot():
		"""
		制做槽位
		"""
		return [{}, {}, {}, {}, {}]
	
			
	@staticmethod
	def sell(usr, equipmentid):
		"""
		卖出装备
		"""
		inv = usr.getInventory()		
		
		sellequipment = []
		
		for equipid in equipmentid:
			equipment = inv.getEquipment(equipid)
					
			if not equipment:
				return {'msg':'equipment_not_exist'}
		
			equipmentConf = config.getConfig('equipment')
			equipmentInfo = equipmentConf[equipment['equipmentid']]
		
			sellGold = equipmentInfo['price']		
			usr.gold = usr.gold + sellGold		
			inv.delEquipment(equipid)
			sellequipment.append(equipid)
		inv.save()
		usr.save()
		
		return {'gold':usr.gold, 'delete_equipment_array':sellequipment}		
		
	@staticmethod
	def takeoff(inv, card):
		"""
		脱下
		"""
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
		"""
		交换
		"""
		toSlot = None
		if toCard.has_key('slot'):
			toSlot = toCard['slot']			
		toCard['slot'] = fromCard['slot']
		del fromCard['slot']
		if toSlot:
			fromCard['slot'] = toSlot
		return []					

	@staticmethod
	def degradation(usr, equipmentid):
		"""
		降级
		"""
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
		goldGain = int(strengthenPriceConf[str(equipmentQuality)][equipment['strengthLevel']] * gameConf['equipment_degradation_price_rate'])
		
		equipment['strengthLevel'] = equipment['strengthLevel'] - 1
		if equipment['strengthLevel'] <= 0:
			del equipment['strengthLevel']
		
		usr.gold = usr.gold + goldGain
		
		inv.save()
		usr.save()
		
		return {'gold':usr.gold, 'equipment_degradation':equipment}
		
	@staticmethod
	def assembly(usr, equipmentid):
		"""
		装配
		"""
		inv = usr.getInventory()
		
		if not inv.equipment_chip.has_key(equipmentid):
			return {'msg':'equipment_chip_not_enough'}
		
		equipmentConf = config.getConfig('equipment')
		
		if not equipmentConf.has_key(equipmentid):
			return {'msg':'equipment_chip_not_exist'}
		
		equipmentInfo = equipmentConf[equipmentid]
		
		if inv.equipment_chip[equipmentid] < equipmentInfo['chip']:
			return {'msg':'equipment_chip_not_enough'}
				
		inv.equipment_chip[equipmentid] = inv.equipment_chip[equipmentid] - equipmentInfo['chip']
		if inv.equipment_chip[equipmentid] == 0:
			del inv.equipment_chip[equipmentid]
		equipment = inv.addEquipment(equipmentid)
		inv.save()
		
		if inv.equipment_chip.has_key(equipmentid):
			return {'equipment_chip':{equipmentid: inv.equipment_chip[equipmentid]}, 'add_equipment':equipment}
		else:
			return {'equipment_chip':{equipmentid: 0}, 'add_equipment':equipmentid}
			