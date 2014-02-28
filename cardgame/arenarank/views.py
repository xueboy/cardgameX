#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.cache import cache
from gclib.json import json
from arenarank.models.models import tower_ladder, medal_arena
from arenarank.models.network_ladder import network_ladder
from arenarank.models.infection_arena import infection_arena
from arenarank.routine.arena import arena

def show_ladder(request):				
	roleid = request.REQUEST['roleid']
	return HttpResponse(json.dumps(arena.show_ladder(roleid)))
	
def stand_ladder(request):	
	roleid = request.REQUEST['roleid']	
	return HttpResponse(json.dumps(arena.stand(roleid)))
	
def defeat(request):	
	offenceRoleid = request.REQUEST['offence_roleid']
	defenceRoleid = request.REQUEST['defence_roleid']	
	return HttpResponse(json.dumps(arena.defeat(offenceRoleid, defenceRoleid)))
	
def convert(request):
	roleid = request.REQUEST['roleid']
	score = int(request.REQUEST['score'])	
	return HttpResponse(json.dumps(arena.convert(roleid, score)))
	
def show_all(request):	
	return HttpResponse(json.dumps(arena.show_all()))	

def remove(request):
	roleid = request.REQUEST['roleid']	
	return HttpResponse(json.dumps(arena.remove(roleid)))
	
def set_avatar_id(request):
	roleid = request.REQUEST['roleid']
	avatar_id = request.REQUEST['avatar_id']	
	return HttpResponse(json.dumps(arena.set_avatar_id(roleid, avatar_id)))
	
	
def score(request):
	roleid = request.REQUEST['roleid']	
	return HttpResponse(json.dumps(arena.score(roleid)))
	
def award_score(request):
	roleid = request.REQUEST['roleid']
	awardScore = request.REQUEST['award_score']
	ld = ladder.instance()
	return HttpResponse(json.dumps(ld.award_score(roleid, int(awardScore))))
	
def tower_stand(request):
	roleid = request.REQUEST['roleid']
	level = int(request.REQUEST['level'])
	point = int(request.REQUEST['point'])
	name = request.REQUEST['name']
	floor = int(request.REQUEST['floor'])	
	return HttpResponse(json.dumps(arena.stand(roleid, name, level, point, floor)))
	
def tower_show(request):	
	return HttpResponse(json.dumps(arena.show_ladder()))
	
	
def grab_medal(request):
	
	offenceRoleid = request.REQUEST['offenceRoleid']
	deffenceRoleid = request.REQUEST['deffenceRoleid']
	
	level = int(request.REQUEST['level'])
	medalid = request.REQUEST['medalid']
	chipnum = int(request.REQUEST['chipnum'])
	
	ld = medal_arena.instance()
	if ld.is_protect(deffenceRoleid):
		return HttpResponse(json.dumps({'msg':'arene_grab_in_protect'}))
	if ld.lose_medal(deffenceRoleid, medalid, chipnum) == 0:
		return HttpResponse(json.dumps({'msg':'medal_not_exist'}))
	
	return HttpResponse(json.dumps(ld.win_medal(offenceRoleid, level, medalid, chipnum)))
	
	
#def lose_medal(request):
#	
#	roleid = request.REQUEST['roleid']
#	medalid = request.REQUEST['medalid']
#	chipnum = int(request.REQUEST['chipnum'])
#	
#	ld = medal_arena.instance()
#	return HttpResponse(json.dumps(ld.lose_medal(roleid, medalid, chipnum)))
	
def seek_holder(request):
	
	roleid = int(request.REQUEST['roleid'])
	level = int(request.REQUEST['level'])
	medalid = request.REQUEST['medalid']
	chipnum = int(request.REQUEST['chipnum'])
	ld = medal_arena.instance()
	return HttpResponse(json.dumps(ld.seek_holder(roleid, level, medalid, chipnum)))
	
	
def medal_levelup(request):
	
	roleid = request.REQUEST['roleid']
	medalid = request.REQUEST['medalid']	
	ld = medal_arena.instance()
	return HttpResponse(json.dumps(ld.medal_levelup(roleid, medalid)))
	
def new_medal(request):
	roleid = request.REQUEST['roleid']
	medalid = request.REQUEST['medalid']
	chipnum = request.REQUEST['chipnum']
	level = request.REQUEST['level']
	cnt = request.REQUEST['count']
	
	ld = medal_arena.instance()
	return HttpResponse(json.dumps(ld.new_medal(roleid, int(level), medalid, int(chipnum), int(cnt))))
	
