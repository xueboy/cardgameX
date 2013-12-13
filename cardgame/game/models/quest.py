#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.utility import currentTime
from game.utility.config import config

class quest(object):
	
	def __init__(self):
		object.__init__(self)
		self.finish = {}
		self.current = {}
		
	def init(self):
		pass
	
	def getClientData(self):
		return {'quest_current':self.current, 'quest_available':self.getAvailableQuest()}	
	
	@staticmethod
	def makeQuest(questid):
		return {'count':0, 'create_time':currentTime()}
				
	def getAvailableQuest(self):
		
		questConf = config.getConfig('quest')
		usr = self.user
		newQuest = []
		for qid in questConf:			
			if questConf[qid]['type'] == 1:
				if self.commonIsAvailable(usr, qid, questConf[qid]):
					newQuest.append(qid)
			elif questConf[qid]['type'] == 2:
				if self.dayIsAvailable(usr, qid, questConf[qid]):			
					newQuest.append(qid)					
		return newQuest		
		
	def commonIsAvailable(self, usr, qid, questInfo):				
		newQuest = []		
		alreadyAccept = False
		alreadyFinishPre = False
		alreadyFinish = False		
		if questInfo['level'] > usr.level:
			return False
			
		for questid in self.finish:
			if qid == questid:
				alreadyFinish = True
				if self.finish[questid]['count'] >= questInfo['repeatCount']:
					return False
				break
			if q['nextId'] == questid:
				alreadyFinishPre = True
		
		for questid in self.current:
			if qid == questid:
				return False			
		if questInfo['isFirst'] or alreadyFinishPre:
			return True
		return False
					
	def dayIsAvailable(self, usr, qid, questInfo):				
		if questInfo['level'] > usr.level:
			return False
		alreadyFinishPre = questInfo['isFirst']			
			
		if not alreadyFinishPre:
			for qid, q in self.finish:
				if q['nextId'] == questid:
					return True					
		return False 
			
	def accept(self, questid):
		q = quest.makeQuest(questid)
		usr = self.user
		self.current.append(q)
		if not usr.notify['quest_notify']:
			usr.notify['quest_notify'] = {}
			
		if not usr.notify['quest_notify']['add_quest']:
			usr.notify['quest_notify']['add_quest'] = []
		usr.notify['quest_notify']['add_quest'][questid] = q
		usr.save()
		self.save()
		
	def addQuest(self, questid):		
		if self.canAccept(questid):
			self.accept(questid)
			
		
	def canAccept(self, questid):
		return true
		
	
		
			