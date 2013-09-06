#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from game.utility.config import config
from game.game_def import serverid
from gclib.utility import currentTime
import time

class inventory(object):
	
	def __init__(self):
		self.cards = []
		self.team = ['', '', '', '', '']
		
		
	def getData(self):
		return {'cards':self.cards, 'team': self.team}
		
	def getClientData(self):
		return {'cards':self.cards, 'team': self.team}
		
	def load(self, roleid, data):
		self.roleid = roleid
		self.cards = data['cards']
		self.team = data['team']
		
	def addCard(self, card_id):
		carconf = config.getConfig('card')				
		if carconf.has_key(card_id):
			data = {}
			data['cardid'] = card_id
			data['id'] = self.generateName()
			data['level'] = 1
			data['exp'] = 0
			self.cards.append(data)			
			return data
		return None
		
	def delCard(self, cardid):
		if self.team.count (cardid) > 0:
			return 0
		for card in self.cards:
			if card['id'] == name:
				self.cards.remove(card)
				return 1
		return 0	
	
	def generateName(self):
		serveridLen = len(str(serverid))
		roleidLen = len(str(self.roleid))
		tm = time.gmtime(currentTime())
		ts = time.strftime('%Y%m%d%H%M%S', tm)
		no = self.user.getCardNo()		
		noLen = len(str(no))
		name = str(serveridLen) + str(serverid) + str(roleidLen) + str(self.roleid) + ts + str(noLen) + str(no)		
		return name
		
		
	def getCard(self, cardid):
		if self.team.count(cardid) > 0:
			return None
		for card in self.cards:			
			if card['id'] == cardid:
				return card
		return None
	
	def setTeam(self, cardid1, cardid2, cardid3, cardid4):
		
		if cardid1 != '':
			if cardid1 == cardid2 or cardid1 == cardid3 or cardid1 == cardid4 or cardid1 == self.team[0]:
				return self.team			
		if cardid2 != '':
			if cardid2 == cardid3 or cardid2 == cardid4 or cardid2 == self.team[0]:
				return self.team			
		if cardid3 != '':
			if cardid3 == cardid4 or cardid3 == self.team[0]:
				return self.team			
		if cardid4 != '':
			if cardid4 == self.team[0]:
				return self.team	
		
		if cardid1 == '':
			self.team[1] = ''
		else:
			self.team[1] = self.getCard(cardid1)['id']
		if cardid2 == '':
			self.team[2] = ''
		else:
			self.team[2] = self.getCard(cardid2)['id']
		if cardid3 == '':
			self.team[3] = ''
		else:
			self.team[3] = self.getCard(cardid3)['id']
		if cardid4 == '':
			self.team[4] = ''
		else:
			self.team[4] = self.getCard(cardid4)['id']		
		return self.team
	
	def setLeader(self, cardid):
		if cardid != '':
			if cardid == self.team[1] or cardid == self.team[2] or cardid == self.team[3] or cardid == self.team[4]:
				return self.team
		usr = self.user
		
		if cardid == '':
			self.team[0] = ''
			usr.leader = {}
		else:
			self.team[0] = self.getCard(cardid)['id']		
		usr.leader = cardid
		return self.team
	
		
		