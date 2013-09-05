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
		
		
	def getData(self):
		return self.cards
		
	def getClientData(self):
		return self.cards
		
	def load(self, roleid, data):
		self.roleid = roleid
		self.cards = data
		
	def addCard(self, card_id):
		carconf = config.getConfig('card')				
		if carconf.has_key(card_id):
			data = {}
			data['carid'] = card_id
			data['id'] = self.generateName()
			self.cards.append(data)			
			return data
		return None
		
	def delCard(self, name):
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