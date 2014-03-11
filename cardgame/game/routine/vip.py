#coding:utf-8\
#!/usr/bin/env python

from gclib.utility import currentTime, is_same_day
from game.utility.config import config

class vip:
	
	@staticmethod
	def make():
		"""
		制做
		"""
		return {'level':0, 'charge':0, 'buy_stamina_count':0, 'buy_sp_count':0, 'vip_last_update_time':0, 'buy_arena_times':0, 'buy_dungeon_reset_count':0, 'buy_arena_protect_times':0, 'reset_infection_pretige_score_times':0}
			
			
	@staticmethod
	def charge(usr, point):
		"""
		充值
		"""
		
		vipConf = config.getConfig('vip')		
		usr.vip['charge'] = usr.vip['charge'] + point		
		for (i, p) in enumerate(vipConf['price']):
			if usr.vip['charge'] <= p:
				usr.vip['level'] = i + 1
		usr.gem = usr.gem + point				
	
	@staticmethod
	def level(usr):
		"""
		等级
		"""
		return usr.vip['level']
		
	@staticmethod
	def value(usr, name):
		"""
		值
		"""
		vip.updateVip(usr)
		vipConf = config.getConfig('vip')
		if not vipConf.has_key(name):
			return None
		return vipConf[name][usr.vip['level']]
		
		
	@staticmethod
	def updateVip(usr):
		"""
		更新vip
		"""
		now = currentTime()
		if not is_same_day(usr.vip['vip_last_update_time'], now):
			usr.vip['buy_stamina_count'] = 0
			usr.vip['buy_sp_count'] = 0
			usr.vip['buy_arena_times'] = 0
			usr.vip['vip_last_update_time'] = now
			
			
	@staticmethod
	def canBuyStamina(usr):
		"""
		是否能够购买体力
		"""
		return vip.value(usr, 'buy_stamina_extra') > usr.vip['buy_stamina_count']
	
	@staticmethod
	def canBuySp(usr):
		"""
		是否能够购买sp
		"""
		return vip.value(usr, 'buy_sp_extra') > usr.vip['buy_sp_count']	
		
	@staticmethod
	def canStrengthEquipmentCritical(usr):
		"""
		可否装备强化暴击
		"""
		return vip.value(usr, 'strength_equipment_critical') != 0
	
	@staticmethod
	def canDungeonSweep(usr):
		"""
		可否地下城扫荡
		"""
		return vip.value(usr, 'dungeon_sweep') != 0
		
	@staticmethod
	def canBuyLuckycatBless(usr):
		"""
		可否购买招财猫祝福
		"""
		return vip.value(usr, 'buy_bless') != 0
		
	@staticmethod
	def canTrainLevel2(usr):
		"""
		可否使用2级培养
		"""
		return vip.value(usr, 'train_level2') != 0
		
	@staticmethod
	def canTrainLevel3(usr):
		"""
		可否使用3级培养
		"""
		return vip.value(usr, 'train_level3') != 0
		
	@staticmethod
	def canEducateLevel2(usr):
		"""
		可否使用2级训练
		"""
		return vip.value(usr, 'educate_level2') != 0
	
	@staticmethod
	def canEducateLevel3(usr):
		"""
		可否使用3级训练
		"""
		return vip.value(usr, 'educate_level3') != 0
		
	@staticmethod
	def canEducateLevel4(usr):
		"""
		可否使用4级训练
		"""
		return vip.value(usr, 'educate_level4') != 0
		
	@staticmethod
	def canEducateLevel5(usr):
		"""
		可否使用5级训练
		"""
		return vip.value(usr, 'educate_level5') != 0
		
	@staticmethod
	def openEducateSlot(usr):
		"""
		打开培养栏位
		"""
		return vip.value(usr, 'educate_slot_extra')
		
	@staticmethod
	def arenaTimes(usr):
		"""
		竞技场次数
		"""
		return vip.value(usr, 'arena_times_extra')
		
	@staticmethod
	def canBuyArenaTimes(usr):
		"""
		是否可以购买竞技场次数
		"""
		return vip.value(usr, 'arena_times_buy') > usr.vip['buy_arena_times']
		
	@staticmethod
	def canBuyDungeonResetCount(usr):
		"""
		是否可以购买地下城重置次数
		"""
		return vip.value(usr, 'dungeon_count_reset') > usr.vip['buy_dungeon_reset_count']
		
	@staticmethod
	def canBuyArenaProtectTimes(usr):
		"""
		是否可以购买竞技城保护时间
		"""
		return vip.value(usr, 'arena_protect_times') > usr.vip['buy_arena_protect_times']
		
	@staticmethod
	def canMedalGrabProbabilityPromote(usr):
		"""
		是否增加勋章抢夺机率
		"""
		return vip.value(usr, 'medal_grab_probability10') != 0
		
	@staticmethod
	def explore_critical_times(usr):
		"""
		探索暴击次数
		"""
		return vip.value(usr, 'explore_critical_times')
		
	@staticmethod
	def canResetInfectionPrestigeScoreCount(usr):
		"""
		可以重置感染声望次数
		"""
		return vip.value(usr, 'infection_prestige_score_reset') > usr.vip['reset_infection_pretige_score_times']