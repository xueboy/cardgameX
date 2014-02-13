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
	ownerTeamPosition = int(request.GET['owner_team_position'])
	slotpos = int(request.GET['sk_slot_pos'])
	stoneid = request.GET['skill']
	
	return skill.install(usr, teamPosition, ownerTeamPosition, slotpos, stoneid)
	
def decompose(request):
	usr = request.user
	skilids = []
	
	skilids.append(request.GET['skill_id1'])
	if request.GET.has_key('skill_id2'):
		skilids.append(request.GET['skill_id2'])
	if request.GET.has_key('skill_id3'):
		skilids.append(request.GET['skill_id3'])
	if request.GET.has_key('skill_id4'):
		skilids.append(request.GET['skill_id4'])
	if request.GET.has_key('skill_id5'):
		skilids.append(request.GET['skill_id5'])
	if request.GET.has_key('skill_id6'):
		skilids.append(request.GET['skill_id6'])
	if request.GET.has_key('skill_id7'):
		skilids.append(request.GET['skill_id7'])
	if request.GET.has_key('skill_id8'):
		skilids.append(request.GET['skill_id8'])
	if request.GET.has_key('skill_id9'):
		skilids.append(request.GET['skill_id9'])
	if request.GET.has_key('skill_id10'):
		skilids.append(request.GET['skill_id10'])

	return skill.decompose(usr, skilids)
	
def assembly(request):
	
	usr = request.user
	
	skillid = request.GET['skillid']
	
	return skill.assembly(usr, skillid)