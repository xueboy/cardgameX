﻿#coding:utf-8
#!/usr/bin/env python

from game.models.inventory import inventory
from game.routine.equipment import equipment


def strengthen(request):
	
	id = request.GET['id']
	isUseGem = request.GET['is_use_gem']
	usr = request.user
	isUseGem = isUseGem == 'yes'
	ownerTeamPosition = int(request.GET['owner_team_position'])
	return equipment.strengthen(usr, id, ownerTeamPosition, isUseGem)	
	
def strengthen_reset(request):
	usr = request.user	
	return equipment.strengthen_reset(usr)

def equip(request):
	
	teamPosition = int(request.GET['team_position'])
	equipmentid = request.GET['equipment_id']	
	ownerTeamPosition = int(request.GET['owner_team_position'])
	usr = request.user
	return equipment.equip(usr, teamPosition, ownerTeamPosition, equipmentid)
	
def sell(request):
	
	equipmentid = [request.GET['equipment_id1']]	
	for i in range(2, 50):
		keyname = 'equipment_id' + str(i)
		if request.GET.has_key(keyname):
			equipmentid.append(request.GET[keyname])
		else:
			break
	usr = request.user
	return equipment.sell(usr, equipmentid)
	
	
def degradation(request):
	equipmentid = request.GET['id']
	usr = request.user
	return equipment.degradation(usr, equipmentid)
	

def assembly(request):
	
	usr = request.user
	
	equipmentid = request.GET['equipmentid']
	
	return equipment.assembly(usr, equipmentid)