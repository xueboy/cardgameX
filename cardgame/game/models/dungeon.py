#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from random import sample
from gclib.DBConnection import DBConnection
from gclib.gcjson import gcjson



class dungeon(object):
	
	def __init__(self):
		self.normal_recored = []		#{battleid:'', fieldid:'',finishCount:1, enterCount:1 }		all normal dungeon recorder
		self.last_dungeon = {}			#{battleid:'', fieldid:''}  last available dungeon
		self.reinforce_list = []		#[roleid]	list	
		
	

	
	def getData(self):
		data = {}
		#data['normal_recrod'] = self.normal_recored
		data['last_dungeon'] = self.last_dungeon		
		return data
		
	def getClientData(self):
		return self.getData()		
		
	def canEnterNormal(self, conf, battleId, fieldId):
		if (not self.last_dungeon.has_key('battleId')) or (not self.last_dungeon.has_key('fieldId')):
			return conf[0]['battleId'] == battleId and conf[0]['field'][0]['fieldId'] == fieldId
		
		for battle in conf:
			for field in battle['field']:
				if battle['battleId'] == battleId and field['fieldId'] == fieldId:
					return True
				if battle['battleId'] == self.last_dungeon['battleid'] and field['fieldId'] == self.last_dungeon['fieldid']:
					return False
		return False	
		
	def getVolunteer(self):		
		usr = self.user
		excludeRoleids = usr.friends.keys()
		excludeRoleids.extend(self.reinforce_list)		
		conn = DBConnection.getConnection()		
		sql = "SELECT * FROM user WHERE roleid NOT IN (%s) ORDER BY RAND() LIMIT 3"
		res = conn.query(sql, [','.join(excludeRoleids)])
		data = []
		for record in res:
			vol = usr.__class__()
			vol.load(record[0], gcjson.loads(record[2]))
			data.append(vol.getFriendData())
			print vol.getFriendData()
			print vol.roleid
			print record[0]
		return data
				
	
	def getReinforcement(self):
		usr = self.user		
		reinforce = self.getVolunteer()		
		friendRoleids = usr.friends.keys()
		for i in self.reinforce_list:
			friendRoleids.remove(i)				
		scount = 8
		if scount > len(friendRoleids):
			scount = len(friendRoleids)
		friendRoleids = sample(friendRoleids, scount)
		for i in friendRoleids:
			reinforce.append(usr.friends[i])

		
		return reinforce