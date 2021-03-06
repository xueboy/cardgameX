﻿#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config
from game.routine.drop import drop

class levelup:
	
	@staticmethod
	def award(usr, level):
		"""
		升级奖励
		"""
		if usr.level < level:
			return {'msg':'level_required'}
		if level in usr.levelup['record']:
			return {'msg':'levelup_award_already_have'}
				
		levelupConf = config.getConfig('levelup')
		
		levelKey = str(level)
		if not levelupConf.has_key(levelKey):
			return {'msg':'levelup_award_not_exist'}
		
		dropid = levelupConf[levelKey]
		
		awd = {}
		awd = drop.open(usr, dropid, awd)
		usr.levelup['record'].append(level)
		data = drop.makeData(awd, {})
		usr.save()
		return data
		
	@staticmethod
	def make():
		"""
		制做
		"""
		return {'record':[]}
			
	
		
