#coding:utf-8
#!/usr/bin/env python

from gclib.utility import is_same_day, currentTime, day_diff, str_to_day_time, is_in_day_period
from game.utility.config import config
from game.routine.drop import drop
import random

class signin:
	
	@staticmethod
	def login(usr):
		now = currentTime()
		signinConf = config.getConfig('signin')
		dd = day_diff(now, usr.signin['last_login_time'])
		if dd == 1:
			usr.signin['login_count'] = usr.signin['login_count'] + 1
		elif dd > 1:
			usr.signin['login_count'] = 1
		usr.signin['last_login_time'] = currentTime()
		
		data = {}
		data['signin_index'] = (usr.signin['login_count'] - 1) % len(signinConf)
		data['have_signin'] = signin.have_signin(usr, now)
		usr.save()		
		return data
							
		
	@staticmethod
	def have_signin(usr, now):
		return is_same_day(usr.signin['last_signin_time'], now)
		
	@staticmethod
	def do_signin(usr):
		
		now = currentTime()
		
		if signin.have_signin(usr, now):
			return {'msg':'signin_already_have'}
		
		signinConf = config.getConfig('signin')
		signin_index = (usr.signin['login_count'] - 1) % len(signinConf)
		signinAward = signinConf[signin_index]
		
		awd = {}
		awd = drop.open(usr, signinAward['dropid'], awd)
		usr.signin['last_signin_time'] = now
		usr.save()
		return awd		
		
	@staticmethod
	def make():
		return {'last_signin_time':0, 'last_login_time':0, 'login_count':0, 'last_meal_time':[], 'continue_award_time':[], 'draw_award_time':[]}
		

	@staticmethod
	def reset(usr):
		usr.signin = signin.make()
		
	@staticmethod
	def meal(usr):
		now  = currentTime()
		gameConf = config.getConfig('game')
		if not signin.can_meal(now, usr.signin['last_meal_time'], gameConf):
			return {'msg':'meal_can_not'}
		
		usr.chargeStamina(gameConf['meal_point'])
		return {'stamina':usr.stamina}
	
	@staticmethod
	def can_meal(now, last_meal_time, gameConf):
		
		t1 = str_to_day_time(gameConf['meal_time1'][0])		
		t2 = str_to_day_time(gameConf['meal_time1'][1])
		if last_meal_time and is_in_day_period(t1, t2, now):
			if is_in_day_period(t1, t2, last_meal_time[-1]):
				return False
			else:
				return True
		t1 = str_to_day_time(gameConf['meal_time2'][0])
		t2 = str_to_day_time(gameConf['meal_time2'][1])
		if is_in_day_period(t1, t2, now):
			if last_meal_time and is_in_day_period(t1, t2, last_meal_time[-1]):
				return False
			else: 
				return True
		return False
	
	@staticmethod
	def continue_award(usr, no):
		openAwardConf = config.getConfig('open_award')
		if not signin.is_continue_award_available(no, openAwardConf):
			return {'msg':'open_award_not_available'}
		
		
		if usr.signin['login_count'] < no:
			return {'msg':'bad_parameter'}
				
		if signin.is_continue_award_already_get(usr, no):
			return {'msg':'open_award_already_get'}
		
		while len(usr.signin['continue_award_time']) < no:
			usr.signin['continue_award_time'].append(None)
		
		usr.signin['continue_award_time'][no - 1] = currentTime()
		
		cardid = openAwardConf['continue_award'][no - 1]
		
		inv = usr.getInventory()
		c = inv.addCard(cardid)
		inv.save()
		data = {}
		data['add_card'] = c
		return data
		
	@staticmethod
	def draw_award(usr):
		openAwardConf = config.getConfig('open_award')
		drawidx = []
		
		for t in usr.signin['draw_award_time']:
			if is_same_day(t, currentTime()):
				return {'msg':'open_award_already_get'}
		
		for idx, ad in enumerate(openAwardConf['draw_award']):
			 if len(usr.signin['draw_award_time']) > idx and not usr.signin['draw_award_time'][idx]:
			 	continue
			 if ad['day'] > len(usr.signin['draw_award_time']):
			 	continue			 	
			 drawidx.append(idx)
			 
		if not drawidx:
			return {'msg':'open_award_already_get'}
			
		adidx = random.sample(drawidx, 1)[0]
		ad = openAwardConf['draw_award'][adidx]
		data = {}
		data = drop.open(usr, ad['dropid'], data)
		while len(usr.signin['draw_award_time']) <= adidx:
			usr.signin['draw_award_time'].append(None)
		usr.signin['draw_award_time'][adidx] = currentTime()
		usr.save()		
		
		return data	
		
	@staticmethod
	def is_continue_award_available(no, openAwardConf):
		if len(openAwardConf['continue_award']) < no:
			return False
		if not openAwardConf['continue_award'][no -1]:
			return False
		return True
			
	@staticmethod
	def is_continue_award_already_get(usr ,no):
		if len(usr.signin['continue_award_time']) < no:
			return False
		
		if usr.signin['continue_award_time'][no - 1]:
			return True
		return False
