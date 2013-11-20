#coding:utf-8
#!/usr/bin/env python

from game.routine.skill import skill

def levelup(request):
	usr = request.user
	
	dest_skillid = request.GET['dest_skill']
	source_skillid = []
	source_skillid.append(request.GET['source_skill1'])
	if request.GET.has_key('source_skill2'):
		source_skillid.append(request.GET['source_skill2'])
	if request.GET.has_key('source_skill3'):
		source_skillid.append(request.GET['source_skill3'])
	if request.GET.has_key('source_skill4'):
		source_skillid.append(request.GET['source_skill4'])
	if request.GET.has_key('source_skill5'):
		source_skillid.append(request.GET['source_skill5'])
	if request.GET.has_key('source_skill6'):
		source_skillid.append(request.GET['source_skill6'])
		
	return skill.levelup(usr, dest_skillid, source_skillid)
	
def install(request):
	
	usr = request.user
	
	teamPosition = int(request.GET['team_position'])
	slotpos = int(request.GET['sk_slot_pos'])
	stoneid = request.GET['skill']
	
	return skill.install(usr, teamPosition, slotpos, stoneid)