#coding:utf-8
#!/usr/bin/env python

from django.db import models
from gclib.facility import facility
from gclib.utility import currentTime()

class ladder(facility):
	def __init__(self):
		facility.__init__(self)
		self.rank = []
		self.item = {}
		
	def stand(self, roleid, name, level):
		if not self.item.has_key(roleid):
			rd = {}
			rd['roleid'] = roleid
			rd['name'] = name
			rd['level'] = level
			rd['last_update'] = currentTime()
			rd['score'] = 0
			self.item[roleid] = rd
			self.rank.append(roleid)
			return len(self.rank) -1
		return -1

	def show(self, roleid):
		
		ls = []
		
		if self.item.has_key(roleid):
			position = self.rank.index(roleid)
			self.update(roleid, currentTime())
			if position < 26:
				#top 25				
				cnt = len(self.rank) - 1
				if cnt > 25:
					cnt = 25
				for i in range(cnt):
					ls.append(self.show_floor(i))				
			else:
				#top 10
				for i in range(10):
					ls.append(self.show_floor(i))
				#up 8
				uls = []
				lastPosition = position - 1
				uls.append(self.show_floor(lastPosition))
				lastPosition = ladder.up_floor(position, lastPosition)
				uls.append(self.show_floor(lastPosition))
				lastPosition = ladder.up_floor(position, lastPosition)
				uls.append(self.show_floor(lastPosition))
				lastPosition = ladder.up_floor(position, lastPosition)
				uls.append(self.show_floor(lastPosition))
				lastPosition = ladder.up_floor(position, lastPosition)
				uls.append(self.show_floor(lastPosition))
				lastPosition = ladder.up_floor(position, lastPosition)
				uls.append(self.show_floor(lastPosition))
				lastPosition = ladder.up_floor(position, lastPosition)
				uls.append(self.show_floor(lastPosition))				
				lastPosition = ladder.up_floor(position, lastPosition)
				uls.append(self.show_floor(lastPosition))
				uls.reverse()
				ls.extend(uls)
				#self and below 7
				for i in range(position, position + 7):
					ls.append(self.show_floor(lastPosition))					
			return ls			
		return None
						
	def show_floor(self, position):
		rd = self.item[self.rank[position]]
		return {'position': position, 'roleid':rd['roleid'], 'point':rd['point'], 'name':rd['name'], 'level':rd['level']}
			
	@staticmethod
	def up_floor(position, lastPosition):
		return lastPosition - int(position / 101) - 1
		
	def update(self, roleid, now):
		
		ladderScoreConf = config.getConfig('ladder_score')
		
		duration = now - self.item['last_update']
		
		if duration < 60:
			return
		
		position = self.rank.index(roleid)
		score = 0
		if position < len(ladderScoreConf) - 1:
			score = ladderScoreConf[position - 1]			
		elif position < 1001:
			score = int(0.007 * position * position - 15.37 * position + 8553) / 6
		else:
			score = 16
		
		score = score * duration / 600
		self.item[roleid]['point'] = self.item[roleid]['point'] + score
		
	def defeat(self, offenceRoleid, defenceRoleid):
		offencePosition = self.rank.index(offenceRoleid)
		defencePosition = self.rank.index(defenceRoleid)
		
		self.rank.remove(offencePosition)
		self.insert(defencePosition, offenceRoleid)
		for i in range(defencePosition, offencePosition):
			self.update(i, self.rank[i], currentTime())