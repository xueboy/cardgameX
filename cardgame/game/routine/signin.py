#coding:utf-8
#!/usr/bin/env python

from gclib.utility import is_same_day, currentTime, day_diff, str_to_day_time, is_in_day_period
from game.utility.config import config
from game.routine.drop import drop
import random

class signin:
	
	@staticmethod
	def login(usr):
		"""
		登陆
		"""
		now = currentTime()
		gameConf = config.getConfig('game')
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
		
		t1 = [str_to_day_time(gameConf['meal_time1'][0]), str_to_day_time(gameConf['meal_time1'][1])]
		t2 = [str_to_day_time(gameConf['meal_time2'][0]), str_to_day_time(gameConf['meal_time2'][1])]
		
		b1 = False
		b2 = False
		
		if  len(usr.signin['last_meal_time']) > 2:
			usr.signin['last_meal_time'] =  usr.signin['last_meal_time'][-2:-1]
		
		if len(usr.signin['last_meal_time']) > 1:
			if is_in_day_period(t1[0], t1[1], usr.signin['last_meal_time'][-2]) or is_in_day_period(t1[0], t1[1], usr.signin['last_meal_time'][-1]):
				b1 = True
			if is_in_day_period(t2[0], t2[1], usr.signin['last_meal_time'][-1]):
				b2 = True			
		elif len(usr.signin['last_meal_time']) > 0:
			if is_in_day_period(t1[0], t1[1], usr.signin['last_meal_time'][-1]):
				b1 = True
			if is_in_day_period(t2[0], t2[1], usr.signin['last_meal_time'][-1]):
				b2 = True
		data['last_meal_time'] = [b1, b2]
		if len(usr.signin['continue_award_time']) == 2:
			data['continue_award_time'] = [True, True]
		elif len(usr.signin['continue_award_time']) == 0:
			data['continue_award_time'] = [True]
		elif day_diff(now, usr.signin['continue_award_time'][-1]) == 1:
			data['continue_award_time'] = [True]
		else:
			data['continue_award_time'] = [False]
		data['continue_award'] = usr.signin['continue_award_time']
		data['draw_award'] = usr.signin['draw_award_time']
		usr.save()		
		return data
							
		
	@staticmethod
	def have_signin(usr, now):
		"""
		是否已经签到
		"""
		return is_same_day(usr.signin['last_signin_time'], now)
		
	@staticmethod
	def do_signin(usr):
		"""
		是否签名
		"""
		
		now = currentTime()
		
		if signin.have_signin(usr, now):
			return {'msg':'signin_already_have'}
		
		signinConf = config.getConfig('signin')
		signin_index = (usr.signin['login_count'] - 1) % len(signinConf)
		signinAward = signinConf[signin_index]
		
		awd = {}
		awd = drop.open(usr, signinAward['dropid'], awd)
		awd = drop.makeData(awd, {})
		usr.signin['last_signin_time'] = now
		usr.save()
		return awd		
		
	@staticmethod
	def make():
		"""
		制做
		"""
		return {'last_signin_time':0, 'last_login_time':0, 'login_count':0, 'last_meal_time':[], 'continue_award_time':[], 'draw_award_time':[]}
		

	@staticmethod
	def reset(usr):
		"""
		重制
		"""
		usr.signin = signin.make()
		
	@staticmethod
	def meal(usr):
		"""
		用餐
		"""
		now  = currentTime()
		gameConf = config.getConfig('game')
		if not signin.can_meal(now, usr.signin['last_meal_time'], gameConf):
			return {'msg':'meal_can_not'}
		usr.signin['last_meal_time'].append(now)
		
		usr.chargeStamina(gameConf['meal_point'])
		return {'stamina':usr.stamina}
	
	@staticmethod
	def can_meal(now, last_meal_time, gameConf):		
		"""
		可以用餐
		"""
		t1 = str_to_day_time(gameConf['meal_time1'][0])		
		t2 = str_to_day_time(gameConf['meal_time1'][1])
		if is_in_day_period(t1, t2, now):
			if last_meal_time and is_in_day_period(t1, t2, last_meal_time[-1]):
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
	def continue_award(usr):
		"""
		连续登陆
		"""
		openAwardConf = config.getConfig('open_award')
		if not signin.is_continue_award_available(openAwardConf):
			return {'msg':'open_award_not_available'}
							
		if signin.is_continue_award_already_get(usr):
			return {'msg':'open_award_already_get'}
		
		now = currentTime()
		if not usr.signin['continue_award_time']:
			if day_diff(now, usr.signin['continue_award_time'][-1]) != 1:
				usr.signin['continue_award_time'] = []
				
		usr.signin['continue_award_time'].append(now)
		
		
		cardid = openAwardConf['continue_award'][len(usr.signin['continue_award_time']) - 1]
		
		inv = usr.getInventory()
		c = inv.addCard(cardid)
		inv.save()
		usr.save()
		data = {}
		data['add_card'] = c
		return data
		
	@staticmethod
	def draw_award(usr):
		"""
		开服奖励
		"""
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
		awd = {}
		awd = drop.open(usr, ad['dropid'], awd)
		while len(usr.signin['draw_award_time']) <= adidx:
			usr.signin['draw_award_time'].append(None)
		usr.signin['draw_award_time'][adidx] = currentTime()
		usr.save()
		data = drop.makeData(awd, {})
		
		return data	
		
	@staticmethod
	def is_continue_award_available(no, openAwardConf):
		"""
		连续登陆奖励是否有效
		"""
		if usr.signin['login_count'] < 2:
			return False
		if len(openAwardConf['continue_award']) <= usr.signin['continue_award_time']:
			return False		
		return True
			
	@staticmethod
	def is_continue_award_already_get(usr):
		"""
		连续登陆奖励是否已领
		"""
		now = currentTime()		
		if not usr.signin['continue_award_time']:
			return True
		
		for award_time in usr.signin['continue_award_time']:
			if is_same_day(award_time, now):
				return True		
		return False
