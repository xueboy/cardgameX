#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.cache import cache
from gclib.json import json
from arenarank.models import ladder, tower_ladder, medal_arena

def show_ladder(request):	
			
	roleid = request.REQUEST['roleid']
	ld = ladder.instance()
	return HttpResponse(json.dumps( ld.show(roleid)))	
	
def stand_ladder(request):
	
	roleid = request.REQUEST['roleid']
	ld = ladder.instance()	
	
	return HttpResponse(json.dumps(ld.stand(roleid)))
	
def defeat(request):
	
	offenceRoleid = request.REQUEST['offence_roleid']
	defenceRoleid = request.REQUEST['defence_roleid']	
	ld = ladder.instance()
	
	return HttpResponse(json.dumps(ld.defeat(offenceRoleid, defenceRoleid)))
	
def convert(request):
	roleid = request.REQUEST['roleid']
	score = request.REQUEST['score']	
	ld = ladder.instance()
	return HttpResponse(json.dumps(ld.convert(roleid, int(score))))
	
def show_all(request):
	ld = ladder.instance()
	return HttpResponse(json.dumps(ld.show_all()))
	

def remove(request):
	roleid = request.REQUEST['roleid']
	ld = ladder.instance()
	ld.remove(roleid)
	return HttpResponse(json.dumps(ld.show_all()))
	
def set_avatar_id(request):
	roleid = request.REQUEST['roleid']
	avatar_id = request.REQUEST['avatar_id']
	ld = ladder.instance()
	return HttpResponse(json.dumps(ld.set_avatar_id(roleid, avatar_id)))
	
	
def score(request):
	roleid = request.REQUEST['roleid']
	ld = ladder.instance()
	return HttpResponse(json.dumps(ld.score(roleid)))
	
def award_score(request):
	roleid = request.REQUEST['roleid']
	awardScore = request.REQUEST['award_score']
	ld = ladder.instance()
	return HttpResponse(json.dumps(ld.award_score(roleid, int(awardScore))))
	
def tower_stand(request):
	roleid = request.REQUEST['roleid']
	level = request.REQUEST['level']
	point = request.REQUEST['point']
	name = request.REQUEST['name']
	floor = request.REQUEST['floor']
	ld = tower_ladder.instance()
	return HttpResponse(json.dumps(ld.stand(roleid, name, int(level), int(point), int(floor))))
	
def tower_show(request):
		
	ld = tower_ladder.instance()
	return HttpResponse(json.dumps(ld.show_ladder()))
	
	
def grab_medal(request):
	
	offenceRoleid = request.REQUEST['offenceRoleid']
	deffenceRoleid = request.REQUEST['deffenceRoleid']
	
	level = int(request.REQUEST['level'])
	medalid = request.REQUEST['medalid']
	chipnum = int(request.REQUEST['chipnum'])
	
	ld = medal_arena.instance()
	if ld.is_protect().s():
		return {'msg':'arene_grab_in_protect'}
	if ld.lose_medal(offenceRoleid, medalid, chipnum) == 0:
		return HttpResponse(json.dumps({'msg':'medal_not_exist'}))
	
	return HttpResponse(json.dumps(ld.win_medal(deffenceRoleid, level, medalid, chipnum)))
	
	
def lose_medal(request):
	
	roleid = request.REQUEST['roleid']
	medalid = request.REQUEST['medalid']
	chipnum = int(request.REQUEST['chipnum'])
	
	ld = medal_arena.instance()
	return HttpResponse(json.dumps(ld.lose_medal(roleid, medalid, chipnum)))
	
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
	return HttpResponse(json.dumps(ld.is_protect(defenceRoleid)))