#coding:utf-8
#!/usr/bin/env python

from arenarank.models.tower_ladder import tower_ladder

class tower:
	
	@staticmethod
	def stand(roleid, name, level, point, floor):
		"""
		添加排行
		"""
		tl = tower_ladder.instance()
		return tl.stand(roleid, name, level, point, floor)
		
	@staticmethod
	def show_ladder():
		"""
		显示天梯
		"""
		tl = tower_ladder.instance()
		return tl.show_ladder()