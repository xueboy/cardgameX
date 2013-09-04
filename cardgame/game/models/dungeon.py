#coding:utf-8
#!/usr/bin/env python

from gclib.object import object


class dungeon(object):
	
	def getData(self):
		data = {}
		data['normal_finished'] = []	#[lastBattle, lastField]
		return data
		
	def getClientData(self):
		return self.getData()
			
		