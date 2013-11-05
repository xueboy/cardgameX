#coding:utf-8
#!/usr/bin/env python

from gclib.utility import is_expire

class luckycat:
	@staticmethod
	def make():
		data = {}
		data['level'] = 0
		data['critical'] = []
		data['beckon_count'] = 0
		data['beckon_last_time'] = 0
		return data
		
		
	@staticmethod
	def beckon(usr):
		pass
		
		
		
		
	@staticmethod
	def isCritical(usr):
		pass
		
	@staticmethod
	def updateBeckonCount(usr):
		gameConf = config.getConfig('game')
		if is_expire(gameConf['luckycat_beckon_count_reset_time']):
			pass