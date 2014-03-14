#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config
from game.routine.luck import luck
from game.routine.skill import skill

class pvp:
	
	@staticmethod
	def almanacPvpProperty(usr):
		"""
		图签pvp数据
		"""
		
		al = usr.getAlmanac()
		
		combinaionConf = config.getConfig('almanac_combination')
		
		ppData = {}
		ppData['attack'] = 0
		ppData['hp'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0
		ppData['pa'] = 0		
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0		
		ppData['pe'] = 0
		ppData['speed'] = 0
						
#		for cb in al.combine:
#			if cb['typestr'] == 'strenghth':
#				ppData['strenghth'] = ppData['strenghth'] + cb['val']
#			elif cb['typestr'] == 'intelligence':
#				ppData['intelligence'] = ppData['intelligence'] + cb['val']
#			elif cb['typestr'] == 'artifice':
#				ppData['artifice'] = ppData['artifice'] + cb['val']
#			elif cb['typestr'] == 'attack':
#				ppData['attack'] = ppData['attack'] + cb['val']
#			elif cb['typestr'] == 'hp':
#				ppData['hp'] = ppData['hp'] + cb['val']
#			elif cb['typestr'] == 'critical':
#				ppData['critical'] = ppData['critical'] + cb['val']
#			elif cb['typestr'] == 'tenacity':
#				ppData['tenacity'] = ppData['tenacity'] + cb['val']
#			elif cb['typestr'] == 'dodge':
#				ppData['dodge'] = ppData['dodge'] + cb['val']
#			elif cb['typestr'] == 'hit':
#				ppData['hit'] = ppData['hit'] + cb['val']
#			elif cb['typestr'] == 'block':
#				ppData['block'] = ppData['block'] + cb['val']
#			elif cb['typestr'] == 'wreck':
#				ppData['wreck'] = ppData['wreck'] + cb['val']
#			elif cb['typestr'] == 'pt':
#				ppData['pt'] = ppData['pt'] + cb['val']			
#			elif cb['typestr'] == 'pd':
#				ppData['pd'] = ppData['pd'] + cb['val']
#			elif cb['typestr'] == 'md':
#				ppData['md'] = ppData['md'] + cb['val']
#			elif cb['typestr'] == 'criticallv':
#				ppData['criticallv'] = ppData['criticallv'] + cb['val']
#			elif cb['typestr'] == 'tenacitylv':
#				ppData['tenacity'] = ppData['tenacity'] + cb['val']
#			elif cb['typestr'] == 'dodgelv':
#				ppData['dodgelv'] = ppData['dodgelv'] + cb['val']
#			elif cb['typestr'] == 'hitlv':
#				ppData['hitlv'] = ppData['hitlv'] + cb['val']
#			elif cb['typestr'] == 'blocklv':
#				ppData['blocklv'] = ppData['blocklv'] + cb['val']
#			elif cb['typestr'] == 'wrecklv':
#				ppData['wrecklv'] = ppData['wrecklv'] + cb['val']
#			elif cb['typestr'] == 'speed':
#				ppData['speed'] = ppData['speed'] + cb['val']
				
		return ppData
		
	@staticmethod
	def medalPvpProperty(usr):
		"""
		勋章pvp数据
		"""
		inv = usr.getInventory()
		
		medalConfig = config.getConfig('medal')
		medalLevelConfig = config.getConfig('medal_level')
		
		ppData = {}
		ppData['attack'] = 0
		ppData['hp'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0
		ppData['pa'] = 0		
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0		
		ppData['pe'] = 0
		ppData['speed'] = 0
			
		for medalid in inv.medal:
			medalLevelInfo = medalLevelConfig[medalid][inv.medal[medalid]['level']]			
			if medalLevelInfo['typestr'] == 'strenghth':
				ppData['strenghth'] = ppData['strenghth'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'intelligence':
				ppData['intelligence'] = ppData['intelligence'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'artifice':
				ppData['artifice'] = ppData['artifice'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'attack':
				ppData['attack'] = ppData['attack'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'hp':
				ppData['hp'] = ppData['hp'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'critical':
				ppData['critical'] = ppData['critical'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'tenacity':
				ppData['tenacity'] = ppData['tenacity'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'dodge':
				ppData['dodge'] = ppData['dodge'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'hit':
				ppData['hit'] = ppData['hit'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'block':
				ppData['block'] = ppData['block'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'wreck':
				ppData['wreck'] = ppData['wreck'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'pt':
				ppData['pt'] = ppData['pt'] + medalLevelInfo['val']			
			elif medalLevelInfo['typestr'] == 'pd':
				ppData['pd'] = ppData['pd'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'md':
				ppData['md'] = ppData['md'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'criticallv':
				ppData['criticallv'] = ppData['criticallv'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'tenacitylv':
				ppData['tenacity'] = ppData['tenacity'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'dodgelv':
				ppData['dodgelv'] = ppData['dodgelv'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'hitlv':
				ppData['hitlv'] = ppData['hitlv'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'blocklv':
				ppData['blocklv'] = ppData['blocklv'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'wrecklv':
				ppData['wrecklv'] = ppData['wrecklv'] + medalLevelInfo['val']
			elif medalLevelInfo['typestr'] == 'speed':
				ppData['speed'] = ppData['speed'] + medalLevelInfo['val']		
		
		return ppData
		
	@staticmethod
	def practicePvpProperty(usr):
		"""
		训练pvp数据
		"""
		ppData = {}
		ppData['attack'] = 0
		ppData['hp'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0
		ppData['pa'] = 0		
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0		
		ppData['pe'] = 0		
		ppData['speed'] = 0
		
		practicePropertyConf = config.getConfig('practice_property')
		
		if usr.practice['critical_level'] > 0:
			ppData['critical'] = practicePropertyConf['critical_property'][usr.practice['critical_level']]
		if usr.practice['tenacity_level'] > 0:
			ppData['tenacity'] = practicePropertyConf['tenacity_property'][usr.practice['tenacity_level']]
		if usr.practice['block_level'] > 0:
			ppData['block'] = practicePropertyConf['block_property'][usr.practice['block_level']]
		if usr.practice['wreck_level'] > 0:
			ppData['wreck'] = practicePropertyConf['wreck_property'][usr.practice['wreck_level']]
			
		return ppData
		
	@staticmethod
	def luckPvpProperty(usr, card):
		"""
		缘份pvp数据
		"""
		ppData = {}
		ppData['attack'] = 0
		ppData['hp'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0
		ppData['pa'] = 0		
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0		
		ppData['pe'] = 0		
		ppData['speed'] = 0
		
		petConf = config.getConfig('pet')
		luckConf = config.getConfig('luck')
	
		for luckdata in petConf[card['cardid']]['luck']:
			luckid = luck.check(usr, card, petConf)		
			
			luckInfo = luckConf[luckid]
			
		
			if luckInfo['typestr'] == 'strenghth':
				ppData['strenghth'] = ppData['strenghth'] + luckInfo['value']
			elif luckInfo['typestr'] == 'intelligence':
				ppData['intelligence'] = ppData['intelligence'] + luckInfo['value']
			elif luckInfo['typestr'] == 'artifice':
				ppData['artifice'] = ppData['artifice'] + luckInfo['value']
			elif luckInfo['typestr'] == 'attack':
				ppData['attack'] = ppData['attack'] + luckInfo['value']
			elif luckInfo['typestr'] == 'hp':
				ppData['hp'] = ppData['hp'] + luckInfo['value']
			elif luckInfo['typestr'] == 'critical':
				ppData['critical'] = ppData['critical'] + luckInfo['value']
			elif luckInfo['typestr'] == 'tenacity':
				ppData['tenacity'] = ppData['tenacity'] + luckInfo['value']
			elif luckInfo['typestr'] == 'dodge':
				ppData['dodge'] = ppData['dodge'] + luckInfo['value']
			elif luckInfo['typestr'] == 'hit':
				ppData['hit'] = ppData['hit'] + luckInfo['value']
			elif luckInfo['typestr'] == 'block':
				ppData['block'] = ppData['block'] + luckInfo['value']
			elif luckInfo['typestr'] == 'wreck':
				ppData['wreck'] = ppData['wreck'] + luckInfo['value']
			elif luckInfo['typestr'] == 'pt':
				ppData['pt'] = ppData['pt'] + luckInfo['value']			
			elif luckInfo['typestr'] == 'pd':
				ppData['pd'] = ppData['pd'] + luckInfo['value']
			elif luckInfo['typestr'] == 'md':
				ppData['md'] = ppData['md'] + luckInfo['value']
			elif luckInfo['typestr'] == 'criticallv':
				ppData['criticallv'] = ppData['criticallv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'tenacitylv':
				ppData['tenacity'] = ppData['tenacity'] + luckInfo['value']
			elif luckInfo['typestr'] == 'dodgelv':
				ppData['dodgelv'] = ppData['dodgelv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'hitlv':
				ppData['hitlv'] = ppData['hitlv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'blocklv':
				ppData['blocklv'] = ppData['blocklv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'wrecklv':
				ppData['wrecklv'] = ppData['wrecklv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'speed':
				ppData['speed'] = ppData['speed'] + luckInfo['value']
				
		return ppData
		
		
	@staticmethod
	def mergePvpProperty(p1, p2):
		"""
		合并pvp数据
		"""
		ppData = p1.copy()
		ppData['attack'] = p1['attack'] + p2['attack']
		ppData['hp'] = p1['hp'] + p2['hp']
		ppData['pd'] = p1['pd'] + p2['pd']
		ppData['md'] = p1['md'] + p2['md']
		ppData['pt'] = p1['pt'] + p2['pt']		
		ppData['pr'] = p1['pr'] + p2['pr']
		ppData['mr'] = p1['mr'] + p2['mr']
		ppData['critical'] = p1['critical'] + p2['critical']
		ppData['tenacity'] = p1['tenacity'] + p2['tenacity']
		ppData['block'] = p1['block'] + p2['block']
		ppData['wreck'] = p1['wreck'] + p2['wreck']
		ppData['hit'] = p1['hit'] + p2['hit']
		ppData['dodge'] = p1['dodge'] + p2['dodge']
		ppData['pa'] = p1['pa'] + p2['pa']		
		ppData['strength'] = p1['strength'] + p2['strength']
		ppData['intelligence'] = p1['intelligence'] + p2['intelligence']
		ppData['artifice'] = p1['artifice'] + p2['artifice']
		ppData['pi'] = p1['pi'] + p2['pi']		
		ppData['pe'] = p1['pe'] + p2['pe']
		ppData['speed'] = p1['speed'] + p2['speed']
		ppData['init_star'] = p1['init_star']
		ppData['level'] = p1['level']
		ppData['sk_slot'] = p1['sk_slot']		
		return ppData
		
		
	@staticmethod
	def pvpPetProperty(usr, card, petConf):
		"""
		宠物pvp数据
		"""
		
		petInfo = petConf[card['cardid']]
		
		star = card['init_star'] + int(card['level'] * 0.4)
		
		inv = usr.getInventory()
		ppData = {}
		ppData['attack'] = petInfo['attack'] + int(petInfo['attackgrowth'] * (card['level'] + star * 5)  * 0.5)
		ppData['hp'] = petInfo['hp'] + int(petInfo['hpgrowth'] * (card['level'] + star * 5) * 0.5)
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = petInfo['pr'] + star * petInfo['prgrowth']
		ppData['mr'] = petInfo['mr'] + star * petInfo['mrgrowth']
		ppData['critical'] = petInfo['critical']
		ppData['tenacity'] = petInfo['tenacity']
		ppData['block'] = petInfo['block']
		ppData['wreck'] = petInfo['wreck']
		ppData['hit'] = petInfo['hit']
		ppData['dodge'] = petInfo['dodge']		
		ppData['strength'] = petInfo['strength']
		ppData['intelligence'] = petInfo['intelligence']
		ppData['artifice'] = petInfo['artifice']
		ppData['pi'] = 0		
		ppData['pa'] = petInfo['pa'] + petInfo['pagrowth'] * star		
		ppData['id'] = card['id']
		ppData['cardid'] = card['cardid']
		ppData['pe'] = 0
		ppData['init_star'] = card['init_star']
		ppData['level'] = card['level']
		ppData['sk_slot'] = pvp.pvpGetSkSlots(usr)
		ppData['speed'] = 0
		return ppData
		
	@staticmethod
	def pvpGetSkSlots(usr):
		"""
		得到技能栏位
		"""
		inv = usr.getInventory()		
		sk_slot = {}		
		for (i, t) in enumerate(inv.team):
			if t:
				tc = inv.getCard(t)
				if tc.has_key('sk_slot'):
					sk_slot['t'+ str(i)] = tc['sk_slot']
				else:
					sk_slot['t' + str(i)] = skill.make_sk_slot()
			else:
				sk_slot['t' + str(i)] = skill.make_sk_slot()
			for sk in sk_slot['t' + str(i)]:
				if sk:
					del sk['id']
					del sk['exp']
		return sk_slot
		
	@staticmethod
	def pvpEquipmentProperty(equipment, equipmentConf):
		"""
		pvp装备属性
		"""
				
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
		ppData['pe'] = 0
		ppData['speed'] = 0
		return ppData
		
	@staticmethod
	def pvpStoneProperty(st, stoneConf):
		"""
		pvp宝石属性
		"""
		ppData['hp'] = 0
		ppData['pa'] = 0
		ppData['ma'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0
		ppData['mt'] = 0					
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
		ppData['speed'] = 0		

		quality = stoneConf[st['stoneid']]['quality']
		stoneConf = config.getConfig('stone')
		stoneInfo = stoneConf[st[stoneid]]
				
		if st['typestr'] == 'strenghth':
			ppData['strenghth'] = stoneInfo[st['level'] - 1]['value']
		elif st['typestr'] == 'intelligence':
			ppData['intelligence'] = stoneInfo[st['level'] - 1]['value']
		elif st['typestr'] == 'artifice':
			ppData['artifice'] = stoneInfo[st['level'] - 1]['value']		
		elif st['typestr'] == 'pt':
			ppData['pt'] = stoneInfo[st['level'] - 1]['value']		
		elif st['typestr'] == 'pd':
			ppData['pd'] = stoneInfo[st['level'] - 1]['value']
		elif st['typestr'] == 'md':
			ppData['md'] = stoneInfo[st['level'] - 1]['value']		
		
		return ppData

		
		