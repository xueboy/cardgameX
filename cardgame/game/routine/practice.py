#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config

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
			if not card:
				return {'msg':'card_not_exist'}
			quality = petConf[card['cardid']]['quality']
			point = practiceLevelConf['card_point'][quality - 1] + point
			inv.delCard(card['id'])
			
		res = practice.levelup(usr, tp, point, practiceLevelConf)
		if res.has_key('msg'):
			return res
		
		inv.save()
		usr.save()
		
		data = usr.practice.copy()
		data['delete_card_array'] = cardid
		
		return data
		
				
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
		
		res = practice.levelup(usr, tp, point, practiceLevelConf)
		if res.has_key('msg'):
			return res	
		inv.save()
		usr.save()
		
		data = usr.practice.copy()
		data['delete_card_chip_dic'] = chipDic
		return data
		
		
	@staticmethod
	def skill_levelup(usr, tp, skillid):
			
		if not skillid:
			return {}
		
		skillConf = config.getConfig('skill')
		practiceLevelConf = config.getConfig('practice_level')
		inv = usr.getInventory()
		
		point = 0
		
		for sid in skillid:
			sk = inv.getSkill(sid)
			if not sk:
				return {'msg': 'skill_not_exist'}
			quality = skillConf[sk['skillid']]['quality']
			point = practiceLevelConf['skill_point'][quality - 1] + point
			inv.delSkill(sk['id'])
			
		res = practice.levelup(usr, tp, point, practiceLevelConf)
		if res.has_key('msg'):
			return res
		
		inv.save()
		usr.save()
		
		data = usr.practice.copy()
		data['delete_skill_array'] = skillid
		
		return data
		
		
	@staticmethod
	def skill_chip_levelup(usr, tp, chipDic):
				
		if not chipDic:
			return {}
		
		skillConf = config.getConfig('skill')
		practiceLevelConf = config.getConfig('practice_level')
		inv = usr.getInventory()
		
		point = 0
		
		for chipid in chipDic:
			if not inv.skill_chip.has_key(chipid):
				return {'msg':'chip_not_exist'}
			inv.skill_chip[chipid] = inv.skill_chip[chipid] - chipDic[chipid]
			if inv.skill_chip[chipid] < 0:
				return {'msg': 'chip_not_enough'}
			if inv.skill_chip[chipid] == 0:
				del inv.skill_chip[chipid]
			quality = skillConf[chipid]['quality']
			point = int(practiceLevelConf['skill_point'][quality - 1] / skillConf[chipid]['chip']) * chipDic[chipid] + point
		
		res = practice.levelup(usr, tp, point, practiceLevelConf)
		if res.has_key('msg'):
			return res	
		inv.save()
		usr.save()
		data = usr.practice.copy()
		data['delete_skill_chip_dic'] = chipDic
		return data
		
						
	@staticmethod
	def levelup(usr, tp, point, practiceLevelConf):
		print usr.practice
		if tp == 'critical':
			usr.practice['critical_exp'] = usr.practice['critical_exp'] + point
			level = usr.practice['critical_level']
			if level >= practiceLevelConf['critical_level']:
				return {'msg':'practice_level_max'}
			while usr.practice['critical_exp'] >= (practiceLevelConf['critical_level'][level + 1] - practiceLevelConf['critical_level'][level]):
				usr.practice['critical_exp'] = usr.practice['critical_exp'] - (practiceLevelConf['critical_level'][level + 1] - practiceLevelConf['critical_level'][level])
				usr.practice['critical_level'] = usr.practice['critical_level'] + 1
		elif tp == 'tenacity':
			usr.practice['tenacity_exp'] = usr.practice['tenacity_exp'] + point
			level = usr.practice['tenacity_level']
			if level >= practiceLevelConf['tenacity_level']:
				return {'msg':'practice_level_max'}
			while usr.practice['tenacity_exp'] >= (practiceLevelConf['tenacity_level'][level + 1] - practiceLevelConf['tenacity_level'][level]):
				usr.practice['tenacity_exp'] = usr.practice['tenacity_exp'] - (practiceLevelConf['tenacity_level'][level + 1] - practiceLevelConf['tenacity_level'][level])
				usr.practice['tenacity_level'] = usr.practice['tenacity_level'] + 1
		elif tp == 'block':
			usr.practice['block_exp'] = usr.practice['block_exp'] + point
			level = usr.practice['block_level']
			if level >= practiceLevelConf['block_level']:
				return {'msg':'practice_level_max'}
			while usr.practice['block_exp'] >= (practiceLevelConf['block_property'][level + 1] - practiceLevelConf['block_level'][level]):
				usr.practice['block_exp'] = usr.practice['block_exp'] - (practiceLevelConf['block_level'][level + 1] - practiceLevelConf['block_level'][level])
				usr.practice['block_level'] = usr.practice['block_level'] + 1	
		elif tp == 'wreck':
			usr.prictice['wreck_exp'] = usr.practice['wreck_exp'] + point
			level = usr.practice['wreck_level']
			if level >= practiceLevelConf['wreck_level']:
				return {'msg':'practice_level_max'}
			while usr.prictice['wreck_exp'] >= (practiceLevelConf['wreck_level'][level + 1] - practiceLevelConf['wreck_level'][level]):
				usr.practice['wreck_exp'] = usr.practice['wreck_exp'] - (practiceLevelConf['wreck_level'][level + 1] - practiceLevelConf['wreck_level'][level])
				usr.practice['wreck_level'] = usr.practice['wreck_level'] + 1	
		else:
			return {'msg':'bad_parameter'}
		return {}
		
		
		