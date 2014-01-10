#coding:utf-8
#!/usr/bin/env python

from gclib.utility import is_same_day, currentTime, day_diff, str_to_day_time, is_in_day_period
from game.utility.config import config
from game.routine.drop import drop

class signin:
	
	@staticmethod
	def login(usr):
		now = currentTime()
		signinConf = config.getConfig('signin')
		dd = day_diff(now, usr.signin['last_login_time'])
		if dd == 1:
			usr.sigin['login_count'] = usr.signin['login_count'] + 1
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
		return {'last_signin_time':0, 'last_login_time':0, 'login_count':0, 'last_meal_time':[]}
		

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
		
		