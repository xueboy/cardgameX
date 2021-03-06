#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.cache import cache
from gclib.json import json
from arenarank.models.network_ladder import network_ladder
from arenarank.models.infection_arena import infection_arena
from arenarank.routine.arena import arena
from arenarank.routine.medal import medal
from arenarank.routine.infection import infection
from arenarank.routine.tower import tower

def show_ladder(request):
	"""
	显示天梯
	"""
	roleid = request.REQUEST['roleid']
	return HttpResponse(json.dumps(arena.show(roleid)))
	
def stand_ladder(request):
	"""
	站上天梯
	"""
	roleid = request.REQUEST['roleid']	
	return HttpResponse(json.dumps(arena.stand(roleid)))
	
def defeat(request):	
	"""
	击败
	"""
	offenceRoleid = request.REQUEST['offence_roleid']
	defenceRoleid = request.REQUEST['defence_roleid']	
	return HttpResponse(json.dumps(arena.defeat(offenceRoleid, defenceRoleid)))
	
def convert(request):
	"""
	兑换
	"""
	roleid = request.REQUEST['roleid']
	score = int(request.REQUEST['score'])	
	return HttpResponse(json.dumps(arena.convert(roleid, score)))
	
def show_all(request):	
	"""
	显示全部
	"""
	return HttpResponse(json.dumps(arena.show_all()))	

def remove(request):
	"""
	移除
	"""
	roleid = request.REQUEST['roleid']	
	return HttpResponse(json.dumps(arena.remove(roleid)))
	
def set_avatar_id(request):
	"""
	设置avatar_id
	"""
	roleid = request.REQUEST['roleid']
	avatar_id = request.REQUEST['avatar_id']	
	return HttpResponse(json.dumps(arena.set_avatar_id(roleid, avatar_id)))
	
	
def score(request):
	"""
	积分
	"""
	roleid = request.REQUEST['roleid']	
	return HttpResponse(json.dumps(arena.score(roleid)))
	
def award_score(request):
	"""
	积分奖励
	"""
	roleid = request.REQUEST['roleid']
	awardScore = request.REQUEST['award_score']
	ld = ladder.instance()
	return HttpResponse(json.dumps(ld.award_score(roleid, int(awardScore))))
	
def tower_stand(request):
	"""
	站上塔
	"""
	roleid = request.REQUEST['roleid']
	level = int(request.REQUEST['level'])
	point = int(request.REQUEST['point'])
	name = request.REQUEST['name']
	floor = int(request.REQUEST['floor'])	
	return HttpResponse(json.dumps(tower.stand(roleid, name, level, point, floor)))
	
def tower_show(request):	
	"""
	显示武神塔排名
	"""
	return HttpResponse(json.dumps(tower.show_ladder()))
	
	
def grab_medal(request):
	"""
	抢夺勋章
	"""
	offenceRoleid = request.REQUEST['offenceRoleid']
	defenceRoleid = request.REQUEST['defenceRoleid']	
	level = int(request.REQUEST['level'])
	medalid = request.REQUEST['medalid']
	chipnum = int(request.REQUEST['chipnum'])	
	return HttpResponse(json.dumps(medal.grab_medal(offenceRoleid, defenceRoleid, level, medalid, chipnum)))
	
def seek_holder(request):
	"""
	寻找持有者
	"""
	roleid = int(request.REQUEST['roleid'])
	level = int(request.REQUEST['level'])
	medalid = request.REQUEST['medalid']
	chipnum = int(request.REQUEST['chipnum'])	
	return HttpResponse(json.dumps(medal.seek_holder(roleid, level, medalid, chipnum)))
	
	
def medal_levelup(request):	
	"""
	勋章升级
	"""
	roleid = request.REQUEST['roleid']
	medalid = request.REQUEST['medalid']	
	return HttpResponse(json.dumps(medal.medal_levelup(roleid, medalid)))
	
def new_medal(request):
	"""
	新勋章
	"""
	roleid = request.REQUEST['roleid']
	medalid = request.REQUEST['medalid']
	chipnum = int(request.REQUEST['chipnum'])
	level = int(request.REQUEST['level'])
	cnt = int(request.REQUEST['count'])	
	return HttpResponse(json.dumps(medal.new_medal(roleid, level, medalid, chipnum, cnt)))
	
def delete_medal(request):
	"""
	删除勋章
	"""
	roleid = request.REQUEST['roleid']
	medalid = request.REQUEST['medalid']
	level = request.REQUEST['level']
	chipnum = request.REQUEST['chipnum']
	cnt = request.REQUEST['count']	
	ld = medal_arena.instance()
	return HttpResponse(json.dumps(ld.delete_medal(roleid, int(level), medalid, int(chipnum), int(cnt))))
	
