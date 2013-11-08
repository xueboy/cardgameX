#coding:utf-8
#!/usr/bin/env python

from game.models.user import user
from game.routine.luckycat import luckycat


def beckon(request):
	usr = request.user
	useGem = (request.GET['use_gem'] == 'yes')	
	return luckycat.beckon(request.user, useGem)
	
def feed(request):
	targetid = request.GET['target']
	target = None
	if targetid:
		target = user.get(targetid)
		if not target:
			return {'msg':'friend_not_exist'}
	return luckycat.feed(request.user, target)
	
	
def roll_bless(request):
	usr = request.user
	return luckycat.rollBless(usr)
	
def beckon_reset(request):
	usr = request.user
	return luckycat.beckon_reset(usr)