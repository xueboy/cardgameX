#coding:utf-8
#!/usr/bin/env python


from django.http import HttpResponse
from game.utility.config import config
from gclib.gcjson import gcjson

def enter(request):
	
	usr = request.user
	dun = usr.getDungeon()
	battleid = request.GET['battle_id']
	fieldid = request.GET['field_id']	
	dunConf = config.getConfig('dungeon')
	
	if dun.canEnterNormal(dunConf, battleid, fieldid) == True:
		reinforce = dun.getReinforcement()
		dun.setCurrentField(battleid, fieldid)
		dun.save()
		return HttpResponse(gcjson.dumps({'reinforce':reinforce}))
	return HttpResponse('not available dungeon')
	
	
def start(request):
	reinforceid = request.GET['reinforce_id']	
	usr = request.user
	dun = usr.getDungeon()
	ls = dun.reinforces
	if dun.isReinforceExist(reinforceid):
		dunConf = config.getConfig('dungeon')
		for battleConf in dunConf:
			if battleConf['battleId'] == dun.curren_field['battleid']:
				for fieldConf in battleConf['field']:
					if fieldConf['fieldId'] == dun.curren_field['fieldid']:
						waves = dun.arrangeWaves(fieldConf)
						return HttpResponse(gcjson.dumps(waves))
		return HttpResponse(gcjson.dumps({'msg':'field not exist'}))
	else: 
		return HttpResponse(gcjson.dumps({'msg':'reinforce not exist', 'reinforce': dun.reinforces}))
			
