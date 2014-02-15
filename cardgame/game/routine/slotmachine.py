#coding:utf-8
#!/usr/bin/env python

from gclib.utility import currentTime, str_to_date_time, is_same_day, randint
from game.utility.config import config

class slotmachine:
	
	@staticmethod
	def make():
		return {'play_time':[]}
	
	@staticmethod
	def play(usr):
		now = currentTime()
		
		gameConf = config.getConfig('game')
		
		isAvailable = True
		
		for ts in gameConf['slot_machine_open_time']:
			t = str_to_date_time(ts)
			if is_same_day(now, t):
				isAvailable = True
				break
				
		if not isAvailable:
			return {'msg':'slotmachine_not_available'}
						
		slotmachineConf = config.getConfig('slotmachine')
				
		times = len(usr.slotmachine['play_time'])
		
		if len(slotmachineConf['price']) <= times:		
			return {'msg':'slotmachine_max_time'}
				
		gemCost = slotmachineConf['price'][times]
				
		if usr.gem < gemCost:
			return {'msg':'gem_not_enough'}
		
		usr.gem = usr.gem - gemCost
		
		rd = randint()
				
		benefit = 1
		for bf in slotmachineConf['rate']:
			if rd > bf['probability']:
				rd = rd - bf['probability']
			else:
				benefit = bf['benefit']
				
		gem = int(gemCost * benefit)
		
		usr.gem = usr.gem + gem
		
		usr.slotmachine['play_time'].append(now)
		usr.save()
		
		
		return {'benefit':gem, 'gem':usr.gem}
				
		
		
	@staticmethod
	def getClientData(usr):
		return {'times':len(usr.slotmachine['play_time'])}
				
				
		
				
				