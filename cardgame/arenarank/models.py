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
			return {'ladder':ls, 'score':self.item[roleid]['score'], 'position':position + 1}
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
		roleid = self.rank[position]
		if not self.item.has_key(roleid):
			return {'msg' : 'roleid_not_exist'}		
		rd = self.item[roleid]
		return {'position': position + 1, 'roleid':rd['roleid'], 'name':rd['name'], 'level':rd['level'], 'avatar_id':rd['avatar_id']}
			
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
				
				
class tower_ladder(facility):
	def __init__(self):
		facility.__init__(self)
		self.rank20 = []
		self.rank30 = []
		self.rank40 = []
		self.rank50 = []
		self.item = {}
		
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
		
	def stand(self, roleid, name, level, point):
		
		gameConf = config.getConfig('game')
		
		if roleid in self.rank20:
			self.rank20.remove(roleid)
		if roleid in self.rank30:
			self.rank30.remove(roleid)
		if roleid in self.rank40:
			self.rank40.remove(roleid)
		if roleid in self.rank50:
			self.rank50.remove(roleid)
		
		if roleid in self.item:
			del self.item[roleid]
		
		if len(self.rank20) > gameConf['tower_ladder_size']:
			self.rank20 = self.rank20[0:19]				
		if len(self.rank30) > gameConf['tower_ladder_size']:
			self.rank30 = self.rank30[0:19]		
		if len(self.rank40) > gameConf['tower_ladder_size']:
			self.rank40 = self.rank40[0:19]				
		if len(self.rank50) > gameConf['tower_ladder_size']:
			self.rank50 = self.rank50[0:19]		
		
		if level < 20:			
			for (rk, i) in enumerate(self.rank20):
				if point > rk['point']:
					self.rank20.insert(i, {'point':point, 'roleid':roleid})
					self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name}
					return {'position': i, 'rank_level':20}
		elif level < 30:
			for (rk, i) in enumerate(self.rank30):
				if point > rk['point']:
					self.rank30.insert(i, {'point':point, 'roleid':roleid})
					self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name}
					return {'position':i, 'rank_level':30}
		elif level < 40:
			for (rk, i) in enumerate(self.rank40):
				 if point > rk['point']:
				 	self.rank40.insert(i, {'point': point, 'roleid':roleid})
				 	self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name}
				 	return {'position':i, 'rank_level':40}
		else:
			for (rk, i) in enumerate(self.rank50):
				if point > rk['point']:
					self.rank50.insert(i, {'point':point, 'roleid':roleid})
					self.item[roleid] = {'roleid':roleid, 'level':level, 'point':point, 'name':name}
					return {'position':i, 'rank_level':50}		
		return {'msg':'tower_ladder_not_stand'}
			
	def show_ladder(self, level):
		rank = None
		
		if level < 20:
			rank = self.rank20
		elif level < 30:
			rank = self.rank30
		elif level < 40:
			rank = self.rank40
		else:
			rank = self.rank50
			
		ls = []
			
		for i in range(len(rank)):
			ls.append(tower_ladder.show_position(rank, self.item, i))
		return ls
			
		
	@staticmethod
	def show_position(rank, item, position):
		roleid = rank[position]		
		return {'roleid':roleid, 'name':item[roleid]['name'], 'level':item[roleid]['level'], 'position':position}
		
class medal_arena(facility):	
		
	def __init__(self):
		facility.__init__(self)
		self.medal_hold = {}
		self.medal_level = {}
	
	def win_medal(self, roleid, level, medalid, chipnum):
		
			
		self.medal_level[roleid] = level
			
		if not self.medal_hold.has_key(medalid):
			medalConf = config.getConfig('medal')			
			self.medal_hold[medalid] = [] * medalConf['chip']			
			self.medal_hold[medalid][chipnum].append(roleid)
		else:
			if roleid not in self.medal_hold[medalid][chipnum]:
				medal_hold[medalid][chipnum].append(roleid)
		return {}
				
	def lose_medal(self, roleid, medalid, chipnum):		
		if roleid in self.medal_hold[medalid][chipnum]:
			self.medal_hold[medalid][chipnum].remove(roleid)
			return 1
		return 0			
		
	def role_level(self, roleid, level):
		self.medal_level[roleid] = level	
		
	def seek_holder(self, level, medalid, chipnum):
		holder = []
		
		gameConf = config.getConfig('game')
		
		if not self.medal_hold.has_key(medalid):
			return {'msg':'medal_holder_exhaust'}
		
		levelBase = level - gameConf['medal_holder_level_at_last']
		
		if levelBase < 1:
			levelBase = 1
		
		self.medal_hold[chipnum] = random.shuffle(self.medal_hold[chipnum])			
		for r in self.medal_hold:
			if self.medal_level[r] <= levelBase:
				continue
			if r not in holder:
				holder.append(m)
				if len(holder) >= gameConf['medal_holder_count']:
					break					
		return {'holder':holder}
			
	def medal_levelup(self, roleid, medalid):
		medalConf = config.getConfig('medal')
		medalInfo = medalConf[medalid]
		
		for cp in range(medalInfo['chip']):
			if roleid in self.medal_hold[medalid][cp]:
			 self.medal_hold[medalid][cp].remove(roleid)
		
		return {}