#coding:utf-8
#!/usr/bin/env python
from gclib.curl import curl
from gclib.json import json
from gclib.utility import drop as randrop, currentTime
from cardgame.settings import ARENE_SERVER
from game.utility.config import config



class medal:
		
	@staticmethod
	def make():
		return {'protect':0, 'grabmedalid':'', 'grabmedalchip':-1, 'grabmedalroleid':0, 'levelup_last_time':0}
			
	@staticmethod
	def getClientData(usr):
		data = {}
		data['medal_protect'] = usr.medal['protect']
		data['medal_levelup_last_time'] = usr.medal['levelup_last_time']
		return data
		
	@staticmethod
	def seek_holder(usr, medalid, chipnum):		
		res = json.loads(curl.url(ARENE_SERVER +  '/arena/seek_holder/', None, {'roleid':usr.roleid, 'level':usr.level, 'medalid':medalid, 'chipnum':chipnum}))
		
		if res.has_key('holder'):
		
			gameConf = config.getConfig('game')
			
			holder = []
		
			for h in res['holder']:
				usrh = usr.__class__.get(h)
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
		medalLevelConfig = config.getConfig('medal_level')
		medalInfo = medalConfig[medalid]		
		inv = usr.getInventory()
		if not inv.medal.has_key(medalid):
			return {'msg':'medal_not_exist'}		
				
		res = medal.levelupMedal(usr.roleid, medalid)
		if res.has_key('msg'):
			return res
				
		medalLevel = inv.medal[medalid]['level']
		medalLevelMax = len(medalLevelConfig[medalid])
		if medalLevelMax <= medalLevel:
			return {'msg':'medal_level_max'}
		
		for c in inv.medal[medalid]['chip']:
			if c < 1:
				return {'msg':'medal_chip_not_complete'}				
		
		for i in range(len(inv.medal[medalid]['chip'])):
			inv.medal[medalid]['chip'][i] = inv.medal[medalid]['chip'][i] - 1
			
		inv.medal[medalid]['gravel'] = inv.medal[medalid]['gravel'] + medalInfo['gravel']
		
		while medalLevelConfig[medalid][medalLevel] <= inv.medal[medalid]['gravel'] and medalLevelMax > medalLevel:
			medalLevel = medalLevel + 1			
		
		inv.medal[medalid]['level'] = medalLevel
		
		usr.medal['levelup_last_time'] = currentTime()
		
		inv.save()
		return inv.medal[medalid]
		
	@staticmethod
	def medalProtect(usr, sec):
		
		now = currentTime()
		
		if usr.medal_protect  < now:
			usr.medal_protect = usr.medal_protect + sec
		else:
			usr.medal_protect = now + sec
			
	@staticmethod
	def grabMedal(offenceRoleid, defenceRoleid, level, medalid, chipnum):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/grab_medal/', None, {'level':level, 'medalid':medalid, 'chipnum':chipnum, 'offenceRoleid': offenceRoleid, 'deffenceRoleid': defenceRoleid}))	
			
	@staticmethod
	def newMedal(usr, medalid, chipnum, cnt):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/new_medal/', None, {'roleid':usr.roleid, 'level':usr.level, 'medalid':medalid, 'chipnum':chipnum, 'count':cnt}))	
			
	def deleteMedal(usr, medalid, chipnum, cnt):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/delete_medal/', None, {'roleid':usr.roleid, 'level':usr.level, 'medalid':medalid, 'chipnum':chipnum, 'count':cnt}))	
			
	@staticmethod
	def levelupMedal(roleid, medalid):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/medal_levelup/', None, { 'medalid':medalid, 'roleid': roleid, 'medalid': medalid}))
			
	def grab(usr, defenceRoleid):
		gameConf = config.getConfig('game')
		
		if usr.sp < gameConf['medal_grab_sp']:
			return {'msg':'sp_not_enough'}				
		usr.sp = usr.sp - gameConf['medal_grab_sp']
		usr.medal['grabmedalroleid'] = defenceRoleid		
		return {'sp':usr.sp}
	
	@staticmethod
	def win(usr):
		
		gameConf = config.getConfig('game')
		
		if usr.medal['grabmedalroleid'] == 0:
			return {'msg':'medal_grab_shoulb_before'}		
		
		now = currentTime()
		defenceUsr = usr.__class__.get(usr.medal['grabmedalroleid'])
		
		if not defenceUsr:
			return {'msg':'usr_not_exist'}
		
		if randrop(gameConf['medal_grab_probablity']):
			res = medal.grabMedal(usr.roleid, defenceRoleid, usr.level, usr.medal['grabmedalid'], usr.medal['grabmedalchip'])
			if res.has_key('msg'):
				return res
			
			inv = usr.getIinventory()
			medalchip = inv.addMedalChip(usr.medal['grabmedalid'], usr.medal['grabmedalchip'])
			
			
			defenceInv = defenceUsr.getIinventory()
			defenceInv.delMedalChip(usr.medal['grabmedalid'], usr.medal['grabmedalchip'])
			usr.medal['grabmedalid'] = ''
			usr.medal['grabmedalchip'] = 0
			return {'update_medal_chip':medalchip}			
		return {}
			
	@staticmethod
	def grab(usr, grabRoleid):
		return {}
	@staticmethod
	def grab_fail(usr, defenceRoleid):
		return {}