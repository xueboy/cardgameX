﻿#coding:utf-8
#!/usr/bin/env python

import copy
from gclib.utility import currentTime, drop
from game.utility.config import config
from game.routine.pet import pet
from game.routine.vip import vip
class educate:
	
	@staticmethod
	def start(usr, edupos, cardid):
		"""
		开始训练
		"""
		inv = usr.getInventory()
		card = inv.getCard(cardid)
		if not card:
			return {'msg':'card_not_exist'}
				
		if educate.is_edu_slot_start(usr, edupos):
			educate.stop(usr, edupos)			
				
		if educate.card_already_educate(usr, cardid):			
			return {'msg':'educate_card_already_educate'}
						
		gameConf = config.getConfig('game')
		educateConf = config.getConfig('educate')
		
		educateInfo = educateConf[usr.level - 1]		
		goldCost = educateInfo['gold']
		if goldCost > usr.gold:
			return {'msg':'gold_not_enough'}
				
		now = currentTime()
		slot = usr.educate['edu_slot'][edupos]
		slot['card_id'] = cardid
		slot['start_time'] = now
		slot['start_level'] = usr.level
		slot['last_update_time'] = now
		slot['fraction'] = 0.0
		slot['expptm'] = educateInfo['expptm']				
		slot['edt'] = usr.educate['edt']
		
		usr.gold = usr.gold - goldCost
		usr.educate['edt'] = 0
		usr.save()		
		return educate.getClientData(usr, gameConf)		
			
	@staticmethod
	def stop(usr, edupos):
		"""
		停卡训练
		"""
		gameConf = config.getConfig('game')
		educate.update_exp(usr, gameConf)
		if not educate.is_edu_slot_start(usr, edupos):
			return {'msg':'educate_edu_slot_not_start'}
		usr.educate['edu_slot'][edupos] = educate.make_open_edu_slot(0)
		usr.save()
		return educate.getClientData(usr, gameConf)
		
	@staticmethod
	def call(usr):
		"""
		召唤
		"""
		educateGradeConf = config.getConfig('educate_grade')
		
		edt = usr.educate['edt']		
		goldCost = educateGradeConf[edt]['price']['gold']
		gemCost = educateGradeConf[edt]['price']['gem']
		
		if goldCost > usr.gold:
			return {'msg': 'gold_not_enough'}
		if gemCost > usr.gem:
			return {'msg': 'gem_not_enough'}
				
		usr.gold = usr.gold - goldCost
		usr.gem = usr.gem - gemCost
				
		probability = educateGradeConf[edt]['probability']	
		
		if drop(probability):
			edt = edt + 1			
			if edt > (len(educateGradeConf) - 1):
				edt = len(educateGradeConf) - 1
		else:
			edt = 0
			
		if edt == 2 and (not vip.canEducateLevel2(usr)):
			return {'msg':'vip_required'}
		if edt == 3 and (not vip.canEducateLevel3(usr)):
			return {'msg':'vip_required'}
		if edt == 4 and (not vip.canEducateLevel4(usr)):
			return {'msg':'vip_required'}
		usr.educate['edt'] = edt			
		usr.save()
		return {'gold':usr.gold, 'gem':usr.gem, 'edu_edt':edt}				
	
	@staticmethod
	def open_edu_solt(usr):
		"""
		打开训练栏位
		"""
		
		gameConf = config.getConfig('game')
		gemCost = 0
		
		cnt = 0
		for solt in usr.educate:
			if solt:
				cnt = cnt + 1
				
		if vip.openEducateSlot(usr) < cnt:
			return {'msg':'vip_required'}		
				
		for i, solt in enumerate(usr.educate['edu_slot']):
			if not solt:
				gemCost = gameConf['educate_open_gem'][i]
				if usr.gem < gemCost:
					return {'msg':'gem_not_enough'}
				usr.educate['edu_slot'][i] = educate.make_open_edu_slot(0)
				return educate.getClientData(usr, gameConf)				
		return {'msg':'educate_all_edu_slot_open'}	
	
	@staticmethod
	def make():
		"""
		制做
		"""
		data = {}
		data['edu_slot'] = [{}, {}, {}, {}, {}, {}]
		data['edt'] = 0
		return data
		
	@staticmethod
	def make_open_edu_slot(edt):
		"""
		制做训练栏位
		"""
		return {'edt':edt}
	
	@staticmethod
	def make_null_edu_slot():
		"""
		制做空训练栏位
		"""
		return {}
		
	@staticmethod
	def levelup_update(usr, gameConf):
		"""
		should be called when user level up
		"""
		needSave = False		
		for s, l in enumerate(usr.educate['edu_slot']):			
			if (gameConf['educate_auto_open_level'][s] <= usr.level) and (not l):				
				usr.educate['edu_slot'][s] = educate.make_open_edu_slot(0)
				needSave = True
		if needSave:
			usr.save()			

	@staticmethod
	def is_edu_slot_start(usr, edupos):
		"""
		是否训练开始
		"""
		return usr.educate['edu_slot'][edupos].has_key('start_time')		
	
	@staticmethod
	def card_already_educate(usr, cardid):
		"""
		卡牌已经训练
		"""
		for slot in usr.educate['edu_slot']:
			if slot and slot.has_key('card_id') and slot['card_id'] == cardid:
				return True
		return False
		
	@staticmethod
	def update_exp(usr, gameConf):		
		"""
		更新经验
		"""
		petConf = config.getConfig('pet')
		petLevelConf = config.getConfig('pet_level')		
		inv = usr.getInventory()
				
		now = currentTime()
		eduCard = []
		for edu_slot in usr.educate['edu_slot']:
			if edu_slot and edu_slot.has_key('start_time'):
				educateGradeConf = config.getConfig('educate_grade')		
				educateEndTime = edu_slot['start_time'] + gameConf['educate_duration']
				educateDuration = now - edu_slot['last_update_time']				
				if now > educateEndTime:
					educateDuration = educateEndTime - edu_slot['last_update_time']
					del edu_slot['start_time']
					del edu_slot['last_update_time']
				else:
					edu_slot['last_update_time'] = now
				rate = educateGradeConf[edu_slot['edt']]['rate']
				exp = edu_slot['expptm'] * educateDuration / 3600 * rate + edu_slot['fraction']
				edu_slot['fraction'] = exp - int(exp)
				exp = int(exp)
				if exp:
					card = inv.getCard(edu_slot['card_id'])
					pet.gainExp(usr, card, int(exp), petConf, petLevelConf, gameConf)					
					eduCard.append(card)		
		inv.save()
		usr.save()	
				
	@staticmethod
	def getEduSlots(usr, gameConf):
		"""
		得到训练栏位
		"""
		now = currentTime()		
		edu_slot = usr.educate['edu_slot']
		data = {}
		data = []
		for slot in edu_slot:
			if slot.has_key('start_time'):
				s = educate.make_open_edu_slot(slot['edt'])
				countdown = gameConf['educate_duration'] - (now - slot['start_time'])
				if countdown < 0:
					countdown = 0
				s['expptm'] = slot['expptm']
				s['finish_countdown'] = countdown
				s['card_id'] = slot['card_id']
				data.append(s)
			elif slot:
				s = educate.make_open_edu_slot(slot['edt'])
				if slot.has_key('card_id'):
					s['card_id'] = slot['card_id']
				data.append(s)
			else:
				data.append({})
			
		return data
	
	@staticmethod
	def getClientData(usr, gameConf):	
		"""
		得到玩家数据
		"""
		data = {}		
		data['edu_slot'] = educate.getEduSlots(usr, gameConf)
		data['edu_edt'] = usr.educate['edt']
		return data