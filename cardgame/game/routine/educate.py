#coding:utf-8
#!/usr/bin/env python

import copy
from gclib.utility import currentTime, drop
from game.utility.config import config
from game.routine.pet import pet

class educate:
	
	@staticmethod
	def start(usr, edupos, cardid):
		inv = usr.getInventory()
		card = inv.getCard(cardid)
		if not card:
			return {'msg':'card_not_exist'}
				
		if educate.is_edu_slot_start(usr, edupos):
			return {'msg':'educate_edu_slot_already_start'}
				
		if educate.card_already_educate(usr, cardid):
			return {'msg':'educate_card_already_educate'}
						
		gameConf = config.getConfig('game')
		educateGradeConf = config.getConfig('educate_grade')		
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
		slot['rate'] = educateGradeConf[usr.educate['edt']]['rate']
		slot['edt'] = usr.educate['edt']
		
		usr.gold = usr.gold - goldCost
		usr.educate['edt'] = 0
		usr.save()		
		return educate.getClientData(usr, gameConf)		
			
	@staticmethod
	def stop(usr, edupos):
		gameConf = config.getConfig('game')
		educate.update_exp(usr, gameConf)
		if not educate.is_edu_slot_start(edupos):
			return {'msg':'educate_edu_slot_not_start'}
		usr.educate['edu_slot'][edupos] = educate.make_open_edu_slot(0)
		usr.save()
		return educate.getClientData(usr, gameConf)
		
	@staticmethod
	def call(usr):
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
		rate = educateGradeConf[edt]['rate']
		
		if drop(probability):
			edt = edt + 1
			if edt > (len(educateGradeConf) - 1):
				edt = len(educateGradeConf) - 1
		else:
			edt = 0
		usr.educate['edt'] = edt			
		
		return {'gold':usr.gold, 'gem':usr.gem, 'edu_edt':edt}				
		
	@staticmethod
	def make():
		data = {}
		data['edu_slot'] = [{}, {}, {}, {}, {}, {}]
		data['edt'] = 0
		return data
		
	@staticmethod
	def make_open_edu_slot(edt):
		return {'edt':edt}
	
	@staticmethod
	def make_null_edu_slot():
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
		return usr.educate['edu_slot'][edupos].has_key('start_time')		
	
	@staticmethod
	def card_already_educate(usr, cardid):
		for slot in usr.educate['edu_slot']:
			if slot and slot.has_key('card_id') and slot['card_id'] == cardid:
				return True
		return False	
		
	@staticmethod
	def update_exp(usr, gameConf):		
		
		petConf = config.getConfig('pet')
		petLevelConf = config.getConfig('pet_level')		
		inv = usr.getInventory()
				
		now = currentTime()
		eduCard = []
		for edu_slot in usr.educate['edu_slot']:
			if edu_slot and edu_slot.has_key('start_time'):
				educateDuration = now - edu_slot['last_update_time']
				if educateDuration > gameConf['educate_duration']:
					educateDuration = gameConf['educate_duration']
					del edu_slot['start_time']
					del edu_slot['last_update_time']
				else: 
					exp = edu_slot['expptm'] * (now - edu_slot['last_update_time']) / 600 * edu_slot['rate'] + edu_slot['fraction']
				edu_slot['fraction'] = exp - int(exp)
				exp = int(exp)
				if exp:
					card = inv.getCard(edu_slot['card_id'])
					pet.gainExp(card, int(exp), petConf, petLevelConf, gameConf)
					edu_slot['last_update_time'] = now
					eduCard.append(card)		
		inv.save()		
				
	@staticmethod
	def getEduSlots(usr, gameConf):
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
				s['finish_countdown'] = countdown
				s['card_id'] = slot['card_id']
				data.append(s)
			else:
				data.append(slot)
		return data
	
	@staticmethod
	def getClientData(usr, gameConf):	
		data = {}		
		data['edu_slot'] = educate.getEduSlots(usr, gameConf)
		data['edu_edt'] = usr.educate['edt']
		return data