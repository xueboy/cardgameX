#coding:utf-8
#!/usr/bin/env python


from django.http import HttpResponse
from game.utility.config import config
from gclib.gcjson import gcjson

def enter(request):
	
	usr = request.user
	dun = usr.getDungeon()
	battleId = request.GET['battle_id']
	fieldId = request.GET['field_id']	
	dunConf = config.getConfig('dungeon')
	
	if dun.canEnterNormal(dunConf, battleId, fieldId) == True:
		reinforce = dun.getReinforcement()
		return HttpResponse(gcjson.dumps({'reinforce':reinforce}))
	return HttpResponse('not available dungeon')
	
	