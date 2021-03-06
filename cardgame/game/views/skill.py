﻿#coding:utf-8
#!/usr/bin/env python

from game.routine.skill import skill
from game.routine.garcha import garcha as garchaR

def levelup(request):
	"""
	技能升级
	"""
	usr = request.user
	
	dest_skillid = request.GET['dest_skill']
	ownerTeamPosition = int(request.GET['owner_team_position'])
	source_skillid = []
	source_skillid.append(request.GET['source_skill1'])
	for i in range(2, 50):
		keyname = 'source_skill' + str(i)	
		if request.GET.has_key(keyname):
			source_skillid.append(request.GET[keyname])
		
	return skill.levelup(usr, dest_skillid, ownerTeamPosition, source_skillid)
	
def install(request):
	"""
	安装技能
	"""
	usr = request.user	
	teamPosition = int(request.GET['team_position'])
	ownerTeamPosition = int(request.GET['owner_team_position'])
	slotpos = int(request.GET['sk_slot_pos'])
	stoneid = request.GET['skill']	
	return skill.install(usr, teamPosition, ownerTeamPosition, slotpos, stoneid)
	
def decompose(request):
	"""
	分解技能
	"""
	usr = request.user
	skilids = []
	
	skilids.append(request.GET['skill_id1'])
	for i in range(2, 50):
		keyname = 'skill_id' + str(i)	
		if request.GET.has_key(keyname):
			skilids.append(request.GET[keyname])
	return skill.decompose(usr, skilids)
	
def assembly(request):	
	"""
	组装技能
	"""
	usr = request.user	
	skillid = request.GET['skillid']	
	return skill.assembly(usr, skillid)
	
def garcha_skill10(request):
	"""
	技能10连抽
	"""
	usr = request.user	
	return garchaR.garcha_skill10(usr)
	
def garcha_skill(request):
	"""
	抽技能
	"""	
	usr = request.user
	nature = int(request.GET['nature'])	
	return garchaR.garcha_skill(usr, nature)