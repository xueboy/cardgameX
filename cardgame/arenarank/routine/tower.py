#coding:utf-8
#!/usr/bin/env python

from arenarank.models.tower_ladder import tower_ladder

class tower:
	
	@staticmethod
	def stand(roleid, name, level, point, floor):		
		tl = tower_ladder.instance()
		return tl.stand(self, roleid, name, level, point, floor)
		
	@staticmethod
	def show_ladder():
		tl = tower_ladder.instance()
		return tl.show_ladder()