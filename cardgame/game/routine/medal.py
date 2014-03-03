﻿#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import drop as randrop, currentTime
from cardgame.settings import ARENE_SERVER, SIGLE_SERVER
from game.utility.config import config
from game.routine.vip import vip

class medal:
		
	@staticmethod
	def make():
		return {'grabmedalid':'', 'grabmedalchip':-1, 'grabmedalroleid':0, 'levelup_last_time':0, 'levelup_medalid':'', 'levelup_count':0}
			
	@staticmethod
	def grabMedal(offenceRoleid, defenceRoleid, level, medalid, chipnum):
		if SIGLE_SERVER:
			from arenarank.routine.medal import medal as medalR
			return medalR.grab_medal(offenceRoleid, defenceRoleid, level, medalid, chipnum)
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/grab_medal/', None, {'level':level, 'medalid':medalid, 'chipnum':chipnum, 'offenceRoleid': offenceRoleid, 'deffenceRoleid': defenceRoleid}))	
			
	@staticmethod
	def newMedal(usr, medalid, chipnum, cnt):
		if SIGLE_SERVER:
			from arenarank.routine.medal import medal as medalR
			return medalR. new_medal(usr.roleid, usr.level, medalid, chipnum, cnt)
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/new_medal/', None, {'roleid':usr.roleid, 'level':usr.level, 'medalid':medalid, 'chipnum':chipnum, 'count':cnt}))	
			
	@staticmethod
	def tryGrab(defenceRoleid):
		if SIGLE_SERVER:
			from arenarank.routine.medal import medal as medalR
			return medalR.try_grab(defenceRoleid)
		else:
			return json.loads(curl.url(ARENE_SERVER + '/arena/try_grab/', None, {'defence_roleid': defenceRoleid}))
			
	@staticmethod
	def levelupMedal(roleid, medalid):
		if SIGLE_SERVER:
			from arenarank.routine.medal import medal as medalR
			return medalR.medal_levelup(roleid, medalidm)
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/medal_levelup/', None, { 'medalid':medalid, 'roleid': roleid, 'medalid': medalid}))
			
	@staticmethod
	def addProtectTime(usr, second):
		if SIGLE_SERVER:
			from arenarank.routine.medal import medal as medalR
			return medalR.add_protect_time(usr.roleid, second)
		else: 
			return json.loads(curl.url(ARENE_SERVER + '/arena/add_protect_time/', None, {'roleid': usr.roleid, 'add_second': second}))
			
	@staticmethod
	def seekHolder(usr, medalid, chipnum):
		if SIGLE_SERVER:
			from arenarank.routine.medal import medal as medalR
			return medalR.seek_holder(usr.roleid, usr.level, medalid, chipnum)
		else:
			return json.loads(curl.url(ARENE_SERVER +  '/arena/seek_holder/', None, {'roleid':usr.roleid, 'level':usr.level, 'medalid':medalid, 'chipnum':chipnum}))
			
	@staticmethod
	def getClientData(usr, gameConf):
		data = {}
		data['medal_protect_time'] = usr.medal['protect_time']
		data['medal_levelup_countdown'] = gameConf['medal_levelup_cooldown'] - currentTime() - usr.medal['levelup_last_time']
		if data['medal_levelup_countdown'] < 0:
			data['medal_levelup_countdown'] = 0
		return data
		
	@staticmethod
	def seek_holder(usr, medalid, chipnum):		
		res = medal.seekHolder(usr, medalid, chipnum)		
		if res.has_key('holder'):		
			gameConf = config.getConfig('game')			
			holder = []		
			for h in res['holder']:
				usrh = usr.__class__.get(h)
				if usrh:				
					holder.append(medal.getHolderData(usrh, gameConf))
			usr.medal['grabmedalid'] = medalid
			usr.medal['chipnum'] = chipnum
			return {'enemy':holder}
		return res			
			
	@staticmethod
	def getHolderData(h, gameConf):
		
		member = []
		for i in range(len(gameConf['medal_holder_appear_member_position'])):
			if gameConf['medal_holder_appear_member_position']:
				invh = h.getInventory()
				if invh.team[i]:
					ch = invh.getCard(invh.team[i])
					member.append(invh.getClientCard(ch))
		hData = {}
		hData['playerName'] = h.name
		hData['playerLevel'] = h.level
		hData['roleId'] = h.roleid
		hData['cards'] = member
		return hData
		
	@staticmethod
	def medallevelup(usr, medalid):
		
		
		
		medalConfig = config.getConfig('medal')
		medalInfo = medalConfig[medalid]		
		medalLevelConfig = config.getConfig('medal_level')
		medalLevelInfo = medalLevelConfig[medalid]		
		gameConf = config.getConfig('game')
		now = currentTime()
		
		medal.update_medal_levelup(usr, now, medalInfo, gameConf)
		
		if not medal.is_time_to_medal_levelup_finish(usr, now, gameConf):
			return {'msg' : 'medal_levelup_not_finish'}
				
		inv = usr.getInventory()				
		mroleid = inv.roleid		
		if not inv.medal.has_key(medalid):
			return {'msg':'medal_not_exist'}
				
		medalLevel = inv.medal[medalid]['level']
		medalLevelMax = len(medalLevelConfig[medalid])
		if medalLevelMax <= medalLevel:
			return {'msg':'medal_level_max'}
				
		for c in inv.medal[medalid]['chip']:
			if c < 1:
				return {'msg':'medal_chip_not_complete'}
						
		usr.medal['levelup_last_time'] = currentTime()
		usr.medal['levelup_medalid'] = medalid		
		
		if usr.medal['levelup_count'] < gameConf['medal_levelup_wink_finish_count']:
			medal.medal_levelup_finish(usr, now, medalInfo, medalLevelInfo, gameConf)
			res = medal.levelupMedal(usr.roleid, medalid)
			if res.has_key('msg'):
				return res
			inv.save()
			usr.save()
			return inv.medal[medalid]
		inv.save()
		usr.save()
		return {'medal_levelup_cooldown':gameConf['medal_levelup_cooldown']}
		
	@staticmethod
	def medal_levelup_finish(usr, now , medalInfo, medalLevelInfo, gameConf):
		medalid = usr.medal['levelup_medalid']
		inv = usr.getInventory()
		for i in range(len(inv.medal[medalid]['chip'])):
			inv.medal[medalid]['chip'][i] = inv.medal[medalid]['chip'][i] - 1
		inv.medal[medalid]['gravel'] = inv.medal[medalid]['gravel'] + medalInfo['gravel']
		medalLevel = inv.medal[medalid]['level']
		m = inv.medal
		while (medalLevelInfo[medalLevel + 1]['exp'] - medalLevelInfo[medalLevel]['exp']) <= inv.medal[medalid]['gravel']:
			inv.medal[medalid]['gravel'] = inv.medal[medalid]['gravel'] - (medalLevelInfo[medalLevel + 1]['exp'] - medalLevelInfo[medalLevel]['exp'])
			medalLevel = medalLevel + 1
			inv.medal[medalid]['level'] = medalLevel		
		usr.medal['levelup_last_time'] = 0
		usr.medal['levelup_medalid'] = ''		
		usr.medal['levelup_count'] = usr.medal['levelup_count'] + 1
		
	@staticmethod
	def is_time_to_medal_levelup_finish(usr, now, gameConf):
		if usr.medal['levelup_last_time'] == 0:
			return True
		return (usr.medal['levelup_last_time'] + gameConf['medal_levelup_cooldown']) < now
		
	@staticmethod
	def update_medal_levelup(usr, now, medalInfo, gameConf):
		if usr.medal['levelup_last_time'] == 0:
			return {}
		if medal.is_time_to_medal_levelup_finish(usr, now, gameConf):
			usr.medal['levelup_last_time'] = 0
			medalid = usr.medal['levelup_medalid']
			usr.medal['levelup_medalid'] = ''			
			return medal.levelupMedal(usr.roleid, medalid)
		return {}	
		
	@staticmethod		
	def grab(usr, defenceRoleid, medalid, chipnum):
		gameConf = config.getConfig('game')
						
		if usr.costSp(gameConf['medal_grab_sp_cost'])	< 0:
			return {'msg':'sp_not_enough'}
		usr.medal['grabmedalroleid'] = defenceRoleid
		usr.medal['grabmedalid'] = medalid
		usr.medal['grabmedalchip'] = chipnum
		
		defenceRole = usr.__class__.get(defenceRoleid)
		if not defenceRole:
			return {'msg':'user_not_exist'}	
		
		usr.save()		
		return {'sp':usr.sp, 'defence':defenceRole.pvpProperty()}
	
	@staticmethod
	def win(usr):
		
		gameConf = config.getConfig('game')
		
		defenceRoleid = usr.medal['grabmedalroleid']
		
		if defenceRoleid == 0:
			return {'msg':'medal_grab_shoulb_before'}		
				
		res = medal.tryGrab(defenceRoleid)
		if res.has_key('msg'):
			return res
		if res['protect']:
			return {'msg':'medal_player_in_protect'}
		
		now = currentTime()
		defenceUsr = usr.__class__.get(defenceRoleid)
		
		if not defenceUsr:
			return {'msg':'usr_not_exist'}
				
		probablity = gameConf['medal_grab_probablity']
		if vip.canMedalGrabProbabilityPromote(usr):
			probablity = probablity + 1000
		
		if randrop(probablity):
			
			medalid = usr.medal['grabmedalid']
			chipnum = usr.medal['grabmedalchip']
			medalConf = config.getConfig('medal')
			medalInfo = medalConf[medalid]
			
			res = medal.update_medal_levelup(defenceUsr, now, medalInfo, gameConf)
			if res.has_key('msg'):
				return res			
			
			defenceUsr_save = False
			defenceInv = defenceUsr.getInventory()
			if defenceUsr.medal['levelup_medalid'] and defenceUsr.medal['levelup_medalid'] == medalid:
				if defenceInv.medal[medalid][chipnum] < 2:
					medal.notify_medal_levelup_interrupt(defenceUsr, medalid)
					defenceUsr.medal['levelup_medalid'] = ''
					defenceUsr.medal['levelup_last_time'] = 0				
					defenceUsr_save = True
			
			res = medal.grabMedal(usr.roleid, usr.medal['grabmedalroleid'], usr.level, usr.medal['grabmedalid'], usr.medal['grabmedalchip'])
			if res.has_key('msg'):
				return res			
			inv = usr.getInventory()			
			
			if defenceInv.delMedalChip(usr.medal['grabmedalid'], usr.medal['grabmedalchip']) < 0:
				return {'msg':'medal_chip_not_enough'}
			medalid = usr.medal['grabmedalid']
			chipnum = usr.medal['grabmedalchip']
			medalchip = inv.addMedalChip(medalid, chipnum)
			usr.medal['grabmedalroleid'] = 0
			usr.medal['grabmedalid'] = ''
			usr.medal['grabmedalchip'] = 0
			usr.save()
			inv.save()
			if defenceUsr_save:
				defenceUsr.save()
			defenceInv.save()
			return { 'grabchipnum':chipnum, 'chip':medalchip['chip'] }
		return {}
	
	@staticmethod
	def grab_fail(usr, defenceRoleid):
		return {}
		
	@staticmethod
	def add_protect_time(usr, second):
		res = medal.addProtectTime(usr, second)		
		if res.has_key('msg'):
			return res		
		return res['protect_time']
			
	@staticmethod
	def notify_medal_levelup_interrupt(usr, medalid):
		if not usr.notify.has_key('medal_levelup_interrup'):
			usr.notify['medal_levelup_interrup'] = []
		usr.notify['medal_levelup_interrup'].append({'medalid' : medalid})
		
	@staticmethod
	def notify_medal_levelup_finish(usr, medalid):
		if not usr.notify.has_key('medal_levelup_finish'):
			usr.notify['medal_levelup_finish'] = []
		inv = usr.getInventory()
		usr.notify['medal_levelup_finish'].append(inv.medal[medalid])
		
			
		