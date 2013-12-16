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
			
	def updateQuest(self, isNotify=False):
		newQuest = self.getAvailableQuest()
		for quest_id in newQuest:
			self.accept(quest_id, isNotify)
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
			
		if not quest.isActive(questInfo):
			return False
			
		for questid in self.finish:
			if qid == questid:
				alreadyFinish = True
				if self.finish[questid]['count'] >= questInfo['repeatCount']:
					return False
				break
			if questInfo['nextId'] == questid:
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
		
		if not quest.isActive(questInfo):
			return False
		alreadyFinishPre = questInfo['isFirst']			
			
		if not alreadyFinishPre:
			for qid in self.finish:
				if self.finish[qid]['nextId'] == questid:
					if not is_same_day(self.finish[qid]['create_time'], currentTime()):
						return True
		return False 
			
	def acceptQuest(self, questid, isNotify=True):
		
		questConf = config.getConfig('quest')
		questInfo = questConf[questid]
		if not self.canAccept(questInfo):
			return {'msg':'quest_can_not_accept'}
		
		q = quest.makeQuest(questid)
		usr = self.user
		self.current[questid] = q
		if isNotify:
			quest.notify_add_quest(q)			
		self.save()
		return q		
	
	@staticmethod
	def notify_add_quest(usr, q):
		if not usr.notify.has_key('quest_notify'):
			usr.notify['quest_notify'] = {}			
			if not usr.notify['quest_notify']['add_quest']:
				usr.notify['quest_notify']['add_quest'] = {}
			usr.notify['quest_notify']['add_quest'][questid] = q
			usr.save()
			
	@staticmethod
	def notify_finish_quest(usr, questid):
		if not usr.notify.has_key('quest_notify'):			
			usr.notify['quest_notify'] = {}			
			if not usr.notify['quest_notify'].has_key('finish_quest'):
				usr.notify['quest_notify']['finish_quest'] = []
			usr.notify['quest_notify']['finish_quest'].append(questid)
			usr.save()
	
	@staticmethod
	def isActive(questInfo):
		"""
		is in active duration
		"""
		if not questInfo['isOpen']:
			return False
		
		now = currentTime()
		if now < questInfo['beginTime']:
			return False
		if now > questInfo['endTime']:
			return False
		return True
			
		
	def canAccept(self, questInfo):		
		usr = self.user
		
		if usr.level < questInfo['level']:
			return False		
		if not self.isActive(questInfo):
			return False

		if not questInfo['isFirst']:
			alreadyFinishPre = False
			for q in self.finish:
				if self.finish[q]['nextId'] == questInfo['questid']:
					alreadyFinishPre = True
					break
			if not alreadyFinishPre:
				return False		
		return True
		
	@staticmethod
	def isFinish(questid,q):
		questConf = config.getConfig('quest')
		questInfo = questConf[questid]
		if questInfo['finishType'] == 'talk_npc_id':
			return True
		elif q.	has_key('finish') and q['finish'] == 1:
			return True
		
		
	def finishQuest(self, questid):
		if not self.current.has_key(questid):
			return {'msg':'quest_not_exist'}
		q = self.current[questid]
		usr = self.user
		if not quest.isFinish(questid, q):
			return {'msg':'quest_not_finish'}
		self.finish[questid] = q
	#	quest.notify_finish_quest(usr, questid)
		del self.current[questid]
		self.save()	
		return {'finish_quest':questid}
	
	def updateFinishDungeonQuest(self, dungeonId):		
		questConf = config.getConfig('quest')
		usr = self.user		
		for questid in self.current:
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'dungeon_id':
				if dungeonId == questInfo['finishValue']:
					self.current[questid]['dungeon_id'] = dungeonId
					self.current[questid]['finish'] = 1
					notify_finish_quest(usr, questid)
					self.finish.append(q)
					del self.current[questid]
		self.current = filter(lambda q: q.has_key('finish') and q['finish'], self.current)
		self.save()
		
	def updateFinishNpcQuest(self):
		pass
	
	def udpateFinishChardgeQuest(self, amount):
		questConf = config.getConfig('quest')
		usr = self.user		
		for questid in self.current:
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'charge_cumulate':
				if not self.current[questid].has_key('charge_count'):
					self.current[questid]['charge_count'] = 0
				self.current[questid]['charge_count'] = self.current[questid]['charge_count'] + amount
				if self.current[questid]['charge_count'] >= questInfo['finishValue']:
					self.current[questid]['finish'] = 1
					notify_finish_quest(usr, questid)
					self.finish.append(questid)		
					del self.current[questid]
		self.current = filter(lambda q: q.has_key('finish') and q['finish'], self.current)
		self.save()
		
	def updateFinishWorldTalkQuest(self):
		questConf = config.getConfig('quest')
		usr = self.user		
		for questid in self.current:
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'world_talk_count':
				if not self.current[questid].has_key('world_talk_count'):
					self.current[questid]['world_talk_count'] = 0
				self.current[questid]['world_talk_count'] = self.current[questid]['world_talk_count'] + 1
				if self.current[questid]['world_talk_count'] >= questInfo['finishValue']:
					self.current[questid]['finish'] = 1
					notify_finish_quest(usr, questid)
					self.finish.append(questid)
					del self.current[questid]
		self.current = filter(lambda q: q.has_key('finish') and q['finish'], self.current)
		self.save()
		
	def udpateFinishFriendQuest(self):
		questConf = config.getConfig('quest')
		usr = self.user
		for questid in self.current:
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'friend_count':
				usrNt = usr.getNetwork()
				if len(usrNt.friend) >= questInfo['finishValue']:
					self.current[questid]['finish'] = 1		
					notify_finish_quest(usr, questid)
					self.finish.append(questid)
					del self.current[questid]
		self.current = filter(lambda q: q.has_key('finish') and q['finish'], self.current)
		self.save()
	
		
	