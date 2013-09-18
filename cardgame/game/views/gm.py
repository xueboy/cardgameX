#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson
from game.utility.config import config

def add_card(request):
	card_id = request.GET['card_id']	
	usr = request.user
	inv = usr.getInventory()
	card = inv.addCard(card_id)
	if card == None:
		return HttpResponse("add card fail")
	usr.save()
	inv.save()
	
	data = {}
	data['add_card'] = card
	return HttpResponse(gcjson.dumps(data))	

def del_card(request):
	cardid = int(request.GET['id'])
	usr = request.user
	inv = usr.getInventory()	
	if inv.delCard(cardid) == 0:
		return HttpResponse("del card fail")	
	usr.save()	
	inv.save()	
	return HttpResponse(gcjson.dumps({'card':inv.getClientData}))	
		
def add_money(request):
	money = int(request.GET['money'])
	usr = request.user
	
	usr.gold = usr.gold + money
	
	usr.save()
	return HttpResponse(gcjson.dumps({'gold':usr.gold}))
		
def gain_exp_card(request):
	cardid = request.GET['card_id']
	exp = request.GET['exp']
	exp = int(exp)
	usr = request.user
	inv = usr.getInventory()
	gameConf = config.getConfig('game')
	petLevelConf = config.getConfig('pet_level')
	petConf = config.getConfig('pet')
	card = inv.getCard(cardid)
	if card != None:
		level = card['level']
		id = card['cardid']		
		star = petConf[id]['star']
		needExp = petLevelConf[str(level)][star - 1]
		levelLimit = gameConf['pet_level_limit'][star - 1]	
		while exp > needExp and levelLimit > level:
			level = level + 1
			card['level'] = level
			needExp = petLevelConf[str(level)][star - 1]
			exp = exp - needExp
			
		if card['level'] >= levelLimit:
			card['level'] = levelLimit
			card['exp'] = 0
		else:
			card['exp'] = exp
	inv.save()
	return HttpResponse(gcjson.dumps({'update_card':card}))
			
		
	