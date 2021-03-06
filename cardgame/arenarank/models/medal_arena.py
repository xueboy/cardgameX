﻿#coding:utf-8
#!/usr/bin/env python

from gclib.DBConnection import DBConnection
from gclib.facility import facility
from game.utility.config import config

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
		新的勋章
		"""
		if medal_arena.db_add_medal(roleid, level, medalid, chipnum, cnt)	== 0:
			return {'msg':'medal_chip_not_enough'}
		return {}
	
	def delete_medal(self, roleid, level, medalid, chipnum, cnt):
		"""
		删除勋章
		"""
		return medal_arena.db_delete_medal(roleid, level, medalid, chipnum, cnt)
		
	def is_protect(self, defenceRoleid):
		"""
		是否被保护
		"""
		pt = medal_arena.db_medal_select_protect_time(defenceRoleid)
		if pt == None:
			return False
		return pt > currentTime()
		
	def add_protect_time(self, roleid, addProtectTime):
		"""
		添加保护时间
		"""
		if medal_arena.db_medal_set_protect_time(roleid, addProtectTime):
			pt = medal_arena.db_medal_select_protect_time(roleid)			
			return {'protect_time':time_to_str(pt)}
		return {'msg':'parameter_bad'}
					
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
		删除勋章
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
		寻找勋章
		"""
		conn = DBConnection.getConnection()
		sql = "SELECT distinct(medal_holder.roleid) FROM medal_holder INNER JOIN medal_level ON medal_holder.roleid = medal_level.roleid WHERE medal_level.level >= %s AND medal_holder.medalid = %s AND medal_holder.chipnum = %s AND medal_holder.roleid <> %s AND IFNULL(medal_level.shield_time, NOW()) <= NOW()  ORDER BY rand() LIMIT %s"
		res = conn.query(sql, [baseLevel, medalid, chipnum, roleid, cnt])						
		if len(res) < cnt:
			res1 = conn.query(sql, [0, medalid, chipnum, roleid, cnt])			
			if res1:					
				res = res + res1
		return list(set([n[0] for n in res]))
				
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
				return {'msg': 'medal_levelup_fail'}
		conn.commit()
		return {}
		
	@staticmethod
	def db_medal_select_protect_time(roleid):
		"""
		查询保护时间
		"""
		conn = DBConnection.getConnection()
		sql = "SELECT shield_time FROM medal_level WHERE roleid = %s"
		
		res = conn.query(sql, [roleid])
		if len(res):
			return res[0][0]			
		return time_to_str(currentTime())
		
	@staticmethod
	def db_medal_set_protect_time(roleid, addProtectTime):
		"""
		设置勋章保护时间
		"""
		conn = DBConnection.getConnection()
		sql = "UPDATE medal_level SET shield_time = IFNULL(shield_time, NOW()) + INTERVAL %s SECOND WHERE roleid = %s"
		row_count = conn.excute(sql, [roleid, addProtectTime])
		if row_count == 1:
			return True
		return False
		
			