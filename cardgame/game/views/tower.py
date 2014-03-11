#coding:utf-8
#!/usr/bin/env python

from game.routine.tower import tower


def start(request):
	"""
	开始爬塔
	"""
	usr = request.user
	markup = request.GET['markup']
	markup = int(markup)	
	return tower.start(usr, markup)
	
	
def beat(request):
	"""
	击败
	"""
	usr = request.user
	difficulty = request.GET['difficulty']
	difficulty = int(difficulty)
	star = request.GET['star']
	star = int(star)
	dp = request.GET['is_drop']
	dp = int(dp)
	ehc = request.GET['enhance']
	ehc = int(ehc)	
	
	return tower.beat(usr, difficulty, star, dp, ehc)
	
def fail(request):
	"""
	爬塔失败
	"""
	usr = request.user
	return tower.fail(usr)

def show_ladder(request):
	"""
	显示排行
	"""
	usr = request.user
	return tower.show_ladder(usr)