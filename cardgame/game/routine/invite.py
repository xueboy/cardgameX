#coding:utf-8
#!/usr/bin/env python

from gclib.utility import currentTime
from game.utility.config import config
from game.utility.invite import invite as inviteU
from game.routine.drop import drop



class invite:
	@staticmethod
	def make():
		return {'invite':[], 'invitee':[], 'open_time': 0, 'invite_award':[]}
			
	@staticmethod
	def getClientData(usr):
		data = {}
		data['invite_code'] = ''
		if usr.accountid != 0:
			data['invite_code'] = inviteU.generateCode(usr.accountid)		
		data['invite'] = usr.invite['invite']
		data['open_time'] = usr.invite['open_time']
		data['invite_award'] = usr.invite['invite_award']
		return data
		
	@staticmethod
	def onLogin(usr):
		if not usr.invite['open_time']:
			usr.invite['open_time'] = currentTime()
			
			
	@staticmethod
	def enterInviteCode(usr, invite_code):
		
		gameConf = config.getConfig('game')				
		accountid = inviteU.reverseCode(invite_code)
		
		now = currentTime()
		if now - usr.invite['open_time'] > gameConf['invite_open_duration']:
			return {'msg':'invite_not_available'}
		
		invAccount = usr.getAccountCls().get(accountid)
		if not invAccount:
			return {'msg':'invite_code_bad'}
		if usr.accountid == accountid:
			return {'msg': 'invite_can_not_self'}
		
		
		
		invUsr = invAccount.getUser()
		if len(invUsr.invite['invite']) >= gameConf['invite_max_count']:
			return {'msg': 'invitee_max_count'}
		if str(usr.roleid) in invUsr.invite['invite']:
			return {'msg':'invite_code_already_use'}
		invUsr.invite['invite'].append(str(usr.roleid))
		
		if str(invUsr.roleid) in usr.invite['invitee']:
			return {'msg':'invite_code_already_use'}
		usr.invite['invitee'].append(str(invUsr.roleid))
		
		inviteConf = config.getConfig('invite')
		
		dropid = inviteConf['invitee_award']
		awd = {}
		data = {}
		if dropid:
			awd = drop.open(usr, dropid, awd)
			data = drop.makeData(awd, {})
		
		invUsr.save()
		usr.save()
		data.update(invite.getClientData(usr))
		return data
		
	@staticmethod
	def inviteAward(usr, inviteCount):
		
		if inviteCount > len(usr.invite['invite']):
			return {'msg':'invite_count_not_enough'}
		
					
		while len(usr.invite['invite_award']) < (inviteCount + 1):
			usr.invite['invite_award'].append('')
		
		if usr.invite['invite_award'][inviteCount]:
			return {'msg':'invite_award_already_have'}
				
		inviteConf = config.getConfig('invite')
		
		dropid = inviteConf['invite_award'][inviteCount]
		if not dropid:
			return {'msg': 'invite_not_have_award'}
				
		

		
		usr.invite['invite_award'][inviteCount] = dropid
		awd = {}
		awd = drop.open(usr, dropid, awd)		
		data = drop.makeData(awd, {})				
		data.update(invite.getClientData(usr))
		usr.save()
		
		return data