def delete_medal(request):
	roleid = request.REQUEST['roleid']
	medalid = request.REQUEST['medalid']
	level = request.REQUEST['level']
	chipnum = request.REQUEST['chipnum']
	cnt = request.REQUEST['count']
	
	ld = medal_arena.instance()
	return HttpResponse(json.dumps(ld.delete_medal(roleid, int(level), medalid, int(chipnum), int(cnt))))
	
def try_grab(request):
	defenceRoleid = request.REQUEST['defence_roleid']	
	ld = medal_arena.instance()
	return HttpResponse(json.dumps({'protect' : ld.is_protect(defenceRoleid)}))
	
def add_protect_time(request):	
	roleid = request.REQUEST['roleid']
	second = int(request.REQUEST['add_second'])	
	ld = medal_arena.instance()
	return HttpResponse(json.dumps(ld.add_protect_time(roleid, second)))
	
def network_gift(request):
	sendRoleid = request.REQUEST['send_roleid']	
	receiveRoleid = request.REQUEST['receive_roleid']
	ld = network_ladder.instance()
	return HttpResponse(json.dumps(ld.gift(sendRoleid, receiveRoleid)))
	
def network_range(request):
	tp = request.REQUEST['type']
	roleid = request.REQUEST['roleid']
	begin = int(request.REQUEST['begin'])
	end = int(request.REQUEST['end'])
	ld = network_ladder.instance()
	if tp == 'charm':
		return HttpResponse(json.dumps(ld.get_charm_range(roleid, begin, end)))
	elif tp == 'tuhao':
		return HttpResponse(json.dumps(ld.get_tuhao_range(roleid, begin, end)))
		
def infection_encounter(request):
	roleid = request.REQUEST['roleid']	
	rolename = request.REQUEST['rolename']
	ia = infection_arena.instance()	
	return HttpResponse(json.dumps(ia.encounter(roleid, rolename)))
	
def infection_beat(request):
	roleid = request.REQUEST['roleid']
	rolelevel = request.REQUEST['rolelevel']
	rolename = request.REQUEST['rolename']
	battleRoleid = request.REQUEST['battle_roleid']
	damage1 = int(request.REQUEST['damage1'])
	damage2 = int(request.REQUEST['damage2'])
	damage3 = int(request.REQUEST['damage3'])
	damage4 = int(request.REQUEST['damage4'])
	damage5 = int(request.REQUEST['damage5'])
	damage6 = int(request.REQUEST['damage6'])
	
	ia = infection_arena.instance()
	return HttpResponse(json.dumps(ia.beat(roleid, rolelevel, rolename, battleRoleid, [damage1, damage2, damage3, damage4, damage5, damage6])))
	
def infection_call_relief(request):	
	roleid = request.REQUEST['roleid']
	i = 1
	idkeyname = 'friendid' + str(i)
	namekeynam = 'friendname' + str(i)
	friendid = []
	while request.REQUEST.has_key(idkeyname):
		friendid.append((request.REQUEST[idkeyname], request.REQUEST[namekeynam]))		
		i = i + 1
		idkeyname = 'friendid' + str(i)
		namekeynam = 'friendname' + str(i)
	ia = infection_arena.instance()
	return HttpResponse(json.dumps(ia.call_relief(roleid, friendid)))
	
def infection_get_battle(request):
	roleid = request.REQUEST['roleid']	
	ia = infection_arena.instance()
	return HttpResponse(json.dumps(ia.get_infection_battle(roleid)))
	
def infection_award(request):
	roleid = request.REQUEST['roleid']
	battleRoleid = request.REQUEST['battle_roleid']
	create_time = int(request.REQUEST['create_time'])
	ia = infection_arena.instance()
	return HttpResponse(json.dumps(ia.get_battle_award(roleid, battleRoleid, create_time)))
	
def infection_ladder(request):
	tp = request.REQUEST['type']
	rolelevel = int(request.REQUEST['rolelevel'])
	ia = infection_arena.instance()
	if tp == 'damage':
		return HttpResponse(json.dumps(ia.damdage_ladder_list(rolelevel)))
	elif tp == 'prestige':
		return HttpResponse(json.dumps(ia.prestige_ladder_list(rolelevel)))
	return HttpResponse(json.dumps({'msg':'infection_bad_ladder_type'}))
	
