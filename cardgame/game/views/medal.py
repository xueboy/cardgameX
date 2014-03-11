#coding:utf-8
#!/usr/bin/env python

from game.routine.medal import medal


def seek_holder(request):
	"""
	寻找持有者
	"""
	medalid = request.GET['medalid']
	chipnum = request.GET['chipnum']
	
	usr = request.user	
	return medal.seek_holder(usr, medalid, chipnum)
	

def grab(request):
	"""
	抢夺
	"""
	grabRoleid = request.GET['grab_roleid']
	medalid = request.GET['medalid']
	chipnum = int(request.GET['chipnum'])
	usr = request.user
	
	return medal.grab(usr, grabRoleid, medalid, chipnum)
	
	
def win(request):	
	"""
	赢
	"""
	usr = request.user	
	return medal.win(usr)
	
def grab_fail(request):
	"""
	输
	"""
	usr = request.user
	grabRoleid = request.GET['grab_roleid']

	return medal.grab_fail(usr, grabRoleid)
	
def levelup(request):
	"""
	勋章升级
	"""
	usr = request.user
	medalid = request.GET['medalid']
	
	return medal.medallevelup(usr, medalid)
	
	