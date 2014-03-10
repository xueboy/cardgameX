#coding:utf-8
#!/usr/bin/env python

from arenarank.models.models import ladder

class arena:
	
	@staticmethod
	def show(roleid):
		"""
		显示天梯
		"""
		ld = ladder.instance()
		return ld.show(str(roleid))
		
	@staticmethod
	def stand(roleid):		
		"""
		加入天梯
		"""
		ld = ladder.instance()		
		return ld.stand(str(roleid))
		
	@staticmethod
	def defeat(offenceRoleid, defenceRoleid):
		"""
		击败
		"""
		ld = ladder.instance()
		return ld.defeat(str(offenceRoleid), str(defenceRoleid))
		
	@staticmethod
	def convert(roleid, score):
		"""
		兑换奖励
		"""
		ld = ladder.instance()
		return ld.convert(str(roleid), score)
		
	@staticmethod
	def show_all():
		"""
		显示全部
		"""
		ld = ladder.instance()
		return ld.show_all()
		
	@staticmethod
	def remove(roleid):
		"""
		从天梯上移除
		"""
		ld = ladder.instance()
		ld.remove(roleid)
		return ld.show_all()
		
	@staticmethod
	def set_avatar_id(roleid, avatar_id):
		"""
		设置avatar_id
		"""
		ld = ladder.instance()
		return ld.set_avatar_id(str(roleid), avatar_id)
		
	@staticmethod
	def score(roleid):
		"""
		天梯分数
		"""
		ld = ladder.instance()
		return ld.score(str(roleid))
		
	@staticmethod
	def award_score(roleid, awardScore):
		"""
		天梯奖励分数
		"""
		ld = ladder.instance()
		return ld.award_score(str(roleid), int(awardScore))
	
	@staticmethod
	def tower_stand(roleid, level, point, name, floor):
		"""
		站上天梯
		"""
		ld = ladder.instance()
		return ld.tower_stand(str(roleid), level, point ,name, floor)
		
	@staticmethod
	def show_ladder():
		"""
		显示天梯
		"""
		ld = ladder.instance()
		return ld.show_ladder()