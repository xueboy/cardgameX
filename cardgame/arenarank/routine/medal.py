﻿#coding:utf-8
#!/usr/bin/env python

from arenarank.models.medal_arena import medal_arena

class medal:
		
	@staticmethod
	def grab_medal(offenceRoleid, defenceRoleid, level, medalid, chipnum):
		"""
		夺取勋章
		"""
		ma = medal_arena.instance()
		ld = medal_arena.instance()
		if ma.is_protect(defenceRoleid):
			return {'msg':'arene_grab_in_protect'}
		if ma.lose_medal(defenceRoleid, medalid, chipnum) == 0:
			return {'msg':'medal_not_exist'}	
		return ma.win_medal(offenceRoleid, level, medalid, chipnum)	
	
	@staticmethod
	def seek_holder(roleid ,level, medalid, chipnum):
		"""
		寻找持有者
		"""
		ma = medal_arena.instance()
		return ma.seek_holder(roleid, level, medalid, chipnum)
		
	@staticmethod
	def medal_levelup(roleid, medalid):		
		"""
		勋章升级
		"""
		ma = medal_arena.instance()
		return ma.medal_levelup(roleid, medalid)
		
	@staticmethod
	def new_medal(roleid, level, medalid ,chipnum, cnt):
		"""
		新勋章
		"""
		ma = medal_arena.instance()
		return ma.new_medal(roleid, level, medalid ,chipnum, cnt)
		
	@staticmethod
	def delete_medal(roleid, level, medalid, chipnum, cnt):
		"""
		删除勋章
		"""
		ma = medal_arena.instance()
		return ma.delete_medal(roleid, level, medalid, chipnum, cnt)
		
	@staticmethod
	def try_grab(defenceRoleid):
		"""
		抢夺
		"""
		ma = medal_arena.instance()
		return {'protect': ma.is_protect(defenceRoleid)}
		
	@staticmethod
	def add_protect_time(roleid, second):
		"""
		添加保护时间
		"""
		ma = medal.instance()
		return ma.add_protect_time(roleid, second)
		
	