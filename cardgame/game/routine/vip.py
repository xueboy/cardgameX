#coding:utf-8\
#!/usr/bin/env python

from gclib.utility import currentTime, is_same_day
from game.utility.config import config

class vip:
	
	@staticmethod
	def make():
		return {'level':0, 'charge':0, 'buy_stamina_count':0, 'buy_sp_count':0, 'vip_last_update_time':0, 'buy_arena_times':0, 'buy_dungeon_reset_count':0}
			
			
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
		if not is_same_day(usr.vip['vip_last_update_time'], now):
			usr.vip['buy_stamina_count'] = 0
			usr.vip['buy_sp_count'] = 0
			usr.vip['buy_arena_times'] = 0
			usr.vip['vip_last_update_time'] = now
			
			
	@staticmethod
	def canBuyStamina(usr):
		return vip.value(usr, 'buy_stamina_extra') > usr.vip['buy_stamina_count']
	
	@staticmethod
	def canBuyStamina(usr):
		return vip.value(usr, 'buy_sp_extra') > usr.vip['buy_sp_count']	
		
	@staticmethod
	def canStrengthEquipmentCritical(usr):
		return vip.value(usr, 'strength_equipment_critical') != 0
	
	@staticmethod
	def canDungeonSweep(usr):
		return vip.value(usr, 'dungeon_sweep') != 0
		
	@staticmethod
	def canBuyLuckycatBless(usr):
		return vip.value(usr, 'buy_bless') != 0
		
	@staticmethod
	def canTrainLevel2(usr):
		return vip.value(usr, 'train_level2') != 0
		
	@staticmethod
	def canTrainLevel3(usr):
		return vip.value(usr, 'train_level3') != 0
		
	@staticmethod
	def canEducateLevel2(usr):
		return vip.value(usr, 'educate_level2') != 0
	
	@staticmethod
	def canEducateLevel3(usr):
		return vip.value(usr, 'educate_level3') != 0
		
	@staticmethod
	def canEducateLevel4(usr):
		return vip.value(usr, 'educate_level4') != 0
		
	@staticmethod
	def canEducateLevel5(usr):
		return vip.value(usr, 'educate_level5') != 0
		
	@staticmethod
	def openEducateSlot(usr):
		return vip.value(usr, 'educate_slot_extra')
		
	@staticmethod
	def arenaTimes(usr):
		return vip.value(usr, 'arena_times_extra')
		
	@staticmethod
	def canBuyArenaTimes(usr):
		return vip.value(usr, 'arena_times_buy') > usr.vip['buy_arena_times']
		
	@staticmethod
	def canBuyDungeonResetCount(usr):
		return vip.value(usr, 'dungeon_count_reset') > usr.vip['buy_dungeon_reset_count']