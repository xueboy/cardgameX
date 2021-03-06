﻿#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config

class practice:
	
	@staticmethod
	def make():
		"""
		制做
		"""
		return {'critical_level':0, 'critical_exp':0, 'tenacity_level':0, 'tenacity_exp':0, 'block_level':0, 'block_exp':0, 'wreck_level':0, 'wreck_exp':0}
	
	@staticmethod
	def getClientData(usr):
		"""
		得到 client data
		"""
		return usr.practice
	
	@staticmethod
	def card_levelup(usr, tp, cardid):
		"""
		用卡牌升级
		"""
				
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
		
		data = practice.practice_type(usr, tp)
		data['delete_dic'] = {}
		for cid in cardid:
			data['delete_dic'][cid] = 1		
		return data
		
				
	@staticmethod
	def card_chip_levelup(usr, tp, chipDic):
		"""
		用卡牌碎片升级
		"""
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
		
		data = practice.practice_type(usr, tp)
		data['delete_dic'] = chipDic
		return data
		
		
	@staticmethod
	def skill_levelup(usr, tp, skillid):
		"""
		用技能升级
		"""
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
		
		data = practice.practice_type(usr, tp)
		data['delete_dic'] = {}
		for sid in skillid:
			data['delete_dic'][sid] = 1
			
		
		return data
		
		
	@staticmethod
	def skill_chip_levelup(usr, tp, chipDic):
		"""
		用技能碎片升级
		"""		
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
		data = practice.practice_type(usr, tp)
		data['delete_dic'] = chipDic
		return data
		
						
	@staticmethod
	def levelup(usr, tp, point, practiceLevelConf):		
		"""
		升级
		"""
		if tp == 'critical':
			usr.practice['critical_exp'] = usr.practice['critical_exp'] + point
			level = usr.practice['critical_level']
			if level >= len(practiceLevelConf['critical_level']):
				return {'msg':'practice_level_max'}
			while usr.practice['critical_exp'] >= (practiceLevelConf['critical_level'][level + 1] - practiceLevelConf['critical_level'][level]):
				usr.practice['critical_exp'] = usr.practice['critical_exp'] - (practiceLevelConf['critical_level'][level + 1] - practiceLevelConf['critical_level'][level])
				usr.practice['critical_level'] = usr.practice['critical_level'] + 1
		elif tp == 'tenacity':
			usr.practice['tenacity_exp'] = usr.practice['tenacity_exp'] + point
			level = usr.practice['tenacity_level']
			if level >= len(practiceLevelConf['tenacity_level']):
				return {'msg':'practice_level_max'}
			while usr.practice['tenacity_exp'] >= (practiceLevelConf['tenacity_level'][level + 1] - practiceLevelConf['tenacity_level'][level]):
				usr.practice['tenacity_exp'] = usr.practice['tenacity_exp'] - (practiceLevelConf['tenacity_level'][level + 1] - practiceLevelConf['tenacity_level'][level])
				usr.practice['tenacity_level'] = usr.practice['tenacity_level'] + 1
		elif tp == 'block':
			usr.practice['block_exp'] = usr.practice['block_exp'] + point
			level = usr.practice['block_level']
			if level >= len(practiceLevelConf['block_level']):
				return {'msg':'practice_level_max'}
			while usr.practice['block_exp'] >= (practiceLevelConf['block_level'][level + 1] - practiceLevelConf['block_level'][level]):
				usr.practice['block_exp'] = usr.practice['block_exp'] - (practiceLevelConf['block_level'][level + 1] - practiceLevelConf['block_level'][level])
				usr.practice['block_level'] = usr.practice['block_level'] + 1	
		elif tp == 'wreck':
			usr.practice['wreck_exp'] = usr.practice['wreck_exp'] + point
			level = usr.practice['wreck_level']
			if level >= len(practiceLevelConf['wreck_level']):
				return {'msg':'practice_level_max'}
			while usr.practice['wreck_exp'] >= (practiceLevelConf['wreck_level'][level + 1] - practiceLevelConf['wreck_level'][level]):
				usr.practice['wreck_exp'] = usr.practice['wreck_exp'] - (practiceLevelConf['wreck_level'][level + 1] - practiceLevelConf['wreck_level'][level])
				usr.practice['wreck_level'] = usr.practice['wreck_level'] + 1	
		else:
			return {'msg':'bad_parameter'}
		return {}
		
		
	@staticmethod
	def practice_type(usr, tp):
		"""
		训练类型
		"""
		if tp == 'critical':
			return {'critical_exp':usr.practice['critical_exp'], 'critical_level': usr.practice['critical_level']}
		elif tp == 'tenacity':
			return {'tenacity_exp':usr.practice['tenacity_exp'], 'tenacity_level': usr.practice['tenacity_level']}
		elif tp == 'block':
			return {'block_exp': usr.practice['block_exp'], 'block_level': usr.practice['block_level']}
		elif tp == 'wreck':
			return {'wreck_exp': usr.practice['wreck_exp'], 'wreck_level': usr.practice['wreck_level']}
		return {}