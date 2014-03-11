#coding:utf-8
#!/usr/bin/env python

from game.models.user import user
from game.routine.luckycat import luckycat


def beckon(request):
	"""
	招财
	"""
	usr = request.user
	useGem = (request.GET['use_gem'] == 'yes')	
	return luckycat.beckon(request.user, useGem)
	
def beckon_clickonce(request):
	"""
	一键招财
	"""
	usr = request.user
	return luckycat.beckon_clickonce(usr)
	
def feed(request):
	"""
	喂养
	"""
	targetid = request.GET['target']
	target = None
	if targetid:
		target = user.get(targetid)
		if not target:
			return {'msg':'friend_not_exist'}
	return luckycat.feed(request.user, target)
	
	
def roll_bless(request):
	"""
	抽取祝福
	"""
	usr = request.user
	isUseGem = (request.GET['use_gem'] == 'yes')
	return luckycat.rollBless(usr, isUseGem)
	
def beckon_reset(request):
	"""
	重置招财
	"""
	usr = request.user
	return luckycat.beckon_reset(usr)
	
	
def agree_request(request):
	"""
	同意请求
	"""
	usr = request.user
	friendid = request.GET['friendid']	
	return luckycat.agreeFeed(usr, int(friendid))
	
def disagree_request(request):
	"""
	不同意请求
	"""
	usr = request.user
	friendid = request.GET['friendid']
	return luckycat.disagreeFeed(usr, int(friendid))
	
	
def cancel_request(request):
	"""
	取消请求
	"""
	usr = request.user
	friendid = request.GET['friendid']
	return luckycat.cancelRequest(usr, int(friendid))