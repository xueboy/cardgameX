#coding:utf-8\
#!/usr/bin/env python

from game.utility.config import config

class vip:
	
	@staticmethod
	def make():
		return {'level':0, 'charge':0, 'buy_stamina_count':0, 'buy_sp_count':0, 'last_vip_update':0}
			
			
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
		vip.updateVip(usr)
		vipConf = config.getConfig('vip')
		if not vipConf.has_key(name):
			return None
		return vipConf[name][usr.vip['level']]
		
		
	@staticmethod
	def updateVip(usr):
		now = currentTime()
		if not is_same_day(usr.vip['last_vip_update'], now):
			usr.vip['buy_stamina_count'] = 0
			usr.vip['buy_sp_count'] = 0
			usr.vip['last_vip_update'] = now
			
			
	@staticmethod
	def canBuyStamina(usr):
		return vip.value(usr, 'buy_stamina_extra') > usr.vip['buy_stamina_count']
	
	@staticmethod
	def canBuyStamina(usr):
		return vip.value(usr, 'buy_sp_extra') > usr.vip['buy_sp_count']	
	
		