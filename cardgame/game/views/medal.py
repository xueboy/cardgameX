#coding:utf-8
#!/usr/bin/env python

from game.routine.medal import medal


def seek_holder(request):
	medalid = request.GET['medalid']
	chipnum = request.GET['chipnum']
	
	usr = request.user	
	return medal.seek_holder(usr, medalid, chipnum)
	

def grab(request):
	grabRoleid = request.GET['grab_roleid']
	medalid = request.GET['medalid']
	chipnum = int(request.GET['chipnum'])
	usr = request.user
	
	return medal.grab(usr, grabRoleid, medalid, chipnum)
	
	
def win(request):	
	usr = request.user	
	return medal.win(usr)
	
def grab_fail(request):
	usr = request.user
	grabRoleid = request.GET['grab_roleid']

	return medal.grab_fail(usr, grabRoleid)
	
def levelup(request):
	
	usr = request.user
	medalid = request.GET['medalid']
	
	return medal.medallevelup(usr, medalid)
	
	