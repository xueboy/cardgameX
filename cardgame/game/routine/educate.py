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
		
		gameConf = config.getConfig('game')
		educateGradeConf = config.getConfig('educate_grade')		
		
		now = currentTime()
		slot = usr.educate['edu_slot'][edupos]
		slot['card_id'] = cardid
		slot['start_time'] = now
		slot['start_level'] = usr.level
		slot['last_update_time'] = now		
		slot['rate'] = educateGradeConf[usr.educate['edt']]['rate']
		usr.save()
		
		return {'edu_slot':educate.getEduSlots(usr, gameConf)}
		
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
			
		
		return {'gold':usr.gold, 'gem':usr.gem, 'educate_edt':edt}				
		
	@staticmethod
	def make():
		data = {}
		data['edu_slot'] = [{}, {}, {}, {}, {}, {}]
		data['edt'] = 0
		return data
		
	@staticmethod
	def levelup_update(usr, gameConf):		
		for s, l in enumerate(usr.educate['edu_slot']):			
			if (gameConf['educate_auto_open_level'][s] <= usr.level) and (not l):				
				usr.educate['edu_slot'][s] = {'grade':1}

	@staticmethod
	def update_exp(usr, gameConf):
		
		educateConf = config.getConfig('educate')
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
				educateInfo = educateConf[edu_slot['start_level'] - 1]
				exp = educateInfo['expptm'] * (now - edu_slot['last_update_time']) / 600 * edu_slot['rate']
				card = inv.getCard(edu_slot['card_id'])
				pet.gainExp(card, exp, petConf, petLevelConf, gameConf)
				edu_slot['exp_last_update_time'] = now
				eduCard.append(card)				
		
				
	@staticmethod
	def getEduSlots(usr, gameConf):
		now = currentTime()
		data = copy.deepcopy(usr.educate['edu_slot'])
		for slot in data:
			if slot.has_key('start_time'):
				slot['finish_countdown'] = gameConf['educate_duration'] - (now - slot['start_time'])
				del slot['start_time']
				del slot['exp_last_update_time']
		return data
	
	@staticmethod
	def getClientData(usr, gameConf):	
		data = {}		
		data['edu_slot'] = educate.getEduSlots(usr, gameConf)
		data['edt'] = usr.educate['edt']
		return data