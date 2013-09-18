#coding:utf-8
#!/usr/bin/env python


from django.http import HttpResponse
from game.utility.config import config
from gclib.gcjson import gcjson
from game.models.user import user

reinforce_price = [
	[20, 1],
	[50, 2],
	[100, 3],
	[150, 4],
	[200, 5]
]


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
	conf = config.getConfig('pet')
	leader = None
	reinforce = None
	if dun.curren_field['battleid'] == '' or dun.curren_field['fieldid'] == '':
		return HttpResponse(gcjson.dumps({'msg':'field_not_enter'}))
	if dun.isReinforceExist(reinforceid):
		reinforce = user.get(reinforceid)
		rei_inv = reinforce.getInventory()
		leaderid = rei_inv.team[0]	
		leader = rei_inv.getCard(leaderid)
		dun.reinforced_list.append(reinforceid)		
	dunConf = config.getConfig('dungeon')
	for battleConf in dunConf:
		if battleConf['battleId'] == dun.curren_field['battleid']:
			for fieldConf in battleConf['field']:
				if fieldConf['fieldId'] == dun.curren_field['fieldid']:
					waves = dun.arrangeWaves(fieldConf)
					staminaCost = fieldConf['stamina']
					if usr.stamina < staminaCost:
						return HttpResponse(gcjson.dumps({'msg':'not_enught_stamina'}))
					usr.stamina = usr.stamina - staminaCost							
					goldCast = 0
					if leader != None:
						start = conf[leader['id']]['star']
						level = leader['leader']
						goldCost = reinforce_price[star - 1][0] + reinforce_price[star - 1][1] * level
						if usr.gold < goldCost:
							return HttpResponse(gcjson.dumps({'msg':'not_enught_gold'}))
						usr.gold = usr.gold - goldCost
						reinforce.gold = reinforce.gold + goldCast
						reinforce.save()
						usr.save()						
													
					data = {}
					data['wave_arrages'] = waves
					data['gold'] = usr.gold
					data['stamina'] = usr.stamina
					
					return HttpResponse(gcjson.dumps(data))
		return HttpResponse(gcjson.dumps({'msg':'field_not_exist'}))
	else: 
		return HttpResponse(gcjson.dumps({'msg':'reinforce_not_exist', 'reinforce': dun.reinforces}))
			
def end(request):
	battleId = request.GET['battle_id']
	fieldId = request.GET['field_id']	
	usr = request.user
	dun = usr.getDungeon()	
	dunConf = config.getConfig('dungeon')
	
	if dun.curren_field['battleid'] != battleId or fieldId != dun.curren_field['fieldid']:
		return HttpResponse(gcjson.dumps({'msg':'dungeon_finished'}))
	
	for battleConf in dunConf:
		if battleConf['battleId'] == dun.curren_field['battleid']:
			for fieldConf in battleConf['field']:
				if fieldConf['fieldId'] == dun.curren_field['fieldid']:
					exp = fieldConf['exp']					
					usr.gainExp(exp)
					awardCard = dun.award()					
					data = {}					
					data['exp'] = usr.exp
					data['level'] = usr.level
					data['gold'] = usr.gold
					data['add_card'] = awardCard
					if dun.curren_field['battleid'] == dun.last_dungeon['battleid'] and dun.curren_field['fieldid'] == dun.last_dungeon['fieldid']:
						dun.nextField()
					dun.curren_field = {}
					data['last_dungeon'] = dun.last_dungeon
					dun.save()
					return HttpResponse(gcjson.dumps(data))
					
	return HttpResponse(gcjson.dumps({'msg':'field_not_exist'}))