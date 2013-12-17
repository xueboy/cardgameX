#coding:utf-8
#!/usr/bin/env python

from gclib.utility import randbigint

class drop:
	@staticmethod
	def open(usr, dropid):
		dropConf = config.getConfig('drop')
		
		rd = randbigint()
		dropInfo = dropConf[dropid]
		
		awd = {}
		
		for d in dropInfo:
			probablity = d['probability']
			msg = None
			if probablity == 1000000:
				msg = drop.award(usr, dropInfo, awd)
				if msg:
					break
			elif probablity < rd:
				rd = rd - probablity
			else:
				msg = drop.award(usr, dropInfo, awd)
				break
				
				
			
	def award(usr, dropInfo, awd):
		
		if dropInfo['type'] == 'st':
			usr.chargeStamina(dropInfo['count'])
			awd['st'] = usr.stamina
		if dropInfo['type'] == 'stone':
			inv = usr.getInventory()
			stone = inv.addStoneCount(dropInfo['id'], dropInfo['count'])
			if not awd.has_key('stone'):
				awd['stone'] = []
			awd['stone'].extend(stone)
	