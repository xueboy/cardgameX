#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.cache import cache
from gclib.json import json
from arenarank.models import ladder

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