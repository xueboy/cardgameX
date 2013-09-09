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
		dun.setCurrentFiled(battleid, fieldid)
		return HttpResponse(gcjson.dumps({'reinforce':reinforce}))
	return HttpResponse('not available dungeon')
	
	
def start(request):
	reinforceid = request.GET['reinforce_id']	
	usr = request.user
	dun = usr.getDungeon()
	
	if dun.reinforeces.index(reinforceid) > -1:
		dunConf = config.getConfig('dungeon')
		for battleConf in dunConf:
			if battleConf['battleId'] == dun.currenField['battleid']:
				for fieldConf in battleConf:
					if fieldConf['fieldid'] == dun.curren_field['fieldid']:
						drops = dun.arrangeWaves(fieldConf)
						