def try_grab(request):
	"""
	抢夺勋章
	"""
	defenceRoleid = request.REQUEST['defence_roleid']		
	return HttpResponse(json.dumps(medal.try_grab(defenceRoleidd)))
	
def add_protect_time(request):	
	"""
	添加保护时间
	"""
	roleid = request.REQUEST['roleid']
	second = int(request.REQUEST['add_second'])		
	return HttpResponse(json.dumps(medal.add_protect_time(roleid, second)))
	
def network_gift(request):
	"""
	礼物
	"""
	sendRoleid = request.REQUEST['send_roleid']	
	receiveRoleid = request.REQUEST['receive_roleid']
	ld = network_ladder.instance()
	return HttpResponse(json.dumps(ld.gift(sendRoleid, receiveRoleid)))
	
def network_range(request):
	"""
	得到排行榜
	"""
	
	tp = request.REQUEST['type']
	roleid = request.REQUEST['roleid']
	begin = int(request.REQUEST['begin'])
	end = int(request.REQUEST['end'])
	ld = network_ladder.instance()
	if tp == 'charm':
		return HttpResponse(json.dumps(ld.get_charm_range(roleid, begin, end)))
	elif tp == 'tuhao':
		return HttpResponse(json.dumps(ld.get_tuhao_range(roleid, begin, end)))
		
def infection_encounter(request):
	"""
	遭遇战斗
	"""
	roleid = request.REQUEST['roleid']	
	rolename = request.REQUEST['rolename']	
	return HttpResponse(json.dumps(infection.encounter(roleid, rolename)))
	
def infection_beat(request):
	"""
	击败
	"""
	roleid = request.REQUEST['roleid']
	rolelevel = request.REQUEST['rolelevel']
	rolename = request.REQUEST['rolename']
	battleRoleid = request.REQUEST['battle_roleid']
	damage1 = int(request.REQUEST['damage1'])
	damage2 = int(request.REQUEST['damage2'])
	damage3 = int(request.REQUEST['damage3'])
	damage4 = int(request.REQUEST['damage4'])
	damage5 = int(request.REQUEST['damage5'])
	damage6 = int(request.REQUEST['damage6'])

	return HttpResponse(json.dumps(infection.beat(roleid, rolelevel, rolename, battleRoleid, [damage1, damage2, damage3, damage4, damage5, damage6])))
	
def infection_call_relief(request):	
	"""
	呼叫援军
	"""
	roleid = request.REQUEST['roleid']
	i = 1
	idkeyname = 'friendid' + str(i)
	namekeynam = 'friendname' + str(i)
	friendid = []
	while request.REQUEST.has_key(idkeyname):
		friendid.append((request.REQUEST[idkeyname], request.REQUEST[namekeynam]))		
		i = i + 1
		idkeyname = 'friendid' + str(i)
		namekeynam = 'friendname' + str(i)
	ia = infection_arena.instance()
	return HttpResponse(json.dumps(ia.call_relief(roleid, friendid)))
	
def infection_get_battle(request):
	"""
	得到战斗
	"""
	roleid = request.REQUEST['roleid']	
	return HttpResponse(json.dumps(infection.get_battle(roleid)))
	
def infection_battle_award(request):
	"""
	得到战斗收益
	"""
	roleid = request.REQUEST['roleid']
	battleRoleid = request.REQUEST['battle_roleid']
	create_time = int(request.REQUEST['create_time'])	
	return HttpResponse(json.dumps(infection.get_battle_award(roleid, battleRoleid, create_time)))
	
def infection_prestige_award(request):
	"""
	声望奖励
	"""
	roleid = request.REQUEST['roleid']
	rolelevel = int(request.REQUEST['rolelevel'])
	return HttpResponse(json.dumps(infection.prestige_award(roleid, rolelevel)))
	
def infection_ladder(request):
	"""
	感染天梯
	"""
	tp = request.REQUEST['type']
	rolelevel = int(request.REQUEST['rolelevel'])	
	return HttpResponse(json.dumps(infection.ladder(tp, rolelevel)))
		
def infection_info(request):
	"""
	感染信息
	"""
	roleid = request.REQUEST['roleid']
	return HttpResponse(json.dumps(infection.user_info(roleid)))
	
def infection_reset_prestige_score(request):
	"""
	重置感染分数
	"""
	roleid = request.REQUEST['roleid']
	return HttpResponse(json.dumps(infection.reset_prestige_score(roleid)))