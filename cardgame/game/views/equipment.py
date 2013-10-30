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
