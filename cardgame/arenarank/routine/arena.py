#coding:utf-8
#!/usr/bin/env python

from arenarank.models.models import ladder

class arena:
	
	@staticmethod
	def show(roleid):
		ld = ladder.instance()
		return ld.show(roleid)
		
	@staticmethod
	def stand(roleid):		
		ld = ladder.instance()		
		return ld.stand(roleid)
		
	@staticmethod
	def defeat(offenceRoleid, defenceRoleid):
		ld = ladder.instance()
		return ld.defeat(offenceRoleid, defenceRoleid)
		
	@staticmethod
	def convert(roleid, score):
		ld = ladder.instance()
		return ld.convert(roleid, score)
		
	@staticmethod
	def show_all():
		ld = ladder.instance()
		return ld.show_all()
		
	@staticmethod
	def remove(roleid):
		ld = ladder.instance()
		ld.remove(roleid)
		return ld.show_all()
		
	@staticmethod
	def set_avatar_id(roleid, avatar_id):
		ld = ladder.instance()
		return ld.set_avatar_id(roleid, avatar_id)
		
	@staticmethod
	def score(roleid):
		ld = ladder.instance()
		return ld.score(roleid)
		
	@staticmethod
	def award_score(roleid, awardScore):
		ld = ladder.instance()
		return ld.award_score(roleid, int(awardScore))
	
	@staticmethod
	def tower_stand(roleid, level, point, name, floor):
		ld = ladder.instance()
		return ld.tower_stand(roleid, level, point ,name, floor)
		
	@staticmethod
	def show():
		ld = ladder.instance(roleid)
		return ld.show(roleid)