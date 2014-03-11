#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import currentTime
from cardgame.settings import ARENE_SERVER

from game.utility.config import config

class gift:
	
	@staticmethod
	def send_gift_recored(sendRoleid, receiveRoleid):
		"""
		记录送礼
		"""
		return json.loads(curl.url(ARENE_SERVER +  '/arena/network_gift/', None, {'send_roleid':sendRoleid, 'receive_roleid': receiveRoleid}))
		
	@staticmethod	
	def send_gift(usr, item, friendid):
		"""
		送礼
		"""
		giftConf = config.getConfig('gift')
		if not giftConf.has_key(item):
			return {'msg':'gift_not_exist'}
		
		giftInfo = giftConf[item]
		
		usrNw = usr.getNetwork()
		goldCost = giftInfo['gold']
		if usr.gold < goldCost:
			return {'msg': 'gold_not_enough'}
		gemCost = giftInfo['gem']
		if usr.gem < gemCost:
			return {'msg': 'gem_not_enough'}
				
		usr.gold = usr.gold - goldCost
		usr.gem = usr.gem - gemCost
		
		friend = usr.__class__.get(friendid)
		if not friend:
			return {'msg':'usr_not_exist'}
		
		friendNw = friend.getNetwork()

		if not usrNw.gift.has_key(item):
			usrNw.gift[item] = {'receive_count':0, 'send_count':0}
		
		if not friendNw.gift.has_key(item):
			friendNw.gift[item] = {'receive_count':0, 'send_count':0}
		
		friendNw.gift[item]['receive_count'] = friendNw.gift[item]['receive_count'] + 1
		usrNw.gift[item]['send_count'] = usrNw.gift[item]['send_count'] + 1
		friendNw.charm = friendNw.charm + giftInfo['charm']				
		usrNw.tuhao = usrNw.tuhao + giftInfo['tuhao']
		gift.notify_new_gift(friend, item)
		
		usrNw.send_gift_record.append({'roleid':friendid, 'send_time':currentTime(), 'item':item})
		friendNw.receive_gift_record.append({'roleid':usr.roleid, 'receive_time':currentTime(), 'item':item})
	
		
		gameConf = config.getConfig('game')
		gift.update_send_gift_list(usr, gameConf)
		gift.update_receive_gift_list(friend, gameConf)
		
		usr.save()
		usrNw.save()
		friend.save()
		friendNw.save()
		gift.send_gift_recored(usrNw.roleid, friend.roleid)
		return {'tuhao':usrNw.tuhao, 'gold':usr.gold, 'gem': usr.gem}
		
	@staticmethod
	def update_send_gift_list(usr, gameConf):
		"""
		更新送礼列表
		"""
		usrNw = usr.getNetwork()
		cnt = len(usrNw.send_gift_record) - gameConf['gift_record_max_count']
		if cnt > 0:
			usrNw.send_gift_record = usrNw.send_gift_record[cnt:]		
				
	@staticmethod
	def update_receive_gift_list(usr, gameConf):
		"""
		接收送礼列表
		"""
		usrNw = usr.getNetwork()
		cnt = len(usrNw.receive_gift_record) - gameConf['gift_record_max_count']
		if cnt > 0:
			usrNw.receive_gift_record = usrNw.receive_gift_record[cnt:]
		
	@staticmethod
	def notify_new_gift(usr, item):
		"""
		提示新礼物
		"""
		usrNw = usr.getNetwork()	
		if not usr.notify.has_key('notify_add_gift'):
			usr.notify['notify_add_gift'] = []
		usr.notify['notify_add_gift'].append(item)
		usr.notify['network_charm'] = usrNw.charm
		
	@staticmethod
	def gift_ladder(usr, tp, begin, end):
		"""
		礼物天梯
		"""
		if tp != 'charm' and tp != 'tuhao':
			return {'msg':'parameter_bad'}
		return json.loads(curl.url(ARENE_SERVER +  '/arena/network_range/', None, {'roleid':usr.roleid, 'type':tp, 'begin': begin, 'end': end}))
	
		