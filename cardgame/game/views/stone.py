﻿#coding:utf-8
#!/usr/bin/env python

from game.routine.stone import stone

def visit(request):
	"""
	访问
	"""
	
	usr = request.user
	level = int(request.GET['vlevel'])
	return stone.visit(usr, level)
	
def visit_gem(request):
	"""
	钻石访问
	"""
	usr = request.user
	level = int(request.GET['vlevel'])
	return stone.visit_gem(usr, level)
		
def visit_clickonece(request):
	"""
	一键访问
	"""
	usr = request.user
	return stone.visit_clickonce(usr, 10)	
	
def levelup(request):
	"""
	宝石升级
	"""
	usr = request.user	
	dest_stoneid = request.GET['dest_stone']
	teamPosition = int(request.GET['team_position'])
	source_stoneid = []
	i = 1	
	source_key = 'source_stone' + str(i)	
	while request.GET.has_key(source_key):
		source_stoneid.append(request.GET[source_key])
		i = i + 1
		source_key = 'source_stone' + str(i)
	
	return stone.levelup(usr, teamPosition, dest_stoneid, source_stoneid)

	
def install(request):
	"""
	安装宝石
	"""
	usr = request.user
	
	teamPosition = int(request.GET['team_position'])
	ownerTeamPosition = int(request.GET['owner_team_position'])
	slotpos = int(request.GET['st_slot_pos'])
	stoneid = request.GET['stone']
		
	return stone.install(usr, teamPosition, ownerTeamPosition, slotpos, stoneid)