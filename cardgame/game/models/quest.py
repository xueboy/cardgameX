﻿#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.utility import currentTime, is_same_day
from game.utility.config import config
from game.routine.drop import drop

class quest(object):
	
	def __init__(self):
		"""
		构造函数
		"""
		object.__init__(self)
		self.finish = {}
		self.current = {}
		self.drama = {}
		self.user = None
		
	def init(self):
		"""
		初始化
		"""
		pass
	
	def install(self, roleid):
		"""
		安装
		"""
		object.install(self, roleid)
	
	def getData(self):
		"""
		得到数据
		"""
		data = object.getData(self)
		data['finish'] = self.finish
		data['current'] = self.current
		data['drama'] = self.drama
		return data
		
		
	def load(self, roleid, data):
		"""
		加载
		"""
		object.load(self, roleid, data)
		self.finish = data['finish']
		self.current = data['current']
		self.drama = data['drama']
	
	def getClientData(self):
		"""
		得到客户端数据
		"""
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
			if t.has_key('finish'):
				del t['finish']
			current[q] = t
		return {'quest_current':current, 'quest_drama':self.drama}	
	
	@staticmethod
	def makeQuest(questid):
		"""
		制做任务数据
		"""
		return {'count':0, 'create_time':currentTime()}
			
	def updateQuest(self, isNotify=False):
		"""
		更新任务
		"""
		newQuest = self.getAvailableQuest()
		for quest_id in newQuest:
			self.acceptQuest(quest_id, isNotify)
		self.save()
			
				
	def getAvailableQuest(self):
		"""
		得到有效的任务
		"""
		
		questConf = config.getConfig('quest')
		usr = self.user
		newQuest = []
		for qid in questConf:			
			if questConf[qid]['type'] == 1 or questConf[qid]['type'] == 4:
				if self.commonIsAvailable(usr, qid, questConf[qid], questConf):					
					newQuest.append(qid)
			elif questConf[qid]['type'] == 2:
				if self.dayIsAvailable(usr, qid, questConf[qid], questConf):			
					newQuest.append(qid)							
		return newQuest		
		
	def commonIsAvailable(self, usr, qid, questInfo, questConf):
		"""
		是否有效的一般任务
		"""
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
				if self.finish[questid]['count'] >= questInfo['repeatCount']:
					return False
				return True
			finishQuestInfo = questConf[questid]
			if finishQuestInfo['nextId'] == qid:				
				alreadyFinishPre = True
			
		if self.current.has_key(qid):
			return False		
		if questInfo['isFirst'] or alreadyFinishPre:			
			return True
		return False
					
	def dayIsAvailable(self, usr, qid, questInfo, questConf):
		"""
		是否有效的每日任务
		"""
		if questInfo['level'] > usr.level:
			return False
		
		if not quest.isActive(questInfo):
			return False
		alreadyFinishPre = questInfo['isFirst']			
			
		if not alreadyFinishPre:
			for fqid in self.finish:
				finishQuestInfo = questConf[fqid]
				if finishQuestInfo['nextId'] == qid:
					if not is_same_day(self.finish[qid]['create_time'], currentTime()):
						return True
		return False 
			
	def acceptQuest(self, questid, isNotify=True):
		"""
		接受任务
		"""
		questConf = config.getConfig('quest')
		questInfo = questConf[questid]
		if not self.canAccept(questid, questInfo, questConf):
			return None
		
		q = None
		if self.finish.has_key(questid):
			q = self.finish[questid]
			del self.finish[questid]
		else:
			q = quest.makeQuest(questid)			
		
		usr = self.user
		if questInfo['finishType'] == 'dungeon_id':
			dun = usr.getDungeon()			
			dun.setLastDungeon(questInfo['finishValue'][0], questInfo['finishValue'][1])
			dun.notify_allow_dungeon(questInfo['finishValue'][0], questInfo['finishValue'][1])
			dun.save()
		self.current[questid] = q
		if isNotify:
			quest.notify_add_quest(usr, questid, q)
		if quest.isFinish(questid, q):
			quest.notify_finish_quest(usr, questid)
			
		self.save()
		return q
		
	def acceptNextQuest(self, questid, questInfo, questConf):
		"""
		接受下一个任务
		"""
		nextQuestid = questInfo['nextId']
		if not nextQuestid:
			return None
		if not  questConf.has_key(nextQuestid):
			return None
		return self.acceptQuest(nextQuestid)
		
	
	@staticmethod
	def notify_add_quest(usr, questid, q):
		"""
		通知添加新任务
		"""
		if not usr.notify.has_key('add_quest_notify'):
			usr.notify['add_quest_notify'] = {}						
		usr.notify['add_quest_notify'][questid] = q
		usr.save()
			
	@staticmethod
	def notify_finish_quest(usr, questid):
		"""
		通知完成任务
		"""
		if not usr.notify.has_key('finish_quest_notify'):
			usr.notify['finish_quest_notify'] = []				
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
		
	def canAccept(self, questid, questInfo, questConf):		
		"""
		是否可以接受任务
		"""
		usr = self.user
		
		if usr.level < questInfo['level']:
			return False.s
		if not self.isActive(questInfo):
			return False.s
		for qid in self.current:
			if qid == questid:
				return False
			
		if not questInfo['isFirst']:
			alreadyFinishPre = False
			for qid in self.finish:
				finishQuestInfo = questConf[qid]
				if finishQuestInfo['nextId'] == questid:
					alreadyFinishPre = True
					break
			if not alreadyFinishPre:
				return False
		return True
		
	@staticmethod
	def isFinish(questid,q):
		"""
		是否已经完成任务
		"""
		questConf = config.getConfig('quest')
		questInfo = questConf[questid]
		#if questInfo['finishType'] == 'talk_npc_id':
			#return True
		if q.has_key('finish') and q['finish'] == 1:
			return True
		return False
		
		
	def finishQuest(self, questid):
		"""
		完成任务
		"""
		if not self.current.has_key(questid):
			return {'msg':'quest_not_exist'}
		q = self.current[questid]
		usr = self.user				
		questConf = config.getConfig('quest')
		questInfo = questConf[questid]		
		
		if (not quest.isFinish(questid, q)) and (questInfo['finishType'] != 'talk_npc_id'):
			return {'msg':'quest_not_finish'}
		q['count'] = q['count'] + 1
		
		del self.current[questid]
		self.finish[questid] = q		

		newQuest = self.acceptNextQuest(questid, questInfo, questConf)	
		
		data = {}
		data['finish_quest'] = questid
		if newQuest:
			data['accept_quest'] = newQuest
		if questInfo['dropid']:
			data = drop.open(usr, questInfo['dropid'], data)		
		self.save()
		return data
	
	def updateFinishDungeonQuest(self, dungeonId, fieldId):		
		"""
		更新完成地下城任务
		"""
		questConf = config.getConfig('quest')
		usr = self.user
		haveQuestFinish = False
		for questid in self.current.keys():
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'dungeon_id':
				if dungeonId == questInfo['finishValue'][0] and fieldId == questInfo['finishValue'][1]:
					self.current[questid]['dungeon_id'] = dungeonId
					self.current[questid]['field_id'] = fieldId
					self.current[questid]['finish'] = True
					self.current[questid]['count'] = self.current[questid]['count'] + 1
					quest.notify_finish_quest(usr, questid)
					self.finish[questid] = self.current[questid]
					del self.current[questid]
					haveQuestFinish = True
		if haveQuestFinish:
			self.updateQuest(True)
			self.save()			
		
	def updateFinishNpcQuest(self):
		"""
		更新完成Npc对话任务
		"""
		pass
	
	def udpateFinishChardgeQuest(self, amount):
		"""
		更新完成充值任务
		"""
		questConf = config.getConfig('quest')
		usr = self.user
		haveQuestFinish = False
		for questid in self.current.keys():
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'charge_cumulate':
				if not self.current[questid].has_key('charge_count'):
					self.current[questid]['charge_count'] = 0
				self.current[questid]['charge_count'] = self.current[questid]['charge_count'] + amount
				if self.current[questid]['charge_count'] >= int(questInfo['finishValue']):
					self.current[questid]['finish'] = True
					self.current[questid]['count'] = self.current[questid]['count'] + 1
					quest.notify_finish_quest(usr, questid)					
					self.finish[questid] = self.current[questid]
					del self.current[questid]
					haveQuestFinish = True
		if haveQuestFinish:
			self.updateQuest(True)
			self.save()
		
	def updateFinishYellQuest(self):
		"""
		更新完成世界聊天任务
		"""
		questConf = config.getConfig('quest')
		usr = self.user
		haveQuestFinish = False
		for questid in self.current.keys():
			questInfo = questConf[questid]						
			if questInfo['finishType'] == 'yell_count':
				if not self.current[questid].has_key('yell_count'):
					self.current[questid]['yell_count'] = 0
				self.current[questid]['yell_count'] = self.current[questid]['yell_count'] + 1
				if self.current[questid]['yell_count'] >= int(questInfo['finishValue']):
					self.current[questid]['finish'] = True
					self.current[questid]['count'] = self.current[questid]['count'] + 1
					quest.notify_finish_quest(usr, questid)
					self.finish[questid] = self.current[questid]
					del self.current[questid]
					haveQuestFinish = True
		if haveQuestFinish:
			self.updateQuest(True)
			self.save()
		
	def udpateFinishFriendQuest(self, usrNt):
		"""
		更新完成好友任务
		"""
		questConf = config.getConfig('quest')
		usr = self.user
		haveQuestFinish = False
		for questid in self.current.keys():
			questInfo = questConf[questid]
			if questInfo['finishType'] == 'friend_count':				
				if len(usrNt.friend) >= int(questInfo['finishValue']):
					self.current[questid]['finish'] = True
					self.current[questid]['count'] = self.current[questid]['count'] + 1
					quest.notify_finish_quest(usr, questid)			
					self.finish[questid] = self.current[questid]
					del self.current[questid]
					haveQuestFinish = True
		if haveQuestFinish:
			self.updateQuest(True)
			self.save()
	
	def updateVipItemBuyQuest(self, item_id, item_count):
		"""
		更新完成购买vip道具任务
		"""
		questConf = config.getConfig('quest')
		usr = self.user
		haveQuestFinish = False
		for questid in self.current.keys():
			questInfo = questConf[questid]
			q = self.current[questid]
			if questInfo['finishType'] == 'vip_item_buy_count':				
				if not q.has_key('vip_item_count'):
					self.q['vip_item_buy_count'] = 0
				q['vip_item_buy_count'] = q['vip_item_buy_count'] + 1
				if q['vip_item_buy_count'] >= int(questInfo['finishValue']):
					self.current[questid]['finish'] = True
					self.current[questid]['count'] = self.current[questid]['count'] + 1
					quest.notify_finish_quest(usr, questid)
					self.finish[questid] = self.current[questid]					
					del self.current[questid]			
					haveQuestFinish = True
		if haveQuestFinish:
			self.updateQuest(True)
			self.save()
		
	def updateArenaWinQuest(self):
		"""
		更新完成竞技胜利任务
		"""
		questConf = config.getConfig('quest')
		usr = self.user
		haveQuestFinish = False
		for questid in self.current.keys():
			questInfo = questConf[questid]
			q = self.current[questid]
			if questInfo['finishType'] == 'arena_win_count':				
				if not q.has_key('vip_item_count'):
					self.q['arena_win_count'] = 0
				q['arena_win_count'] = q['arena_win_count'] + 1
				if q['arena_win_count'] >= int(questInfo['finishValue']):
					self.current[questid]['finish'] = True
					self.current[questid]['count'] = self.current[questid]['count'] + 1
					quest.notify_finish_quest(usr, questid)
					self.finish[questid] = self.current[questid]
					del self.current[questid]
				haveQuestFinish = True
		if haveQuestFinish:
			self.updateQuest(True)
			self.save()
		
	def updateDungeonCountQuest(self):
		"""
		更新完成地下城计数任务
		"""
		questConf = config.getConfig('quest')
		usr = self.user
		haveQuestFinish = False
		for questid in self.current.keys():
			questInfo = questConf[questid]
			q = self.current[questid]
			if questInfo['finishType'] == 'dungeon_win_count':				
				if not q.has_key('dungeon_count'):
					q['dungeon_count'] = 0
				q['dungeon_count'] = q['dungeon_count'] + 1
				if q['dungeon_count'] >= int(questInfo['finishValue']):
					self.current[questid]['finish'] = True
					self.current[questid]['count'] = self.current[questid]['count'] + 1
					quest.notify_finish_quest(usr, questid)
					self.finish[questid] = self.current[questid]
					del self.current[questid]					
					haveQuestFinish = True
		if haveQuestFinish:
			self.updateQuest()
			self.save()