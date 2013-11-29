#coding:utf-8
#!/usr/bin/env python

from gclib.json import json
from game.utility.config import config
from game.routine.pet import pet

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
		
def add_gold(request):
	gold = int(request.GET['gold'])
	usr = request.user	
	usr.gold = usr.gold + gold
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
	cardid = request.GET['card']
	exp = int(request.GET['exp'])	
	usr = request.user
	inv = usr.getInventory()
	gameConf = config.getConfig('game')
	petLevelConf = config.getConfig('pet_level')
	petConf = config.getConfig('pet')
	card = inv.getCard(cardid)
	if not card:
		return {'msg':'card_not_exist'}
	pet.gainExp(card, exp, petConf, petLevelConf, gameConf)				
	inv.save()
	return {'update_card':card}
			
		
def add_equipment(request):
	equipid = request.GET['equipment_id']
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
		
def add_trp(request):
	trp = int(request.GET['trp'])
	usr = request.user	
	usr.trp = usr.trp + trp
	usr.save()
	return {'trp':usr.trp}
		
def add_stone(request):
	stoneid = request.GET['stone']	
	usr = request.user	
	inv = usr.getInventory()
	stone = inv.addStone(stoneid)
	inv.save()
	return {'add_stone':stone}
		
def add_skill(request):
	skillid = request.GET['skill']	
	usr = request.user	
	inv = usr.getInventory()
	skill = inv.addSkill(skillid)
	inv.save()
	return {'add_skill':skill}