#coding:utf-8
#!/usr/bin/env python

from gclib.object import object


class dungeon(object):
	
	def __init__(self):
		self.normal_recored = []		#{battleid:'', fieldid:'',finishCount:1, enterCount:1 }		all normal dungeon recorder
		self.last_dungeon = {}			#{battleid:'', fieldid:''}  last available dungeon
		self.reinforce_list = []		#[roleid]	list
	
	def getData(self):
		data = {}
		data['normal_recrod'] = self.normal_recored
		data['last_dungeon'] = self.last_dungeon		
		return data
		
	def getClientData(self):
		return self.getData()		
		
	def canEnterNormal(self, conf, battleId, fieldId):
		for battle in dunConf:
			for field in battle['field']:
				if battle['battleId'] == battleId and field['fieldId'] == fieldId:
					return True
				if battle['battleId'] == self.last_dungeon['battleid'] and field['fieldId'] == self.last_dungeon['fieldid']:
					return False
		return False	
		
	def getVolunteer(self):
		
		usr = self.user
		friendRoleids = usr.friends.keys()
		conn = DBConnection.getConnection()
		
		sql = "SELECT * FROM user WHERE roleid NOT IN (%s) ORDER BY RAND() LIMIT 3"
		conn.excute(sql, [','.join(friendRoleids)])
		
	
	def getReinforcement(self):
		usr = self.user
		friendRoleid = usr.friends.keys()
		sql