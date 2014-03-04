#coding:utf-8
#!/usr/bin/env python

import random
from gclib.utility import randint, currentTime, is_same_day
from gclib.DBConnection import DBConnection
from game.utility.config import config
from game.routine.drop import drop
from game.routine.vip import vip
from game.routine.infection import infection

class explore:
	
	@staticmethod
	def make():
		return {'times':0, 'last_update_times_time':0, 'critical_count':0}
			
	@staticmethod
	def getClientData(usr):
		data = {}
		data['times'] = usr.explore['times']
		if usr.explore['last_update_times_time'] == 0:
			data['update_times_before'] = 0
		else:
			data['update_times_before'] = currentTime() - usr.explore['last_update_times_time']
		data['critical_count'] = usr.explore['critical_count']
		return data
			
	@staticmethod
	def explore(usr):
		
		explore.update_explore(usr)
		
		exploreConf = config.getConfig('explore_award')		
		exploreInfo = exploreConf[str(usr.level)]
		gameConf = config.getConfig('game')
		usr.explore['times'] = usr.explore['times'] + 1
		if usr.explore['times'] >= gameConf['explore_max_times']:
			return {'msg':'explore_max_times'}
		usr.explore['last_update_times_time'] = currentTime()
		awd = {}
		awd = drop.roll(exploreInfo[0], awd)
		rv = random.uniform(gameConf['explore_gold_and_exp_revision'][0], gameConf['explore_gold_and_exp_revision'][1])
		if awd.has_key('gold'):
			awd['gold'] = awd['gold'] * rv
		if awd.has_key('exp'):
			awd['exp'] = awd['exp'] * rv
		rd = randint()
		if rd < gameConf['explore_critical_probability'] + usr.explore['critical_count'] * gameConf['explore_critical_probability_growth']:
			for key in awd:
				awd[key] = awd[key] * gameConf['explore_critical_income_rate']
			
		awd = drop.roll(exploreInfo[1], awd)		
		awd = drop.do_award(usr, awd, {})		
		data = drop.makeData(awd, {})
		
		rd = randint()		
		if rd < gameConf['explore_extra_times_probability']:
			usr.explore['times'] = usr.explore['times'] - 1						
			if usr.explore['times'] < 0:
				usr.explore['times'] = 0
			data['explore_times'] = usr.explore['times']
						
		rd = randint()
		if rd < gameConf['explore_friend_probability']:
			friendData = explore.recommend_friend(usr)
			if friendData:
				data['friend_data'] = friendData
		
		rd = randint()
		if rd < gameConf['infection_explore_probability']:
			infaction_battle = infection.explore_encounter(usr, gameConf)
			if infaction_battle:
				data['infaction_battle'] = infaction_battle		
		
		usr.save()
		return data
		
	@staticmethod
	def recommend_friend(usr):
		nw = usr.getNetwork()
		
		fl = nw.friend.keys()
		fl.extend(nw.request_list.keys())		
		fl.append('0')
		sql = ''
		if usr.gender == 'male':
			sql = 'SELECT roleid FROM account WHERE roleid not in ' + '(' + (','.join(fl)) + ')' + ' ORDER BY lastlogin, gender LIMIT 1'
		else:
			sql = 'SELECT roleid FROM account WHERE roleid not in ' + '(' + (','.join(fl)) + ')' + ' ORDER BY lastlogin, gender DESC LIMIT 1'
		conn = DBConnection.getConnection()
		res = conn.query(sql,[])		
		if res:
			friend = usr.__class__.get(res[0][0])
			return friend.getFriendData()			
		return {}
		
	@staticmethod
	def buy_critical_times(usr):
		
		gameConf = config.getConfig('game')			
		
		explore.update_explore(usr)	
		
		if usr.explore['critical_count'] >= vip.explore_critical_times(usr):
			return {'msg':'vip_required'}
		usr.explore['critical_count'] = usr.explore['critical_count'] + 1		
		gemCost = gameConf['explore_critical_price'][usr.explore['critical_count'] - 1]
		if gemCost > usr.gem:
			return {'msg':'gem_not_enough'}
		usr.gem = usr.gem - gemCost
		usr.explore['last_update_times_time'] = currentTime()		
		usr.save()
		return {'explore_critical' : usr.explore['explore_critical']}
		
	@staticmethod
	def update_explore(usr):
		now = currentTime()		
		if not is_same_day(usr.explore['last_update_times_time'], now):
			usr.explore['times'] = 0
			usr.explore['last_update_times_time'] = 0
			usr.explore['critical_count'] = 0
			
	@staticmethod
	def on_user_levelup(usr):
		usr.explore['times'] = usr.explore['times'] - 12
		if usr.explore['times'] < 0:
			usr.explore['times'] = 0			
		usr.explore['last_update_times_time'] = currentTime()
		explore.notify_explore_times(usr)
	
	@staticmethod
	def notify_explore_times(usr):
		usr.notify['notify_explore_times'] = usr.explore['times']
			