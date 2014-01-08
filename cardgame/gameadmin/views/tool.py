#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from game.models.user import user
from gclib.utility import currentTime
from django.shortcuts import render
from game.routine.arena import arena
from gclib.json import json
from gameadmin.routine.gm import gm
	
def tool_create_player(request):
	if request.method == 'POST':
		levelf = request.POST['levelf']
		levelt = request.POST['levelt']
		cnt = int(request.POST['count'])
		main_card_dropid = request.POST['main_card_dropid']
		other_card_dropid = request.POST['other_card_dropid']
		card_levelf = request.POST['card_levelf']
		card_levelt = request.POST['card_levelt']
		equip_strenght_levelf = request.POST['equip_strenght_levelf']
		equip_strenght_levelt = request.POST['equip_strenght_levelt']
		skill_levelf = request.POST['skill_levelf']
		skill_levelt = request.POST['skill_levelt']
		stone_levelf = request.POST['stone_levelf']
		stone_levelt = request.POST['stone_levelt']
		stand_ladder = request.POST.has_key('stand_ladder')
		
		for i in range(cnt):
			usr = user()					
			usr.init(None)
			usr.last_login = currentTime()
			usr.name = 'testRobot'
			usr.gender = 'female'
			usr.avatar = '1'
			usr.install(0)
			
			usr.saveRoleId()
			usr.onInit()
			usr.save()
			if stand_ladder:
				res = arena.stand_ladder(usr)	
				if isinstance(res, str):
					res = json.loads(res)
					if res.has_key('msg'):
						return HttpResponse('error:' + str(i) + ':' + str(usr.roleid) + res['msg'])		
	ld = arena.show_all()	
	return render(request, 'tool.html', {'ladder':ld})
		
def tool_ladder_remove(request):
	if request.method == 'POST':		
		optid = request.POST['optid']
		operator = request.POST['operator']
		if operator == 'remove':
			arena.remove(optid)		
	ld = arena.show_all()	
	print ld
	return render(request, 'arena_tool.html', {'ladder':ld})
		
def gm_tool(request):
	if request.method == 'POST':
		pass
	
		
	
	return render(request, 'profile.html', {})
	
def gm_tool_profile_find(request):
	data = {}
	if request.method == 'POST':		
		roleid = request.POST['tfRoleid']
		if roleid:
			usr = user.get(roleid)
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)		
		
	return render(request, 'profile.html', data)
	
def gm_tool_set_profile(request):
	
	data = {}
	if request.method == 'POST':
		operator = request.POST['operator']
		roleid = request.POST['roleid']		
		if operator == 'exp':
			value = request.POST['tfExp']
			if value == '':
				return HttpResponse('经验为空')
			usr = user.get(roleid)
			if not usr:
				return HttpResponse('玩家不存在')
			usr.gainExp(int(value))
			usr.save()
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)
		if operator == 'gold':
			value = request.POST['tfGold']
			if value == '':
				return HttpResponse('金钱为空')
			usr = user.get(roleid)
			if not usr:
				return HttpResponse('玩家不存在')
			usr.gold = int(value)
			usr.save()
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)
		if operator == 'gem':
			value = request.POST['tfGem']
			if value == '':
				return HttpResponse('宝石为空')
			usr = user.get(roleid)
			if not usr:
				return HttpResponse('玩家不存在')
			usr.gem = int(value)
			usr.save()
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)
		if operator == 'stamina':
			value = request.POST['tfStamina']
			if value == '':
				return HttpResponse('体力为空')
			usr = user.get(roleid)
			if not usr:
				return HttpResponse('玩家不存在')
			usr.chargeStamina(value)
			usr.save()
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)
		if operator == 'trp':
			value = request.POST['tfTrp']
			if value == '':
				return HttpResponse('培养点为空')
			usr = user.get(roleid)
			if not usr:
				return HttpResponse('玩家不存在')
			usr.trp = int(value)
			usr.save()
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)
	return render(request, 'profile.html', data)
			
def gm_tool_set_pet(request):
	
	data = {}
	if request.method == 'POST':
		petopt = request.POST['petopt']
		roleid = request.POST['roleid']
		
		usr = user.get(roleid)
		
		if not usr:
			return HttpResponse('玩家不存在')
		acc = usr.getAccount()		
		
		if petopt == 'add':
			cardid = request.POST['petSelect']
			inv = usr.getInventory()
			c = inv.addCard(cardid)
			inv.save()
			if not c:
				return HttpResponse('添加失败')			
		elif petopt == 'remove':
			id = request.POST['petid']
			inv = usr.getInventory()
			if not inv.delCard(id):
				return HttpResponse('删除失败')		
			inv.save()	
		data = gm.show_profile(acc, usr)
		return render(request, 'profile.html', data)
	return HttpResponse('未知命令')
			
			
def gm_tool_set_stone(request):
	data = {}
	if request.method == 'POST':
		stoneopt = request.POST['stoneopt']
		roleid = request.POST['roleid']
		
		usr = user.get(roleid)
		
		if not usr:
			return HttpResponse('玩家不存在')
		acc = usr.getAccount()		
		
		if stoneopt == 'add':
			stoneid = request.POST['stoneSelect']
			inv = usr.getInventory()
			s = inv.addStone(stoneid)
			inv.save()
			if not s:
				return HttpResponse('添加失败')
		elif stoneopt == 'remove':
			id = request.POST['stoneid']
			inv = usr.getInventory()
			if not inv.delStone(id):
				return HttpResponse('删除失败')
			inv.save()
		data = gm.show_profile(acc, usr)
		return render(request, 'profile.html', data)
	return HttpResponse('未知命令')
			
	
	
def gm_tool_set_equipment(request):
	data = {}
	if request.method == 'POST':
		equipmentopt = request.POST['equipmentopt']
		roleid = request.POST['roleid']
		
		usr = user.get(roleid)
		
		if not usr:
			return HttpResponse('玩家不存在')
		acc = usr.getAccount()		
		
		if equipmentopt == 'add':
			equipmentid = request.POST['equipmentSelect']
			inv = usr.getInventory()
			s = inv.addEquipment(equipmentid)
			inv.save()
			if not s:
				return HttpResponse('添加失败')
		elif equipmentopt == 'remove':
			id = request.POST['equipmentid']
			inv = usr.getInventory()
			if not inv.delEquipment(id):
				return HttpResponse('删除失败')
			inv.save()			
		data = gm.show_profile(acc, usr)			
		return render(request, 'profile.html', data)
	return HttpResponse('未知命令')
	

def gm_tool_set_skill(request):
	data = {}
	if request.method == 'POST':
		skillopt = request.POST['skillopt']
		roleid = request.POST['roleid']
		
		usr = user.get(roleid)
		
		if not usr:
			return HttpResponse('玩家不存在')
		acc = usr.getAccount()		
		
		if skillopt == 'add':
			skillid = request.POST['skillSelect']
			inv = usr.getInventory()
			s = inv.addSkill(skillid)
			inv.save()
			if not s:
				return HttpResponse('添加失败')
			data = gm.show_profile(acc, usr)
		elif skillopt == 'remove':
			id = request.POST['skillid']
			inv = usr.getInventory()
			if not inv.delSkill(id):
				return HttpResponse('删除失败')
			inv.save()		
		data = gm.show_profile(acc, usr)
		return render(request, 'profile.html', data)
	return HttpResponse('未知命令')