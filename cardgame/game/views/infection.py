#coding:utf-8
#!/usr/bin/env python
from game.routine.infection import infection
	
def beat(request):
	battleRoleid = request.GET['battle_roleid']
	usr = request.user		
	
	damage1 = int(request.GET['damage1'])
	damage2 = int(request.GET['damage2'])
	damage3 = int(request.GET['damage3'])
	damage4 = int(request.GET['damage4'])
	damage5 = int(request.GET['damage5'])
	damage6 = int(request.GET['damage6'])

	return infection.beat(usr, battleRoleid, [damage1, damage2, damage3, damage4, damage5, damage6])
	
def call(request):
	usr = request.user
	return infection.call(usr)

def encounter(request):	
	usr = request.user
	return infection.encounter(usr)
	
def get_battle(request):
	usr = request.user
	return infection.get_battle(usr)
	
def battle_award(request):
	usr = request.user
	battleRoleid = request.GET['battle_roleid']
	createTime = int(request.GET['create_time'])
	return infection.battle_award(usr, battleRoleid, createTime)
	
def damage_ladder(request):
	usr = request.user
	return infection.damage_ladder(usr)
	
def prestige_ladder(request):
	usr = request.user
	return infection.prestige_ladder(usr)
	
def prestige_award(request):
	usr = request.user	
	return infection.prestige_award(usr)
	
def info(request):
	usr = request.user
	return infection.info(usr)
	
def reset_prestige_score(request):
	usr = request.user
	return infection.reset_prestige_score(usr)