#coding:utf-8
#!/usr/bin/env python

from gclib.utility import currentTime

class quest(object):
	
	def __init__(self):
		object.__init__(self)
		self.finish = []
		self.current = []
		
	@staticmethod
	def makeQuest(questid):
		return {'questid':questid, 'count':0, 'create_time':currentTime()}
		
		
	def levelUpdate(self):
		questConf = config.getConfig('quest')
		usr = self.user
		for questid ,questInfo in questConf:
			alreadyAccept = False
			if questInfo['level'] <= usr.level:
				for q in self.finish:
					if q['questid'] == questid:
						alreadyAccept = True
						break
				if alreadyAccept:
					continue
				for q in self.current:
					if q['questid'] == questid:
						alreadyAccept = True
						break
				if alreadyAccept:
					continue
				self.accept(questid)
			
	def accept(self, questid):
		q = quest.makeQuest(questid)
		usr = self.user
		self.current.append(q)
		if not usr.notify['quest_notify']:
			usr.notify['quest_notify'] = {}
			
		if not usr.notify['quest_notify']['add_quest']:
			usr.notify['quest_notify']['add_quest'] = []
		usr.notify['quest_notify']['add_quest'].append(q)
		usr.save()
		self.save()
		
	def addQuest(self, questid):
		
		if self.canAccept(questid):
			self.accept(questid)
			
		
	def canAccept(self, questid):
		return true
		
			