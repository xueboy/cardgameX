#coding:utf-8
#!/usr/bin/env python

from django.db import models
from gclib.DBConnection import DBConnection
from gclib.facility import facility
from gclib.utility import currentTime, day_diff
from game.models.user import user
from game.utility.config import config

class ladder(facility):
	def __init__(self):
		"""
		构造函数
		"""
		facility.__init__(self)
		self.rank = []
		self.item = {}
		
	def getData(self):
		"""
		得到数据
		"""
		data = {}
		data['rank'] = self.rank
		data['item'] = self.item
		return data
		
	def load(self, name, data):
		"""
		加载
		"""
		facility.load(self, name, data)
		self.rank = data['rank']
		self.item = data['item']
		
	def stand(self, roleid):		
		"""
		添加排行榜
		"""
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
		"""
		显示
		"""
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
		"""
		显示合部
		"""
		uls = []
		for position in range(len(self.rank)):			
			uls.append(self.show_floor(position))					
		return uls
			
	def remove(self, roleid):
		"""
		移除
		"""
		if roleid in self.rank:
			self.rank.remove(roleid)
			del self.item[roleid]
			self.save()
			return {}
		return {'msg':'roleid_not_exsit'}
						
	def show_floor(self, position):
		"""
		显示层数
		"""
		
		if len(self.rank) < position:
			return {'msg':'position_invalid'}
		roleid = self.rank[position]
		if not self.item.has_key(roleid):
			return {'msg' : 'roleid_not_exist'}		
		rd = self.item[roleid]
		return {'position': position + 1, 'roleid':rd['roleid'], 'name':rd['name'], 'level':rd['level'], 'avatar_id':rd['avatar_id']}
			
	@staticmethod
	def up_floor(position, lastPosition):
		"""
		上一层
		"""
		return lastPosition - int(position / 101) - 1
		
	def update(self, position, roleid, now):
		"""
		更新
		"""
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
		"""
		击败
		"""
		offencePosition = self.rank.index(offenceRoleid)
		defencePosition = self.rank.index(defenceRoleid)
		
		del self.rank[offencePosition]
		self.rank.insert(defencePosition, offenceRoleid)
		for i in range(defencePosition, offencePosition):
			self.update(i, self.rank[i], currentTime())
		return self.show(offenceRoleid)
		
	def convert(self, roleid, score):
		"""
		兑换
		"""
		if roleid in self.rank:
			position = self.rank.index(roleid)			
			item = self.item[roleid]			
			if item['score'] < score:
				return {'msg':'arena_score_not_enough'}
			item['score'] = item['score'] - score
			self.save()
			return item		
		return {'msg':'arena_ladder_not_stand'}
		
		
	def set_avatar_id(self, roleid, avatar_id):		
		"""
		设置avatar id
		"""
		if roleid in self.rank:
			position = self.rank.index(roleid)
			item = self.item[roleid]
			item['avatar_id'] = avatar_id
			self.save()
			return item
		else:
			return {'msg':'arena_ladder_not_stand'}
				
	def score(self, roleid):		
		"""
		天梯分数
		"""
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
		"""
		构造函数
		"""
		facility.__init__(self)
		self.rank20 = []
		self.rank30 = []
		self.rank40 = []
		self.rank50 = []
		self.item = {}
		
	def getData(self):
		"""
		得到数据
		"""
		data = {}
		data['rank20'] = self.rank20
		data['rank30'] = self.rank30
		data['rank40'] = self.rank40
		data['rank50'] = self.rank50		
		data['item'] = self.item
		return data
		
	def load(self, name, data):
		"""
		加载
		"""
		facility.load(self, name, data)
		self.rank20 = data['rank20']
		self.rank30 = data['rank30']
		self.rank40 = data['rank40']
		self.rank50 = data['rank50']		
		self.item = data['item']
		
	@staticmethod
	def position_in_rank(rank, roleid):
		"""
		排名
		"""
		for (i, r) in enumerate(rank):
			if r['roleid'] == roleid:
				return i
		return -1
		
		
	def stand(self, roleid, name, level, point, floor):
		"""
		加入天梯
		"""
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
		"""
		显示天梯
		"""
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
			
		
	@staticmethod
	def show_position(rank, item, position):
		"""
		显示天梯位置
		"""
		roleid = rank[position]['roleid']				
		return {'roleid':roleid, 'name':item[roleid]['name'], 'level':item[roleid]['level'], 'position':position, 'in_ladder_day_count': item[roleid]['in_ladder_day_count'], 'point': item[roleid]['point'], 'floor': item[roleid]['floor']}
		
