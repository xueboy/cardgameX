#coding:utf-8
#!/usr/bin/env python

from gclib.json import json
from game.utility.config import config

def add_card(request):
	card_id = request.GET['card_id']	
	usr = request.user
	inv = usr.getInventory()
	card = inv.addCard(card_id)
	if card == None:
		return {'msg':'fail_add_card'}	
	inv.save()
	
	data = {}
	data['add_card'] = card
	return data

def del_card(request):
	id = request.GET['id']
	usr = request.user
	inv = usr.getInventory()	
	if inv.delCard(id) == 0:
		return {'msg':"fail_del_card"}	
	inv.save()	
	return {'del_card':id}
		
def add_money(request):
	money = int(request.GET['money'])
	usr = request.user	
	usr.gold = usr.gold + money	
	usr.save()
	return {'gold':usr.gold}
		
def add_gem(request):
	gem = int(request.GET['gem'])
	usr = request.user
	usr.gem = usr.gem + gem
	usr.save()
	return {'gem':usr.gem}
		 
def gain_exp(request):
	exp = request.GET['exp']
	exp = int(exp)
	usr = request.user
	
	usr.gainExp(exp)
	usr.save()
	return {'exp':usr.exp, 'level':usr.level}
		 
def gain_card_exp(request):
	cardid = request.GET['card_id']
	exp = request.GET['exp']
	exp = int(exp)
	usr = request.user
	inv = usr.getInventory()
	gameConf = config.getConfig('game')
	petLevelConf = config.getConfig('pet_level')
	petConf = config.getConfig('pet')
	card = inv.getCard(cardid)
	if card:
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
	else:
		return {'msg':'card_not_exist'}
	inv.save()
	return {'update_card':card}
			
		
def add_equipment(request):
	equipid = request.GET['equipid']
	usr = request.user
	inv = usr.getInventory()
	equip = inv.addEquipment(equipid)
	if equip == None:
		return {'msg':'fail_add_equipment'}
	inv.save()
	data = {}
	data['add_equipment'] = equip
	return data
	
	
def del_equipment(request):
	id = request.GET['id']
	usr = request.user
	inv = usr.getInventory()
	if inv.delEquipment(id) == 0:
		return {'msg':'fail_del_equipment'}
	inv.save()
	return {'del_equipment':id}