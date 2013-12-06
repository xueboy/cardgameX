#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from cardgame.settings import ARENE_SERVER
from game.models.user import user

def show_ladder(request):	
	usr = request.user	
	return curl.url(ARENE_SERVER +  '/arena/show_ladder/', None, {'roleid':str(usr.roleid)})
		
def stand_ladder(request):
	usr = request.user
	return curl.url(ARENE_SERVER +  '/arena/stand_ladder/', None, {'roleid':str(usr.roleid)})
		
		
def challenge(request):
	usr = request.user
	defenceRoleid = request.GET['defence_roleid']
	defenceRole = user.get(defenceRoleid)
	
	usr.arena['challenge_roleid'] = defenceRole
	usr.save()
	
	return {'defence':defenceRole.getBattleData()}
		
def defeate(request):
	usr = request.user
	
	if usr.arena.has_key('challenge_roleid'):
		curl.url(ARENE_SERVER +  '/arena/stand_ladder/', None, {'roleid':str(usr.roleid)})
	
		