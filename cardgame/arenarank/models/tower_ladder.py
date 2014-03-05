#coding:utf-8
#!/usr/bin/env python

from gclib.facility import facility
from gclib.utility import currentTime, day_diff
from game.utility.config import config
				
class tower_ladder(facility):
	def __init__(self):
		facility.__init__(self)
		self.rank20 = []
		self.rank30 = []
		self.rank40 = []
		self.rank50 = []
		self.item = {}
		self.last_update_time = 0
		
	def getData(self):
		data = {}
		data['rank20'] = self.rank20
		data['rank30'] = self.rank30
		data['rank40'] = self.rank40
		data['rank50'] = self.rank50		
		data['item'] = self.item
		return data
		
	def load(self, name, data):
		facility.load(self, name, data)
		self.rank20 = data['rank20']
		self.rank30 = data['rank30']
		self.rank40 = data['rank40']
		self.rank50 = data['rank50']		
		self.item = data['item']
		self.last_update_time = data['last_update_time']
		
	@staticmethod
	def position_in_rank(rank, roleid):
		for (i, r) in enumerate(rank):
			if r['roleid'] == roleid:
				return i
		return -1
		
		
	def stand(self, roleid, name, level, point, floor):
		
		gameConf = config.getConfig('game')
				
		if tower_ladder.position_in_rank(self.rank20, roleid) != -1:
			self.rank20 = filter(lambda x:x['roleid']!=roleid, self.rank20)					
		if tower_ladder.position_in_rank(self.rank20, roleid) != -1:
			self.rank30 = filter(lambda x:x['roleid']!=roleid, self.rank30)		
		if tower_ladder.position_in_rank(self.rank20, roleid) != -1:
			self.rank40 = filter(lambda x:x['roleid']!=roleid, self.rank40)		
		if tower_ladder.position_in_rank(self.rank20, roleid) != -1:
			self.rank50 = filter(lambda x:x['roleid']!=roleid, self.rank50)
			
		now = currentTime()
		inLadderDayCount = 1		
		lastStandTime = now
		if roleid in self.item:
			inLadderDayCount = self.item[roleid]['in_ladder_day_count']
			lastStandTime = self.item[roleid]['last_stand_time']
			
			del self.item[roleid]
		
		if len(self.rank20) > gameConf['tower_ladder_size']:
			self.rank20 = self.rank20[0:19]				
		if len(self.rank30) > gameConf['tower_ladder_size']:
			self.rank30 = self.rank30[0:19]		
		if len(self.rank40) > gameConf['tower_ladder_size']:
			self.rank40 = self.rank40[0:19]				
		if len(self.rank50) > gameConf['tower_ladder_size']:
			self.rank50 = self.rank50[0:19]		
				
		
		dayCount = day_diff(now, lastStandTime)
		if dayCount == 1:
			inLadderDayCount = inLadderDayCount + 1
		elif dayCount > 1:
			inLadderDayCount = 1
		
		lastStandTime = now
		
		if level < 20:						
			for (i, rk) in enumerate(self.rank20):
				if point > rk['point']:
					self.rank20.insert(i, {'point':point, 'roleid':roleid})
					self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name, 'in_ladder_day_count':inLadderDayCount, 'last_stand_time' : lastStandTime, 'floor':floor}
					self.save()
					return {'position': i, 'rank_level':20}
			if len(self.rank20) < gameConf['tower_ladder_size']:
				self.rank20.append({'point':point, 'roleid':roleid})
				self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name, 'in_ladder_day_count':inLadderDayCount, 'last_stand_time' : lastStandTime, 'floor':floor}
				self.save()
				return {'position': len(self.rank20), 'rank_level':20}	
		elif level < 30:
			for (i, rk) in enumerate(self.rank30):
				if point > rk['point']:
					self.rank30.insert(i, {'point':point, 'roleid':roleid})
					self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name, 'in_ladder_day_count':inLadderDayCount, 'last_stand_time' : lastStandTime, 'floor':floor}
					self.save()
					return {'position':i, 'rank_level':30}
			if len(self.rank30) < gameConf['tower_ladder_size']:
				self.rank30.append({'point':point, 'roleid':roleid})
				self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name, 'in_ladder_day_count':inLadderDayCount, 'last_stand_time' : lastStandTime, 'floor':floor}
				self.save()
				return {'position': len(self.rank30), 'rank_level':20}	
		elif level < 40:
			for (i, rk) in enumerate(self.rank40):
				if point > rk['point']:
					self.rank40.insert(i, {'point': point, 'roleid':roleid})
					self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name, 'in_ladder_day_count':inLadderDayCount, 'last_stand_time' : lastStandTime, 'floor':floor}
					self.save()
					return {'position':i, 'rank_level':40}
			if len(self.rank40) < gameConf['tower_ladder_size']:
				self.rank40.append({'point':point, 'roleid':roleid})
				self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name, 'in_ladder_day_count':inLadderDayCount, 'last_stand_time' : lastStandTime, 'floor':floor}
				self.save()
				return {'position': len(self.rank40), 'rank_level':20}	
		else:
			for (i, rk) in enumerate(self.rank50):
				if point > rk['point']:
					self.rank50.insert(i, {'point':point, 'roleid':roleid})
					self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name, 'in_ladder_day_count':inLadderDayCount, 'last_stand_time' : lastStandTime, 'floor':floor}
					self.save()
					return {'position':i, 'rank_level':50}
			if len(self.rank50) < gameConf['tower_ladder_size']:
				self.rank50.append({'point':point, 'roleid':roleid})
				self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name, 'in_ladder_day_count':inLadderDayCount, 'last_stand_time' : lastStandTime, 'floor':floor}
				self.save()
				return {'position': len(self.rank50), 'rank_level':20}	
		return {'msg':'tower_ladder_not_stand'}
			
	def show_ladder(self):
		rank = None
				
		listLd = {}
		ls = []
		for i in range(len(self.rank20)):
			 ls.append(tower_ladder.show_position(self.rank20, self.item, i))
		listLd['20'] = ls
		ls = []
		
		for i in range(len(self.rank30)):
			 ls.append(tower_ladder.show_position(self.rank30, self.item, i))
		listLd['30'] = ls
		
		ls = []
		for i in range(len(self.rank40)):
			 ls.append(tower_ladder.show_position(self.rank40, self.item, i))
		listLd['40'] = ls
		
		ls = []
		for i in range(len(self.rank50)):
			 ls.append(tower_ladder.show_position(self.rank50, self.item, i))
		listLd['50'] = ls		
		return listLd
	
	def update_ladder(self):
		if not is_same_day(currentTime(), self.last_update_time):
			email.sendMail('3')
			self.last_stand_time = 0
			self.save()
		
	@staticmethod
	def show_position(rank, item, position):
		roleid = rank[position]['roleid']				
		return {'roleid':roleid, 'name':item[roleid]['name'], 'level':item[roleid]['level'], 'position':position, 'in_ladder_day_count': item[roleid]['in_ladder_day_count'], 'point': item[roleid]['point'], 'floor': item[roleid]['floor']}
		

		
		