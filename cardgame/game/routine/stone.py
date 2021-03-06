﻿#coding:utf-8
#!/usr/bin/env python

import random

from gclib.utility import drop, randint
from game.utility.config import config

class stone:
	
	@staticmethod
	def visit(usr, level):
		"""
		访问
		"""
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')
		
		if level > len(usr.stv):
			return {'msg':'svt_too_hight'}
		
		if not usr.stv[level - 1]:
			return {'msg':'svt_not_available'}			
	
		result = []	
		msg = stone.do_visit(usr, level, result, gameConf,stoneProbabilityConf)		
		usr.save()
		inv.save()
		
		if msg:
			return msg		
		data = result[0]
		data['gold'] = usr.gold	
		data['gem'] = usr.gem
		return data
		
	@staticmethod
	def visit_gem(usr, level):
		"""
		钻石访问
		"""
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')
				
		if level > len(usr.stv):
			return {'msg':'svt_too_hight'}
				
		gemCost = stoneProbabilityConf['visitGem'][level - 1]		
		
		if not gemCost:
			return {'msg':'stone_visit_level_gem_not_allow'}
		if gemCost > usr.gem:
			return {'msg':'gem_not_enough'}
				
		probs = stoneProbabilityConf['visit'][level - 1]['gem']
			
		seed = randint()		
		cndStone = []
						
		for prob in probs:
			p = prob['probability'] 
			if p > seed:
				cndStone = prob['stone']
				break
			else:
				seed = seed - p				
				
		stoneid = random.sample(cndStone, 1)[0]
		stone = inv.addStone(stoneid)	
				
		usr.stv[level - 1] = 0
		if level < len(usr.stv):		
			usr.stv[level] = 1		
				
		usr.gem = usr.gem - gemCost
				
		usr.save()
		inv.save()
		
		return {'stv':usr.stv, 'add_stone':stone, 'gem':usr.gem, 'gold':usr.gold}
			
	@staticmethod
	def visit_clickonce(usr, count):	
		"""
		一键访问
		"""
		inv = usr.getInventory()
		gameConf = config.getConfig('game')
		stoneProbabilityConf = config.getConfig('stone_probability')		
		level = stone.max_available_stv(usr)
		
		result = []		
		for i in range(count):
			msg = stone.do_visit(usr, level, result, gameConf, stoneProbabilityConf)
			if msg:
				break
			level = stone.max_available_stv(usr)		
		usr.save()
		inv.save()
		if result:
			return {'result':result, 'gold':usr.gold}
		return msg			
		
	@staticmethod
	def max_available_stv(usr):
		"""
		最大访问等级
		"""
		if usr.stv[4]:
			return 5
		if usr.stv[3]:
			return 4
		if usr.stv[2]:
			return 3
		if usr.stv[1]:
			return 2
		if usr.stv[0]:
			return 1
		
	@staticmethod
	def do_visit(usr, level, result, gameConf,stoneProbabilityConf):
		"""
		访问
		"""
		inv = usr.getInventory()			
		
		goldCost = stoneProbabilityConf['visitGold'][level - 1]		
		
		if goldCost > usr.gold:
			return {'msg':'gold_not_enough'}
		
		probs = stoneProbabilityConf['visit'][level - 1]['gold']
			
		seed = randint()		
		cndStone = []
						
		for prob in probs:
			p = prob['probability'] 
			if p > seed:
				cndStone = prob['stone']
				break
			else:
				seed = seed - p				
				
		stoneid = random.sample(cndStone, 1)[0]
		stone = inv.addStone(stoneid)	
				
		if drop(stoneProbabilityConf['visitProb'][level - 1]):
			usr.stv[level] = 1
		usr.stv[level - 1] = 0	
		usr.stv[0] = 1				
		usr.gold = usr.gold - goldCost		
		result.append({'stv':usr.stv[:], 'add_stone':stone})
		return {}
		
			
	@staticmethod
	def levelup(usr, teamPosition, dest_stoneid, source_stoneid):
		"""
		宝石升级
		"""	
		if not source_stoneid:
			return {'msg':'stone_not_specified'}
				
		stoneConf = config.getConfig('stone')	
				
		inv = usr.getInventory()
		if teamPosition < 0:	
			dest_stone = inv.getStone(dest_stoneid)	
		else:
			ownerid = inv.team[teamPosition]
			if not ownerid:
				return {'msg':'team_position_not_have_member'}
			owner = inv.getCard(ownerid)
			if not owner:
				return {'msg': 'card_not_exist'}
			for i, s in enumerate(owner['st_slot']):
				if s and s['id'] == dest_stoneid:
					dest_stone = s					
					break			
		if not dest_stone:
			return {'msg':'stone_not_exist'}
		exp = 0
				
		for srcid in source_stoneid:			
			ss = inv.getStone(srcid)			
			if not ss:
				return {'msg':'stone_not_exist'}			
			exp = exp + stone.get_exp(ss, stoneConf[ss['stoneid']])			
			inv.delStone(srcid)				
		
		stone.add_exp(dest_stone, exp, stoneConf[dest_stone['stoneid']])
		inv.save()		
		return {'stone':dest_stone, 'stone_delete_array':source_stoneid}
		
	@staticmethod
	def add_exp(st, exp, stoneInfo):	
		"""
		添加经验
		"""
		expdeff = stoneInfo[st['level']]['exp'] - stoneInfo[st['level'] - 1]['exp']
		exp = exp + st['exp']
		st['exp'] = 0
		while expdeff < exp and len(stoneInfo) < st['level']:
			st['level'] = st['level'] + 1
			exp = exp - expdeff
			expdeff = stoneInfo[st['level']]['exp'] - stoneInfo[st['level'] - 1]['exp']
			
		st['exp'] = exp
			
	@staticmethod
	def get_exp(st, stoneInfo):
		"""
		得到经验
		"""
		exp = st['exp']
		exp = exp + stoneInfo[st['level'] - 1]['exp']
		exp = exp + stoneInfo[st['level'] - 1]['gravel']
		return exp
		
	@staticmethod
	def make_stv():
		"""
		制做stv
		"""
		return [1, 0, 0, 0, 0]

	@staticmethod
	def install(usr, teamPosition, ownerTeamPosition, slotpos, stoneid):
		"""
		安装宝石
		"""
		inv = usr.getInventory()
		
		if not inv.team[teamPosition]:
			return {'msg':'team_position_not_have_member'}				
		card = inv.getCard(inv.team[teamPosition])
		if not card:
			return {'msg': 'card_not_exist'}		
		gameConf = config.getConfig('game')		
		if gameConf['stone_slot_level'][slotpos] > usr.level:
			return {'msg': 'level_required'}
		
		if not card.has_key('st_slot'):
			card['st_slot'] = stone.make_st_solt()
	
		stoneConf = config.getConfig('stone')		
		st = None
		owner = None
		if ownerTeamPosition < 0:		
			st = inv.withdrawStone(stoneid)
		else:
			ownerid = inv.team[ownerTeamPosition]
			if not ownerid:
				return {'msg':'team_position_not_have_member'}
			owner = inv.getCard(ownerid)
			if not owner:
				return {'msg': 'card_not_exist'}
			for i, s in enumerate(owner['st_slot']):
				if s and s['id'] == stoneid:
					st = s
					owner['st_slot'][i] = {}
					break			
		
		if not st:
			return {'msg':'stone_not_exist'}
				
		oldst = card['st_slot'][slotpos]
		if (not oldst) and (not stoneid):
			return {'msg':'stone_not_exist'}
			
		sttype = stoneConf[st['stoneid']][st['level'] - 1]['type']
		for st1 in card['st_slot']:
			if st1 and stoneConf[st1['stoneid']][st['level'] - 1]['type'] == sttype:
				return {'msg':'stone_same_type_installed'}				
		
		card['st_slot'][slotpos] = st		
		if oldst:
			inv.depositStone(oldst)		
		inv.save()			
		data = {}		
		data['st_slot'] = inv.getStSlots()
		if oldst:
			data['add_stone'] = oldst			
		if st:
			data['delete_stone'] = st
			
		return data		
		
	@staticmethod
	def make_st_solt():
		"""
		制做宝石槽位
		"""
		return [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
		
	@staticmethod
	def takeoff(inv, card):
		"""
		脱下宝石
		"""
		dst = []
		if card and card.has_key('st_slot'):
			for st in card['st_slot']:
				if st:
					inv.depositStone(st)
					dst.append(st)
			del card['st_slot']
		return dst

	@staticmethod
	def exchage(inv, fromCard, toCard, gameConf):				
		"""
		交换宝石
		"""
		toSlot = None		
		if toCard.has_key('st_slot'):
			toSlot = toCard['st_slot']			
		toCard['st_slot'] = fromCard['st_slot']
		del fromCard['st_slot']
		dst = []
		if toSlot:
			fromCard['st_slot'] = toSlot			
			for i, ts in enumerate(fromCard['st_slot']):
				if ts and gameConf['stone_slot_level'][i] > fromCard['level']:
					inv.depositStone(ts)
					dst.append(ts)
					fromCard['st_slot'][i] = {}
		
		for i, ts in enumerate(toCard['st_slot']):			
			if ts and gameConf['stone_slot_level'][i] > toCard['level']:
					inv.depositStone(ts)
					dst.append(ts)
					toCard['st_slot'][i] = {}		
		return dst
		
