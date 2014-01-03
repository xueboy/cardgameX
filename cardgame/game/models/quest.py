﻿#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.utility import currentTime, is_same_day
from game.utility.config import config
from game.routine.drop import drop

class quest(object):
	
	def __init__(self):
		object.__init__(self)
		self.finish = {}
		self.current = {}
		self.drama = {}
		self.user = None
		
	def init(self):
		pass
	
	def install(self, roleid):
		object.install(self, roleid)
	
	def getData(self):
		data = {}
		data['finish'] = self.finish
		data['current'] = self.current
		data['drama'] = self.drama
		return data
		
		
	def load(self, roleid, data):
		object.load(self, roleid, data)
		self.finish = data['finish']
		self.current = data['current']
		self.drama = data['drama']
	
	def getClientData(self):
		self.updateQuest()
		current = {}		
		for q in self.current:
			t = self.current[q].copy()
			
			if t.has_key('charge_count'):
				t['count'] = t['charge_count']
				del t['charge_count']
			if t.has_key('world_talk_count'):
				t['count'] = t['world_talk_count']
				del t['world_talk_count']
			if t.has_key('vip_item_buy_count'):
				t['count'] = t['vip_item_buy_count']
				del t['vip_item_buy_count']
			if t.has_key('arena_win_count'):
				t['count'] = t['arena_win_count']
				del t['arena_win_count']
			if t.has_key('dungeon_count'):
				t['count'] = t['dungeon_count']
				del t['dungeon_count']
			if t.has_key('dungeon_id'):			
				del t['dungeon_id']
			if t.has_key('field_id'):			
				del t['field_id']				
			current[q] = t
		return {'quest_current':current, 'quest_drama':self.drama}	
	
	@staticmethod
	def makeQuest(questid):
		return {'count':0, 'create_time':currentTime()}
			
	def updateQuest(self, isNotify=False):
		newQuest = self.getAvailableQuest()
		for quest_id in newQuest:
			self.acceptQuest(quest_id, isNotify)
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
			quest.notify_add_quest(usr, questid, q)			
		self.save()
		return {'accept_quest':q}
		
	def acceptNextQuest(self, questid, questInfo, questConf):
		nextQuestid = questInfo['nextId']
		if not  questConf.has_key(nextQuestid):
			return None
		nextQuestInfo = questConf[nextQuestid]
		
		if not self.canAccept(nextQuestInfo):
			return None		
		q = quest.makeQuest(nextQuestid)
		usr = self.user
		self.current[nextQuestid] = q
		quest.notify_add_quest(usr,nextQuestid, q)
		self.save()
		return q
	
	@staticmethod
	def notify_add_quest(usr, questid, q):
		if not usr.notify.has_key('add_quest_notify'):
			usr.notify['add_quest_notify'] = {}						
		usr.notify['add_quest_notify'][questid] = q
		usr.save()
			
	@staticmethod
	def notify_finish_quest(usr, questid):
		if not usr.notify.has_key('finish_quest_notify'):
			usr.notify['finish_quest_notify'] = {}				
		usr.notify['finish_quest_notify'].append(questid)
		usr.save()
	
	@staticmethod
	def isActive(questInfo):
		"""
		is in active duration
		"""
		if not questInfo['isOpen']:
			return False		
		
		now = currentTime()
		if questInfo['beginTime']:
			if now < questInfo['beginTime']:
				return False
		if questInfo['endTime']:
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
				if q == questInfo['nextId']:
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
		del self.current[questid]
		self.finish[questid] = q
	#	quest.notify_finish_quest(usr, questid)		
		questConf = config.getConfig('quest')
		questInfo = questConf[questid]		
		newQuest = self.acceptNextQuest(questid, questInfo, questConf)	
		
		data = {}
		data['finish_quest'] = questid
		if newQuest:
			data['accept_quest'] = newQuest		
		data = drop.open(usr, questInfo['dropid'], data)		
		self.save()
		return data
	
	def updateFinishDungeonQuest(self, dungeonId, fieldId):		
		questConf = config.getConfig('quest')
		usr = self.user
		for questid in self.current.keys():
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'dungeon_id':
				if dungeonId == questInfo['finishValue'][0] and fieldId == questInfo['finishValue'][1]:
					self.current[questid]['dungeon_id'] = dungeonId
					self.current[questid]['field_id'] = fieldId
					self.current[questid]['finish'] = 1					
					quest.notify_finish_quest(usr, questid)
					#self.finish[questid] = self.current[questid]
					#del self.current[questid]
		self.save()
		
	def updateFinishNpcQuest(self):
		pass
	
	def udpateFinishChardgeQuest(self, amount):
		questConf = config.getConfig('quest')
		usr = self.user		
		for questid in self.current.keys():
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'charge_cumulate':
				if not self.current[questid].has_key('charge_count'):
					self.current[questid]['charge_count'] = 0
				self.current[questid]['charge_count'] = self.current[questid]['charge_count'] + amount
				if self.current[questid]['charge_count'] >= questInfo['finishValue']:
					self.current[questid]['finish'] = 1
					quest.notify_finish_quest(usr, questid)
					#self.finish[questid] = self.current[questid]
					#del self.current[questid]
		self.save()
		
	def updateFinishYellQuest(self):
		questConf = config.getConfig('quest')
		usr = self.user		
		for questid in self.current.keys():
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'yell_count':
				if not self.current[questid].has_key('yell_count'):
					self.current[questid]['yell_count'] = 0
				self.current[questid]['yell_count'] = self.current[questid]['yell_count'] + 1
				if self.current[questid]['yell_count'] >= questInfo['finishValue']:
					self.current[questid]['finish'] = 1
					quest.notify_finish_quest(usr, questid)
					#self.finish[questid] = self.current[questid]
					#del self.current[questid]
		self.save()
		
	def udpateFinishFriendQuest(self, usrNt):
		questConf = config.getConfig('quest')
		usr = self.user
		for questid in self.current.keys():
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'friend_count':				
				if len(usrNt.friend) >= questInfo['finishValue']:
					self.current[questid]['finish'] = 1		
					quest.notify_finish_quest(usr, questid)
					#self.finish[questid] = self.current[questid]
					#del self.current[questid]
		self.save()
	
	def updateVipItemBuyQuest(self, item_id, item_count):
		questConf = config.getConfig('quest')
		usr = self.user
		for questid in self.current.keys():
			questInfo = questConf[questid]
			q = self.current[questid]
			if questInfo['finishType'] == 'vip_item_buy_count':				
				if not q.has_key('vip_item_count'):
					self.q['vip_item_buy_count'] = 0
				q['vip_item_buy_count'] = q['vip_item_buy_count'] + 1
				if q['vip_item_buy_count'] >= questInfo['finishValue']:
					quest.notify_finish_quest(usr, questid)
					#self.finish[questid] = self.current[questid]
					#del self.current[questid]			
		self.save()
		
	def updateArenaWinQuest(self):
		questConf = config.getConfig('quest')
		usr = self.user
		for questid in self.current.keys():
			questInfo = questConf[questid]
			q = self.current[questid]
			if questInfo['finishType'] == 'arena_win_count':				
				if not q.has_key('vip_item_count'):
					self.q['arena_win_count'] = 0
				q['arena_win_count'] = q['arena_win_count'] + 1
				if q['arena_win_count'] >= questInfo['finishValue']:
					quest.notify_finish_quest(usr, questid)
					#self.finish[questid] = self.current[questid]
					#del self.current[questid]			
		self.save()
		
	def updateDungeonCountQuest(self):
		questConf = config.getConfig('quest')
		usr = self.user
		for questid in self.current.keys():
			questInfo = questConf[questid]
			q = self.current[questid]
			if questInfo['finishType'] == 'dungeon_win_count':				
				if not q.has_key('dungeon_count'):
					q['dungeon_count'] = 0
				q['dungeon_count'] = q['dungeon_count'] + 1
				if q['dungeon_count'] >= questInfo['finishValue']:
					quest.notify_finish_quest(usr, questid)
					#self.finish[questid] = self.current[questid]
					#del self.current[questid]					
		self.save()