#coding:utf-8
#!/usr/bin/env python

from game.routine.stone import stone

def visit(request):
	
	usr = request.user
	level = int(request.GET['vlevel'])
	return stone.visit(usr, level)
	
def visit_gem(request):
	
	usr = request.user
	level = int(request.GET['vlevel'])
	return stone.visit_gem(usr, level)
	
	
def visit_clickonece(request):
	usr = request.user
	return stone.visit_clickonce(usr, 10)
	
	
def levelup(request):
	
	usr = request.user
	
	dest_stoneid = request.GET['dest_stone']	
	source_stoneid = []	
	i = 1	
	source_key = 'source_stone' + str(i)
	
	while request.GET.has_key(source_key):
		source_stoneid.append(request.GET[source_key])
		i = i + 1
		source_key = 'source_stone' + str(i)
	
	return stone.levelup(usr, dest_stoneid, source_stoneid)


	
def install(request):
	
	usr = request.user
	
	teamPosition = int(request.GET['team_position'])
	slotpos = int(request.GET['st_slot_pos'])
	stoneid = request.GET['stone']
		
	return stone.install(usr, teamPosition, slotpos, stoneid)