class medal_arena(facility):	
		
	def __init__(self):
		"""
		构造函数
		"""
		facility.__init__(self)
		
		
	def load(self, name, data):
		"""
		加载
		"""
		facility.load(self, name, data)
		
		
	def getData(self):
		"""
		得到数据
		"""
		data = {}		
		return data
	
	def win_medal(self, roleid, level, medalid, chipnum):		
		"""
		赢得勋章
		"""
		medal_arena.db_add_medal(roleid, level, medalid, chipnum, 1)
		return {}
				
	def lose_medal(self, roleid, medalid, chipnum):
		"""
		失去勋章
		"""
		if medal_arena.db_remove_medal(roleid, medalid, chipnum) == 1:
			return 1
		return 0		
					
		
	def role_level(self, roleid, level):
		"""
		玩家等级
		"""
		medal_arena.db_set_level(roleid, level)
		
		
	def seek_holder(self, roleid, level, medalid, chipnum):
		"""
		寻找持有者
		"""
		gameConf = config.getConfig('game')
		levelBase = level + gameConf['medal_holder_relate_level_at_last']
		if levelBase < 1:
			levelBase = 1
		holderRoleids = medal_arena.db_seek_medal_holder(roleid, medalid, chipnum, levelBase, gameConf['medal_holder_count'])		
		return {'holder':holderRoleids}
			
	def medal_levelup(self, roleid, medalid):
		"""
		勋章升级
		"""
		medalConf = config.getConfig('medal')
		medalInfo = medalConf[medalid]
		medal_arena.db_medal_levelup(roleid, medalid, medalInfo['chip'])			
		return {}	
		
	def new_medal(self, roleid, level, medalid, chipnum, cnt):		
		"""
		新勋章
		"""
		if medal_arena.db_add_medal(roleid, level, medalid, chipnum, cnt)	== 0:
			return {'msg':'medal_chip_not_enough'}
		return {}
	
	def delete_medal(self, roleid, level, medalid, chipnum, cnt):
		"""
		删除勋章
		"""
		return medal_arena.db_delete_medal(roleid, level, medalid, chipnum, cnt)
		
	@staticmethod
	def db_add_medal(roleid, level, medalid, chipnum, cnt):
		"""
		添加勋章
		"""
		conn = DBConnection.getConnection()	
		conn.star_transaction()	
		sql = "INSERT INTO medal_holder (roleid, medalid, chipnum) VALUES (%s, %s, %s)"
		for i in range(cnt):
			conn.excute_no_commit(sql, [roleid, medalid, chipnum])
		sql = "INSERT INTO medal_level (roleid, level) VALUES (%s, %s) ON DUPLICATE KEY UPDATE level = %s"
		conn.excute_no_commit(sql, [roleid, level, level])
		conn.commit()
			
	@staticmethod
	def db_remove_medal(roleid, medalid, chipnum):
		"""
		移除勋章
		"""
		conn = DBConnection.getConnection()		
		sql = "DELETE FROM medal_holder WHERE roleid = %s AND medalid = %s AND chipnum = %s LIMIT 1"		
		row_count = conn.excute(sql, [roleid, medalid, chipnum])		
		if row_count == 1:
			return 1
		return row_count
		
	@staticmethod
	def db_delete_medal(roleid, medalid, chipnum, cnt):
		"""
		删除勋章
		"""
		conn = DBConnection.getConnection()		
		sql = "DELETE FROM medal_holder WHERE roleid = %s AND medalid = %s AND chipnum = %s LIMIT %s"		
		row_count = conn.excute(sql, [roleid, medalid, chipnum, cnt])		
		if row_count == cnt:
			conn.commit()
			return row_count
		conn.rollback()
		return 0

	@staticmethod		
	def db_set_level(roleid, level):
		"""
		设置等级
		"""
		conn = DBConnection.getConnection()
		sql = "INSERT INTO medal_level (roleid, level) VALUES (%s, %s) ON DUPLICATE KEY UPDATE level = %s"
		conn.excute(sql, [roleid, level, level])
		
	@staticmethod	
	def db_seek_medal_holder(roleid, medalid, chipnum, baseLevel, cnt):
		"""
		寻找勋章持有者
		"""
		conn = DBConnection.getConnection()
		sql = "SELECT distinct(medal_holder.roleid) FROM medal_holder INNER JOIN medal_level ON medal_holder.roleid = medal_level.roleid WHERE medal_level.level >= %s AND medal_holder.medalid = %s AND medal_holder.chipnum = %s AND medal_holder.roleid <> %s ORDER BY rand() LIMIT %s"
		res = conn.query(sql, [baseLevel, medalid, chipnum, roleid, cnt])		
		if len(res) > 0:
			return res[0]
		return []	
		
	@staticmethod
	def db_medal_levelup( roleid, medalid, chipcnt):
		"""
		勋章升级
		"""
		conn = DBConnection.getConnection()
		conn.star_transaction()	
		sql = "DELETE FROM medal_holder WHERE roleid = %s AND medalid = %s AND chipnum = %s LIMIT 1"
		for i in range(chipcnt):
			rc = conn.excute_no_commit(sql, [roleid, medalid, i])
			if rc != 1:
				conn.rollback()				
				return
		conn.commit()
			
		
		