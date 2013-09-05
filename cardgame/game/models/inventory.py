#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from game.utility.config import config
from gclib.gcjson import gcjson

class inventory(object):
	
	def __init__(self):
		self.cards = []
		
		
	def getClientData(self):
		return self.cards
		
	def addCard(self, card_id):
		carconf = config.getConfig('card')
		if carconf.has_key(card_id):
			data = {}
			data['id'] = card_id
			self.cards.append(data)
			return data
		return None