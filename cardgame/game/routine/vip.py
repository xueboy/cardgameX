#coding:utf-8\
#!/usr/bin/env python

from game.utility.config import config

class vip:
	
	@staticmethod
	def make():
		return {'level':0, 'charge':0}
			
			
	@staticmethod
	def charge(usr, point):
		
		vipConf = config.getConfig('vip')
		
		usr.vip['charge'] = usr.vip['charge'] + point
		
		for (i, p) in enumerate(vipConf['price']):
			if usr.vip['charge'] <= p:
				usr.vip['level'] = i + 1
				
	
	@staticmethod
	def level(usr):
		return usr.vip['level']
		
	@staticmethod
	def value(usr, name):
		vipConf = config.getConfig('vip')
		if not vipConf.has_key(name):
			return None
		return vipConf[name][usr.vip['level']]
		