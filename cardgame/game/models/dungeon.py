#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from random import sample
from gclib.DBConnection import DBConnection
from game.utility.config import config
from gclib.utility import randint, currentTime, hit, is_same_day
from game.routine.drop import drop
from game.routine.vip import vip
import time
import random




class dungeon(object):
	
	def __init__(self):
		object.__init__(self)
		self.roleid = 0
		self.normal_recored = {}		#{battleid:'', fieldid:'',finishCount:1, enterCount:1 }		all normal dungeon recorder
		self.last_dungeon = {'battleid':'', 'fieldid':''}			#{battleid:'', fieldid:''}  last available dungeon
		self.reinforced_list = []		#[roleid]	list
		self.last_reinforce_time = 0
		self.curren_field = {'battleid':'', 'fieldid':''}
		self.reinforces = None
		self.curren_field_waves = []
		self.daily_recored = {}
		self.daily_recored_last_time = 0		
		self.fatigue = 0
		#self.allow_list = {}
		self.user = None
		
	def init(self):		
		conf = config.getConfig('dungeon')
		self.last_dungeon['battleid'] = ''
		self.last_dungeon['fieldid'] = ''
	
	def install(self, roleid):
		object.install(self, roleid)
	
	def getData(self):
		data = object.getData(self)
		data['normal_recored'] = self.normal_recored
		data['last_dungeon'] = self.last_dungeon		
		data['reinforced_list'] = self.reinforced_list
		data['last_reinforce_time'] = self.last_reinforce_time
		data['curren_field'] = self.curren_field
		data['reinforces'] = self.reinforces
		data['curren_field_waves'] = self.curren_field_waves
		data['daily_recored'] = self.daily_recored
		data['daily_recored_last_time'] = self.daily_recored_last_time
		data['fatigue'] = self.fatigue
		#data['allow_list'] = self.allow_list
		return data
		
	def load(self, roleid, data):
		object.load(self, roleid, data)
		if isinstance(data['normal_recored'], list):
			self.normal_recored = {}
		else:
			self.normal_recored = data['normal_recored']
		self.last_dungeon = data['last_dungeon']
		self.reinforced_list = data['reinforced_list']
		self.last_reinforce_time = data['last_reinforce_time']
		self.curren_field = data['curren_field']
		self.reinforces = data['reinforces']
		self.daily_recored = data['daily_recored']
		self.daily_recored_last_time = data['daily_recored_last_time']
		#self.allow_list = data['allow_list']
		self.curren_field_waves = data['curren_field_waves']
		self.fatigue = data['fatigue']
		
	def getClientData(self):
		data = {}
		data['last_dungeon'] = self.last_dungeon
		#data['fatigue'] = self.fatigue
		data['daily_recored'] = self.daily_recored
		data['normal_recored'] = self.normal_recored
		#data['curren_field_waves'] = self.curren_field_waves
		#data['allow_list'] = self.allow_list
		return data
		
	def updateReinforce(self):
		now = currentTime()
		tmLast = time.localtime(self.last_reinforce_time)
		tmNow = time.localtime(now)
		if tmLast.tm_year != tmNow.tm_year or tmLast.tm_mon != tmNow.tm_mon or tmLast.tm_mday != tmNow.tm_mday:
			self.reinforced_list = []
			last_reinforce_time = currentTime()
	
	def setLastDungeon(self, battleid, fieldid):
		self.last_dungeon['battleid'] = battleid
		self.last_dungeon['fieldid'] = fieldid
	
	def canEnterNormal(self, conf, battleid, fieldid):
		if (not self.last_dungeon.has_key('battleid')) or (not self.last_dungeon.has_key('fieldid')):
			return False
		if not self.last_dungeon['battleid']:
			return False
		if not self.last_dungeon['fieldid']:
			return False
		
		for battle in conf:
			for field in battle['field']:
				#if battle['battleId'] == battleid and field['fieldId'] == fieldid:
				#	return True
				if battle['battleId'] == self.last_dungeon['battleid'] and field['fieldId'] == self.last_dungeon['fieldid']:
					return True
		return False
		#if not self.allow_list.has_key(battleid):
		#	return False
		#if fieldid not in self.allow_list[battleid]:
		#	return False
		#return True	
		
	def getVolunteer(self):		
		usr = self.user
		excludeRoleids = usr.friends.keys()
		excludeRoleids.extend(self.reinforced_list)		
		conn = DBConnection.getConnection()
		sql = ''
		if len(excludeRoleids) == 0:
			sql = "SELECT * FROM user WHERE roleid ORDER BY RAND() LIMIT 3"
		else:
			sql = "SELECT * FROM user WHERE roleid NOT IN (" + ','.join(excludeRoleids) + ") ORDER BY RAND() LIMIT 3"
		res = conn.query(sql, [])
		data = []
		for record in res:
			if record[0] == usr.roleid:
				continue
			vol = usr.__class__()
			vol.load(record[0], gcjson.loads(record[2]))
			data.append(vol.getFriendData())
		return data
		
	def dailyRecored(self, battleid, fieldid):
		
		if not is_same_day(self.daily_recored_last_time, currentTime()):
			self.daily_recored = {}
			self.daily_recored_last_time = currentTime()
			self.fatigue = 0
		
		if not self.daily_recored.has_key(battleid):
			self.daily_recored[battleid] = {}
		if not self.daily_recored[battleid].has_key(fieldid):
			self.daily_recored[battleid][fieldid] = 0
		self.daily_recored[battleid][fieldid] = self.daily_recored[battleid][fieldid] + 1
		self.daily_recored_last_time = currentTime()
		return self.daily_recored[battleid][fieldid]
	
	def normalRecordEnter(self, battleid, fieldid):
		if not self.normal_recored.has_key(battleid):
			self.normal_recored[battleid] = {}
		if not self.normal_recored[battleid].has_key(fieldid):
			self.normal_recored[battleid][fieldid] = dungeon.make_field_info()			
		
	@staticmethod
	def make_field_info():
		return {'finish':False, 'star':0}
	
	def normalRecordEnd(self, battleid, fieldid, star):		
		print self.normal_recored
		self.normal_recored[battleid][fieldid]['finish'] = True
		if self.normal_recored[battleid][fieldid]['star'] < star:
			self.normal_recored[battleid][fieldid]['star'] = star
				
	
	def getFieldConf(self, battleid, fieldid):
		for battle in conf:
			if battle['battleId'] == dungeonid:
				for field in battle['field']:
					if field['fieldId'] == fieldid:
						return field
		return None
		
	def dailyCount(self, dungeonid, fieldid):
		if not self.daily_recored.has_key(dungeonid):
			return 0;
		if not self.daily_recored[dungeonid].has_key(fieldid):
			return 0;
		return self.daily_recored[dungeonid][fieldid]
		
	
	def getReinforcement(self):
		usr = self.user
		self.updateReinforce()
		reinforces = self.getVolunteer()		
		friendRoleids = usr.friends.keys()
		for i in self.reinforced_list:
			if friendRoleids.count(i) > 0:
				friendRoleids.remove(i)				
		scount = 8
		if scount > len(friendRoleids):
			scount = len(friendRoleids)
		friendRoleids = sample(friendRoleids, scount)
		for i in friendRoleids:
			reinforces.append(usr.friends[i])
		self.reinforces = reinforces
		return reinforces
		
	def setCurrentField(self, battleid, fieldid):
		self.curren_field = {'battleid':battleid, 'fieldid':fieldid}	
		
	def setReinforce(self, ls):
		self.reinforeces = ls
		
	def isReinforceExist(self, reinforceid):
		if reinforceid == '':
			return False
		for reinforce in self.reinforces:
			if reinforce['roleid'] == int(reinforceid):
				return True
		return False
		
	def arrangeWaves(self, field):
		waves = {}		
		for wave in field['wave']:
			i = 0
			cnt = 0
			if sum(wave['count_prob']) != 0 and sum(wave['count']):
				cnt = wave['count'][hit(wave['count_prob'])]			
			monsters = random.sample(wave['monster'], cnt)
			
			monsters.extend(wave['boss'])
			
			waveData = []
			for monsterid in monsters:				
				dropData = {}
				dropid =  wave['drop'][monsterid]
				
				if dropid:					
					dropData = drop.roll(dropid, dropData)				
					
				waveData.append({'monsterid':monsterid, 'drop':dropData})
			i = i + 1
			waves['wave' + str(i)] = waveData
		self.curren_field_waves = waves
		self.save()
		return waves
		
	def award(self):
		usr = self.user
		inv = usr.getInventory()		
		waves = self.curren_field_waves
		awd = {}
		for wave in waves:
			for monsterDrop in waves[wave]:
				dropData = monsterDrop['drop']				
				awd = drop.do_award(usr, dropData, awd)				
					
		self.curren_field_waves = []
		usr.save()
		inv.save()
		awd = drop.makeData(awd, {})
		return awd
	
	def nextField(self):
		dunConf = config.getConfig('dungeon')
		for battleConf in dunConf:
			if battleConf['battleId'] == self.curren_field['battleid']:
				for fieldConf in battleConf['field']:
					if fieldConf['fieldId'] == self.curren_field['fieldid']:
						i = battleConf['field'].index(fieldConf)
						if len (battleConf['field']) > (i + 1):
							self.last_dungeon['fieldid'] = battleConf['field'][i + 1]['fieldId']
						else:
							i = dunConf.index(battleConf)
							if len(dunConf) > (i + 1):
								self.last_dungeon['battleid'] = dunConf[i + 1]['battleId']
								self.last_dungeon['fieldid'] = dunConf[i + 1]['field'][0]['fieldId']

	def notify_allow_dungeon(self, battleid, fieldid):
		usr = self.user
	
		if not usr.notify.has_key('dungeon_allow'):
			usr.notify['dungeon_allow'] = {}
			
		usr.notify['dungeon_allow']['battleid'] = battleid
		usr.notify['dungeon_allow']['fieldid'] = fieldid		
		usr.save()
		
		
	def sweep(self, battleid, fieldid, cnt):
		
		if not self.normal_recored.has_key(battleid):
			return {'msg' : 'dungeon_not_finished'}
		if not self.normal_recored[battleid].has_key(fieldid):
			return {'msg' : 'dungeon_not_finished'}
		
		usr = self.user
		gameConf = config.getConfig('game')
		if (not vip.canDungeonSweep(usr)) and (gameConf['dungeon_vip0_sweep_star'] > self.normal_recored[battleid][fieldid]):
			return {'msg':'dungeon_sweep_not_allowed'}
		self.curren_field = {'battleid':'', 'fieldid':''}	
		dunConf = config.getConfig('dungeon')
		resultData = {}
		resultData['sweep'] = []
		for battleConf in dunConf:
			if battleConf['battleId'] == battleid:
				for fieldConf in battleConf['field']:
					if fieldConf['fieldId'] == fieldid:					
						
						staminaCost = fieldConf['stamina']
						if usr.stamina < staminaCost:
							return {'msg':'stamina_not_enough'}
						if fieldConf['dayCount'] == self.daily_recored[battleid][fieldid]:
							return {'msg':'dungeon_max_count'}
						if fieldConf['dayCount'] < (self.daily_recored[battleid][fieldid] + cnt):
							cnt = fieldConf['dayCount'] - self.daily_recored[battleid][fieldid]							
						qt = usr.getQuest()
						for i in range(cnt):
							waves = self.arrangeWaves(fieldConf)
							staminaCost = fieldConf['stamina']
							if usr.stamina < staminaCost:
								break
							usr.stamina = usr.stamina - staminaCost
							self.daily_recored[battleid][fieldid] = self.daily_recored[battleid][fieldid] + 1
							waves = self.arrangeWaves(fieldConf)
							exp = fieldConf['exp']					
							usr.gainExp(exp)
							data = {}
							if fieldConf['dropid']:
								awd = {}					
								awd = drop.open(usr, fieldConf['dropid'], awd)					
								data = self.award()
								data = drop.makeData(awd, data)
						
							data['add_exp'] = exp							
							
							resultData['sweep'].append(data)
							#if dun.curren_field['battleid'] == dun.last_dungeon['battleid'] and dun.curren_field['fieldid'] == dun.last_dungeon['fieldid']:
							#	dun.nextField()
												
							#data['last_dungeon'] = dun.last_dungeon							
							qt.updateDungeonCountQuest()
							qt.updateFinishDungeonQuest(battleid, fieldid)
							
		resultData['stamina'] = usr.stamina
		resultData['exp'] = usr.exp
		resultData['level'] = usr.level
		resultData['gold'] = usr.gold
		return resultData