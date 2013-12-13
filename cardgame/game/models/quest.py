#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.utility import currentTime, is_same_day
from game.utility.config import config

class quest(object):
	
	def __init__(self):
		object.__init__(self)
		self.finish = {}
		self.current = {}
		
	def init(self):
		pass
	
	
	def getData(self):
		data = {}
		data['finish'] = self.finish
		data['current'] = self.current
		return data
		
		
	def load(self, roleid, data):
		object.load(self, roleid, data)
		self.finish = data['finish']
		self.current = data['current']
	
	def getClientData(self):
		self.updateQuest()
		return {'quest_current':self.current}	
	
	@staticmethod
	def makeQuest(questid):
		return {'count':0, 'create_time':currentTime()}
			
	def updateQuest(self):
		newQuest = self.getAvailableQuest()
		for quest_id in newQuest:
			self.accept(quest_id, False)
		self.save()
			
				
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
			for qid in self.finish:
				if self.finish[qid]['nextId'] == questid:
					if not is_same_day(self.finish[qid]['create_time'], currentTime()):
						return True
		return False 
			
	def accept(self, questid, isNotify=True):
		q = quest.makeQuest(questid)
		usr = self.user
		self.current[questid] = q
		if isNotify:
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
	
	@staticmethod
	def isOpen(questInfo):
		if not questInfo['isOpen']:
			return false
		
		
	def canAccept(self, questid):
		return true
		
	
		
			