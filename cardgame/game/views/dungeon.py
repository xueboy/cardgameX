#coding:utf-8
#!/usr/bin/env python


from game.utility.config import config
from gclib.json import json
from game.models.user import user
import time


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
	#	reinforce = dun.getReinforcement()
		dun.setCurrentField(battleid, fieldid)
		dun.save()
	#	return HttpResponse(gcjson.dumps({'reinforce':reinforce}))
	#return HttpResponse('field_not_available')
	
	
#def start(request):	
	#reinforceid = request.GET['reinforce_id']	
	usr = request.user
	dun = usr.getDungeon()
	conf = config.getConfig('pet')
	dunConf = config.getConfig('dungeon')	
	leader = None
	reinforce = None
	#if dun.curren_field['battleid'] == '' or dun.curren_field['fieldid'] == '':
	#	return HttpResponse(gcjson.dumps({'msg':'field_not_enter'}))		
	#if dun.isReinforceExist(reinforceid):
	#	reinforce = user.get(reinforceid)
	#	rei_inv = reinforce.getInventory()
	#	leaderid = rei_inv.team[0]	
	#	leader = rei_inv.getCard(leaderid)
	#	dun.reinforced_list.append(reinforceid)	
	
	for battleConf in dunConf:
		if battleConf['battleId'] == dun.curren_field['battleid']:
			for fieldConf in battleConf['field']:
				if fieldConf['fieldId'] == dun.curren_field['fieldid']:
					waves = dun.arrangeWaves(fieldConf)
					staminaCost = fieldConf['stamina']
					if usr.stamina < staminaCost:
						return {'msg':'not_enught_stamina'}
					usr.stamina = usr.stamina - staminaCost												
		#			goldCast = 0
		#			if leader != None:
		#				start = conf[leader['id']]['quality']
		#				level = leader['leader']
		#				goldCost = reinforce_price[quality - 1][0] + reinforce_price[quality - 1][1] * level
		#				if usr.gold < goldCost:
		#					return HttpResponse(gcjson.dumps({'msg':'not_enught_gold'}))
		#				usr.gold = usr.gold - goldCost
		#				reinforce.gold = reinforce.gold + goldCast
		#				reinforce.save()
					usr.save()												
					data = {}
					data['wave_arrages'] = waves
					data['gold'] = usr.gold
					data['stamina'] = usr.stamina
					
					return data
	return {'msg':'field_not_exist'}
	
			
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
					dun.curren_field = {'battleid':'', 'fieldid':''}
					data['last_dungeon'] = dun.last_dungeon
					dun.save()
					return data
					
	return {'msg':'field_not_exist'}