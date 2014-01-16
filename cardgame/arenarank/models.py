#coding:utf-8
#!/usr/bin/env python

from django.db import models
from gclib.facility import facility
from gclib.utility import currentTime
from game.models.user import user
from game.utility.config import config

class ladder(facility):
	def __init__(self):
		facility.__init__(self)
		self.rank = []
		self.item = {}
		
	def getData(self):
		data = {}
		data['rank'] = self.rank
		data['item'] = self.item
		return data
		
	def load(self, name, data):
		facility.load(self, name, data)
		self.rank = data['rank']
		self.item = data['item']
		
	def stand(self, roleid):		
		usr = user.get(roleid)
		
		if not usr:
			return {'msg':'user_not_exist'}	
		
		if not self.item.has_key(roleid):			
			rd = {}
			rd['roleid'] = roleid
			rd['name'] = usr.name
			rd['level'] = usr.level
			rd['last_update'] = currentTime()
			rd['score'] = 0
			rd['avatar_id'] = usr.avatar_id
			self.item[roleid] = rd
			self.rank.append(roleid)
			self.save()
			return len(self.rank) -1
		return {'msg':'arena_ladder_already_stand'}

	def show(self, roleid):		
		ls = []
		
		if self.item.has_key(roleid):
			position = self.rank.index(roleid)
			self.update(position, roleid, currentTime())
			if position < 26:
				#top 25				
				cnt = len(self.rank)
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
					if i > len(self.rank):
						break
					ls.append(self.show_floor(i))
			self.save()
			return {'ladder':ls, 'score':self.item[roleid]['score'], 'position':position}
		return {'msg':'arena_ladder_not_stand'}
		
	def show_all(self):
		uls = []
		for position in range(len(self.rank)):			
			uls.append(self.show_floor(position))					
		return uls
			
	def remove(self, roleid):
		if roleid in self.rank:
			self.rank.remove(roleid)
			del self.item[roleid]
			self.save()
			return {}
		return {'msg':'roleid_not_exsit'}
						
	def show_floor(self, position):
		
		if len(self.rank) < position:
			return {'msg':'position_invalid'}
		roleid = self.rank[position - 1]
		if not self.item.has_key(roleid):
			return {'msg' : 'roleid_not_exist'}		
		rd = self.item[roleid]
		return {'position': position, 'roleid':rd['roleid'], 'name':rd['name'], 'level':rd['level'], 'avatar_id':rd['avatar_id']}
			
	@staticmethod
	def up_floor(position, lastPosition):
		return lastPosition - int(position / 101) - 1
		
	def update(self, position, roleid, now):
		
		ladderScoreConf = config.getConfig('ladder_score')		
		if not self.item.has_key(roleid):
			return None
		item = self.item[roleid]		
		duration = now - item['last_update']		
		if duration < 60:
			return item
		score = 0
		if position < len(ladderScoreConf) - 1:
			score = ladderScoreConf[position - 1]			
		elif position < 1001:
			score = int(0.007 * position * position - 15.37 * position + 8553) / 6
		else:
			score = 16
		
		score = score * duration / 600
		item['last_update'] = now
		item['score'] = item['score'] + score
		return item
		
	def defeat(self, offenceRoleid, defenceRoleid):
		offencePosition = self.rank.index(offenceRoleid)
		defencePosition = self.rank.index(defenceRoleid)
		
		del self.rank[offencePosition]
		self.rank.insert(defencePosition, offenceRoleid)
		for i in range(defencePosition, offencePosition):
			self.update(i, self.rank[i], currentTime())
		return self.show(offenceRoleid)
		
	def convert(self, roleid, score):
		
		if roleid in self.rank:
			position = self.rank.index(roleid)			
			item = self.item[roleid]			
			if item['score'] < score:
				return {'msg':'arena_score_not_enoug'}
			item['score'] = item['score'] - score
			self.save()
			return item		
		return {'msg':'arena_ladder_not_stand'}
		
		
	def set_avatar_id(self, roleid, avatar_id):		
		if roleid in self.rank:
			position = self.rank.index(roleid)
			item = self.item[roleid]
			item['avatar_id'] = avatar_id
			self.save()
			return item
		else:
			return {'msg':'arena_ladder_not_stand'}
				
	def score(self, roleid):		
		if roleid in self.rank:
			position = self.rank.index(roleid)
			item = self.update(position, roleid, currentTime())			
			if not item:
				return {'msg':'arena_ladder_not_stand'}
			self.save()
			return {'score':item['score']}
		else:
			return {'msg':'arena_ladder_not_stand'}