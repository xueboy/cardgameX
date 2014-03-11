#coding:utf-8
#!/usr/bin/env python

from gclib.facility import facility
from game.utility.config import config
from game.models.user import user

class network_ladder(facility):
	
	
	def __init__(self):
		"""
		构造函数
		"""
		facility.__init__(self)
		self.user = {}
		self.charm_ladder = []
		self.tuhao_ladder = []
		
	def getData(self):
		"""
		得到数据
		"""		
		data = {}
		data['user'] = self.user
		data['charm_ladder'] = self.charm_ladder
		data['tuhao_ladder'] = self.tuhao_ladder
		return data
		
	def load(self, name, data):
		"""
		加载
		"""
		facility.load(self, name, data)
		self.user = data['user']
		self.charm_ladder = data['charm_ladder']
		self.tuhao_ladder = data['tuhao_ladder']
	
	def gift(self, sendRoleid, receiveRoleid):
		"""
		送礼
		"""
		sendUsr = user.get(sendRoleid)
		receiveUsr = user.get(receiveRoleid)
		
		if (not sendUsr) or (not receiveUsr):
			return {'msg':'usr_not_exist'}
				
		sendUsrNw = sendUsr.getNetwork()
		receiveUsrNw = receiveUsr.getNetwork()
		
		gameConf = config.getConfig('game')				
		
		if receiveRoleid in self.charm_ladder:
			self.charm_ladder = filter(lambda x: x != receiveRoleid, self.charm_ladder)
				
		if sendRoleid in self.tuhao_ladder:
			self.tuhao_ladder = filter(lambda x: x != sendRoleid, self.tuhao_ladder)		
		
		tuhao_position = -1
		for (i, rid) in enumerate(self.tuhao_ladder):			
			if receiveUsrNw.tuhao > self.user[rid]['tuhao']:
				tuhao_position = i
				break
		if len(self.tuhao_ladder) < gameConf['gift_ladder_max_size'] and tuhao_position < 0:
			tuhao_position = len(self.tuhao_ladder)		
		if tuhao_position >= 0:
			self.tuhao_ladder.insert(tuhao_position, sendRoleid)
	
		charm_position = -1
		
		for (i, rid) in enumerate(self.charm_ladder):			
			if receiveUsrNw.charm > self.user[rid]['charm']:
				charm_position = i
				break
		if len(self.charm_ladder) < gameConf['gift_ladder_max_size'] and charm_position < 0:
			charm_position = len(self.charm_ladder)
				
		if charm_position >= 0:
			self.charm_ladder.insert(charm_position, receiveRoleid)

		if tuhao_position >= 0:
			self.user[sendRoleid] = {'roleid':sendRoleid, 'charm':sendUsrNw.charm, 'tuhao': sendUsrNw.tuhao, 'charm': receiveUsrNw.charm, 'name': sendUsr.name, 'level':sendUsr.level}
		if charm_position >= 0:
			self.user[receiveRoleid] = {'roleid':receiveRoleid, 'charm':receiveUsrNw.charm, 'tuhao': receiveUsrNw.tuhao, 'charm': receiveUsrNw.charm, 'name': receiveUsr.name, 'level':receiveUsr.level}
			
		self.update_ladder(gameConf)		
		self.save()
		
		return {'charm_user_position': charm_position, 'tuhao_user_position': tuhao_position}
		
	def update_ladder(self, gameConf):		
		"""
		更新天梯
		"""
		cnt = len(self.charm_ladder) - gameConf['gift_ladder_max_size']
		if cnt > 0:
			for i in range(cnt, gameConf['gift_ladder_max_size'] + cnt):
				if self.charm[i] not in self.tuhao:
					del self.user[self.charm[i]]
			self.charm = self.charm[gameConf['gift_ladder_max_size']]
			
		cnt = len(self.tuhao_ladder) - gameConf['gift_ladder_max_size']
		if cnt > 0:
			for i in range(cnt, gameConf['gift_ladder_max_size'] + cnt):
				if self.tuhao[i] not in self.charm:
					del self.user[self.tuhao[i]]
			self.tuhao = self.tuhao[gameConf['gift_ladder_max_size']]
						
	def get_charm_range(self, roleid, begin, end):
		"""
		得到魅力天梯
		"""		
		data = {'ladder':[]}
		
		ladder_size = len(self.charm_ladder)
		if ladder_size == 0:
			return data
		
		if begin >= ladder_size:
			return {'msg':'ladder_out_of_range'}
		if end >= ladder_size:
			end = ladder_size
			
		for i in range(begin, end):
			item = self.user[self.charm_ladder[i]]
			data['ladder'].append({'position': i, 'roleid': item['roleid'], 'charm': item['charm'], 'name':item['name']})
		if roleid in self.charm_ladder:
			data['position'] = self.charm_ladder.index(roleid) + 1
		return data
		
	def get_tuhao_range(self, roleid, begin, end):
		"""
		得到土豪天梯
		"""		
		data = {'ladder':[]}
		
		ladder_size = len(self.tuhao_ladder)
		if ladder_size == 0:
			return data
		if begin >= ladder_size:
			return {'msg':'ladder_out_of_range'}
		if end >= ladder_size:
			end = ladder_size
			
		for i in range(begin, end):
			item = self.user[self.tuhao_ladder[i]]
			data['ladder'].append({'position': i, 'roleid': item['roleid'], 'tuhao': item['tuhao'], 'name':item['name']})			
		if roleid in self.tuhao_ladder:
			data['position'] = self.tuhao_ladder.index(roleid) + 1
		return data	
		
