#coding:utf-8
#!/usr/bin/env python

from game.models.inventory import inventory
from game.routine.equipment import equipment


def strengthen(request):
	
	id = request.GET['id']
	isUseGem = request.GET['is_use_gem']
	usr = request.user
	isUseGem = isUseGem == 'yes'
	return equipment.strengthen(usr, id, isUseGem)	

def equip(request):
	
	teamPosition = int(request.GET['team_position'])
	equipmentid = request.GET['equipment_id']	
	usr = request.user
	return equipment.equip(usr, teamPosition, equipmentid)
	
def sell(request):
	equipmentid = request.GET['equipment_id']	
	usr = request.user
	return equipment.sell(usr, equipmentid)