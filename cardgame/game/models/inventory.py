#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from game.utility.config import config

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
			data['id'] = card_id
			self.cards.append(data)			
			return data
		return None
		
	def delCard(self, idx):		
		print idx
		print len(self.cards)
		print idx > -1
		print len(self.cards) > idx
		if (idx > -1) and (len(self.cards) > idx):
			self.cards.pop(idx)
			return 1
		return 0