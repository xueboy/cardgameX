#coding:utf-8
#!/usr/bin/env python


class practice:
	
	@staticmethod
	def make():
		return {'critical_level':0, 'critical_exp':0, 'tenacity_level':0, 'tenacity_exp':0, 'block_level':0, 'block_exp':0, 'wreck_level':0, 'wreck_exp':0}
	
	@staticmethod
	def card_levelup(usr, tp, cardid):
		
		if not cardid:
			return {}
		
		petConf = config.getConfig('pet')
		practiceLevelConf = config.getConfig('practice_level')
		inv = usr.getInventory()
		
		point = 0
		
		for cid in cardid:
			card = inv.getCard(cid)
			quality = petConf[card['cardid']]['quality']
			point = practiceLevelConf['card_point'][quality - 1] + point
			inv.delCard(card['id'])
			
		practice.levelup(usr, pt, point)
		
		inv.save()
		usr.save()
		
		return usr.prictice
		
		
	@staticmethod
	def levelup(usr, pt, point):
		if tp == 'critical':
			usr.prictice['critical_exp'] = usr.prictice['critical_exp'] + point
			level = usr.prictice['critical_level']
			if level >= practiceLevelConf['critical_level']:
				return {'msg':'practice_level_max'}
			while usr.prictice['critical_exp'] > practiceLevelConf['critical_property'][level + 1] - practiceLevelConf['critical_property'][level + 1]:
				usr.prictice['critical_exp'] = usr.practice['critical_exp'] - (practiceLevelConf['critical_property'][level + 1] - practiceLevelConf['critical_property'][level + 1])
				usr.prictice['critical_level'] = usr.prictice['critical_level'] + 1
		elif tp == 'tenacity':
			usr.prictice['tenacity_exp'] = usr.prictice['tenacity_exp'] + point
			level = usr.prictice['tenacity_level']
			if level >= practiceLevelConf['tenacity_level']:
				return {'msg':'practice_level_max'}
			while usr.prictice['tenacity_exp'] > practiceLevelConf['tenacity_property'][level + 1] - practiceLevelConf['tenacity_property'][level + 1]:
				usr.prictice['tenacity_exp'] = usr.practice['tenacity_exp'] - (practiceLevelConf['tenacity_property'][level + 1] - practiceLevelConf['tenacity_property'][level + 1])
				usr.prictice['tenacity_level'] = usr.prictice['tenacity_level'] + 1
		elif tp == 'block':
			usr.prictice['block_exp'] = usr.prictice['block_exp'] + point
			level = usr.prictice['block_level']
			if level >= practiceLevelConf['block_level']:
				return {'msg':'practice_level_max'}
			while usr.prictice['block_exp'] > practiceLevelConf['block_property'][level + 1] - practiceLevelConf['block_property'][level + 1]:
				usr.prictice['block_exp'] = usr.practice['block_exp'] - (practiceLevelConf['block_property'][level + 1] - practiceLevelConf['block_property'][level + 1])
				usr.prictice['block_level'] = usr.prictice['block_level'] + 1	
		elif tp == 'wreck':
			usr.prictice['wreck_exp'] = usr.prictice['wreck_exp'] + point
			level = usr.prictice['wreck_level']
			if level >= practiceLevelConf['wreck_level']:
				return {'msg':'practice_level_max'}
			while usr.prictice['wreck_exp'] > practiceLevelConf['wreck_property'][level + 1] - practiceLevelConf['wreck_property'][level + 1]:
				usr.prictice['wreck_exp'] = usr.practice['wreck_exp'] - (practiceLevelConf['wreck_property'][level + 1] - practiceLevelConf['wreck_property'][level + 1])
				usr.prictice['wreck_level'] = usr.prictice['wreck_level'] + 1	
		else:
			return {'msg':'bad_parameter'}
		return {}
		
	@staticmethod
	def card_chip_levelup(usr, tp, chipDic):
		
		if not chipDic:
			return {}
		
		petConf = config.getConfig('pet')
		practiceLevelConf = config.getConfig('practice_level')
		inv = usr.getInventory()
		
		point = 0
		
		for chipid in chipDic:
			if not inv.card_chip.has_key(chipid):
				return {'msg':'chip_not_exist'}
			inv.card_chip[chipid] = inv.card_chip[chipid] - chipDic[chipid]
			if inv.card_chip[chipid] < 0:
				return {'msg': 'chip_not_enough'}
			if inv.card_chip[chipid] == 0:
				del inv.card_chip[chipid]
			quality = petConf[chipid]['quality']
			point = int(practiceLevelConf['card_point'][quality - 1] / petConf[chipid]['chip']) * chipDic[chipid] + point
			
			
		
		
	@staticmethod
	def skill_levelup(skillid):
		pass
		
	@staticmethod
	def skill_chip_levelup(skill_chip):
		pass