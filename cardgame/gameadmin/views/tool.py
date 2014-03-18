#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from game.utility.config import config
from game.models.user import user
from game.models.account import account
from gclib.utility import currentTime
from django.shortcuts import render
from game.routine.arena import arena
from gclib.json import json
from gameadmin.routine.gm import gm
from game.routine.signin import signin
from game.routine.medal import medal
from game.routine.equipment import equipment
from game.routine.skill import skill
from game.routine.drop import drop
from game.routine.stone import stone
import random
	
def tool_create_player(request):
	if request.method == 'POST':
		player_name = request.POST['player_name']
		levelf = int(request.POST['levelf'])
		levelt = int(request.POST['levelt'])
		protagonist_card = request.POST['protagonist_card']
		other_card = request.POST['other_card']
		card_count = int(request.POST['card_count'])
		card_levelf = int(request.POST['card_levelf'])
		card_levelt = int(request.POST['card_levelt'])
		attack_equipment = request.POST['attack_equipment']
		hp_equipment = request.POST['hp_equipment']
		defence_equipment = request.POST['defence_equipment']		
		pd_equipment = request.POST['pd_equipment']
		md_equipment = request.POST['md_equipment']
		equipment_strength_levelf = int(request.POST['equipment_strength_levelf'])
		equipment_strength_levelt = int(request.POST['equipment_strength_levelt'])
		fire_skill = request.POST['fire_skill']
		water_skill = request.POST['water_skill']
		poison_skill = request.POST['poison_skill']
		super_skill = request.POST['super_skill']
		straw_skill = request.POST['straw_skill']		
		general_skill = request.POST['general_skill']
		skill_levelf = int(request.POST['skill_levelf'])
		skill_levelt = int(request.POST['skill_levelt'])
		stone_seed = request.POST['stone']
		stone_levelf = int(request.POST['stone_levelf'])
		stone_levelt = int(request.POST['stone_levelt'])
		practicef = int(request.POST['practicef'])
		practicet = int(request.POST['practicet'])
		strengthenf = int(request.POST['strengthenf'])
		strengthent = int(request.POST['strengthent'])
		
		intelligencef = int(request.POST['intelligencef'])
		intelligencet = int(request.POST['intelligencet'])
		artificef = int(request.POST['artificef'])
		artificet = int(request.POST['artificet'])
		medal_levelf = int(request.POST['medal_levelf'])
		medal_levelt = int(request.POST['medal_levelt'])
			
		gameConf = config.getConfig('game')
		
		for i in range(card_count):
			usr = user()					
			usr.init(None)
			usr.last_login = currentTime()
			usr.name = player_name
			usr.gender = 'male'
			usr.avatar = '1'
			usr.install(0)
			
			usr.saveRoleId()
			usr.onInit()
			usr.level = random.randint(levelf, levelt)
			inv = usr.getInventory()
			awd = drop.open(usr, protagonist_card, {})
			for (i, l) in enumerate(gameConf['team_member_open_level']):
				if l <= usr.level:
					if awd['add_card_array']:
						awd['add_card_array'][0]['level'] = random.randint(card_levelf, card_levelt)
						inv.team[i] = awd['add_card_array'][0]['id']
					break
					
			for (i, l) in enumerate(gameConf['team_member_open_level']):
				if l <= usr.level and not inv.team[i]:
					awd = drop.open(usr, other_card, {})
					if awd['add_card_array']:
						awd['add_card_array'][0]['level'] = random.randint(card_levelf, card_levelt)
						inv.team[i] = awd['add_card_array'][0]['id']
					break			
			petConf = config.getConfig('pet')
			for (i, cid) in enumerate(inv.team):
				if cid:
					card = inv.getCard(cid)
					if card:
						awd = drop.open(usr, attack_equipment, {})
						if awd.has_key('add_equipment_array'):
							awd['add_equipment_array'][0]['strengthLevel'] = random.randint(equipment_strength_levelf, equipment_strength_levelt)
							equipment.equip(usr, i, -1, awd['add_equipment_array'][0]['id'])
						awd = drop.open(usr, hp_equipment, {})
						if awd.has_key('add_equipment_array'):
							awd['add_equipment_array'][0]['strengthLevel'] = random.randint(equipment_strength_levelf, equipment_strength_levelt)
							equipment.equip(usr, i, -1, awd['add_equipment_array'][0]['id'])
						awd = drop.open(usr, defence_equipment, {})
						if awd.has_key('add_equipment_array'):
							awd['add_equipment_array'][0]['strengthLevel'] = random.randint(equipment_strength_levelf, equipment_strength_levelt)
							equipment.equip(usr, i, -1, awd['add_equipment_array'][0]['id'])						
						awd = drop.open(usr, pd_equipment, {})
						if awd.has_key('add_equipment_array'):
							awd['add_equipment_array'][0]['strengthLevel'] = random.randint(equipment_strength_levelf, equipment_strength_levelt)
							equipment.equip(usr, i, -1, awd['add_equipment_array'][0]['id'])
						awd = drop.open(usr, md_equipment, {})
						if awd.has_key('add_equipment_array'):
							awd['add_equipment_array'][0]['strengthLevel'] = random.randint(equipment_strength_levelf, equipment_strength_levelt)
							equipment.equip(usr, i, -1, awd['add_equipment_array'][0]['id'])
						
						petInfo = petConf[card['cardid']]						
						skill_seed = None
						
						if petInfo['nature'] == '2':
							skill_seed = poison_skill
						elif petInfo['nature'] == '3':
							skill_seed = straw_skill
						elif petInfo['nature'] == '4':
							skill_seed = water_skill
						elif petInfo['nature'] == '5':
							skill_seed = fire_skill
						elif petInfo['nature'] == '6':
							skill_seed = super_skill
						elif petInfo['nature'] == '7':
							skill_seed = general_skill
							
						if skill_seed:
							for k in range(3):
								awd = drop.open(usr, skill_seed, {})
								if awd.has_key('add_skill_array'):
									awd['add_skill_array'][0]['level'] = random.randint(skill_levelf, skill_levelt)
									skill.install(usr, i, -1, k, awd['add_skill_array'][0]['id'])
									
						for (k, l) in enumerate(gameConf['stone_slot_level']):
							if l <= usr.level:
								awd = drop.open(usr, stone_seed, {})
								if awd.has_key('add_stone_array'):
									awd['add_stone_array'][0]['level'] = random.randint(stone_levelf, stone_levelt)
									stone.install(usr, i, -1, k, awd['add_stone_array'][0]['id'])
						card['strength'] = random.randint(strengthenf, strengthent)
						card['intelligence'] = random.randint(intelligencef, intelligencet)
						card['artifice'] = random.randint(artificef, artificet)
						
						medalConf = config.getConfig('medal')
						
						for medalid in medalConf:
							inv.medal[medalid] =  {'level':0, 'chip': [0] * medalConf[medalid]['chip'], 'id':medalid, 'gravel':0}
							inv.medal[medalid]['level'] = random.randint(medal_levelf, medal_levelt)
									
			usr.practice['critical_level'] = random.randint(practicef, practicet)
			usr.practice['tenacity_level'] = random.randint(practicef, practicet)
			usr.practice['block_level'] = random.randint(practicef, practicet)
			usr.practice['wreck_level'] = random.randint(practicef, practicet)			
			
																	
			usr.save()
			res = arena.stand_ladder(usr)	
			if isinstance(res, str):
				res = json.loads(res)
				if res.has_key('msg'):
					return HttpResponse('error:' + str(i) + ':' + str(usr.roleid) + res['msg'])		
	ld = arena.show_all()	
	return render(request, 'arena_tool.html', {'ladder':ld})
		
def tool_ladder_remove(request):
	if request.method == 'POST':
		optid = request.POST['optid']
		operator = request.POST['operator']
		if operator == 'remove':
			arena.remove(optid)		
	ld = arena.show_all()
	return render(request, 'arena_tool.html', {'ladder':ld})
		
def gm_tool(request):
	if request.method == 'POST':
		pass
	return render(request, 'profile.html', {})
	
def gm_tool_profile_find(request):
	data = {}
	if request.method == 'POST':
		opt = request.POST['findopt']
		if opt == 'roleidFind':
			roleid = request.POST['tfRoleid']
			if roleid:
				usr = user.get(roleid)
				if not usr:
					return HttpResponse('玩家不存在')
				acc = usr.getAccount()
				data = gm.show_profile(acc, usr)
		elif opt == 'accountFind':
			name = request.POST['tfAccountName']
			acc = account.get_by_account_name(name)
			if not acc:
				return HttpResponse('帐号不存在')
			usr = acc.getUser()
			if not usr:
				return HttpResponse('玩家不存在')
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
		elif operator == 'gold':
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
		elif operator == 'gem':
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
		elif operator == 'stamina':
			value = request.POST['tfStamina']
			if value == '':
				return HttpResponse('体力为空')
			usr = user.get(roleid)
			if not usr:
				return HttpResponse('玩家不存在')
			usr.chargeStamina(int(value))
			usr.save()
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)
		elif operator == 'trp':
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
		elif operator == 'reset_login':
			usr = user.get(roleid)
			signin.reset(usr)
			usr.save()
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)
		elif operator == 'login_count':
			value = request.POST['tfLoginCount']
			if value == '':
				return HttpResponse('次数不能为空')
			usr = user.get(roleid)
			if not usr:
				return HttpResponse('玩家不存在')
			usr.signin['login_count'] = int(value)
			usr.signin['last_login_time'] = currentTime()
			usr.signin['last_signin_time'] = currentTime()
			usr.save()
			acc = usr.getAccount()
			data = gm.show_profile(acc, usr)
		elif operator == 'email':
			value = request.POST['emailSselect']
			if value == '':
				return HttpResponse('email不能为空')
			usr = user.get(roleid)
			if not usr:
				return HttpResponse('玩家不存在')
			
			nw = usr.getNetwork()
			emailConf = config.getConfig('email')
			emailInfo = emailConf[value]
			
			if emailInfo['optype'] == 1:
				nw.appendEmail(value, usr.name)
			elif emailInfo['optype'] == 2:
				nw.appendEmail(value, str(currentTime()))
			else: 
				return HttpResponse('不能发送')
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
			cnt = int(request.POST['tfPetCount'])
			level = int(request.POST['tfPetLevel'])
			inv = usr.getInventory()
			c = inv.addCardCount(cardid, cnt, level)
			inv.save()
			if not c:
				return HttpResponse('添加失败')			
		elif petopt == 'remove':
			id = request.POST['petid']
			inv = usr.getInventory()
			if not inv.delCard(id):
				return HttpResponse('删除失败')		
			inv.save()
		elif petopt == 'add_chip':
			cardid = request.POST['petChipSelect']
			cnt = int(request.POST['tfPetChipCount'])
			inv = usr.getInventory()
			if inv.addCardChip(cardid, cnt) < 0:
				return HttpResponse('添加失败')				
			inv.save()
		else:
			return HttpResponse('无效的功能')
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
			cnt = int(request.POST['tfStoneCount'])
			inv = usr.getInventory()
			s = inv.addStoneCount(stoneid, cnt)
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
			cnt = int(request.POST['tfEquipmentCount'])
			inv = usr.getInventory()
			s = inv.addEquipmentCount(equipmentid,cnt)
			inv.save()
			if not s:
				return HttpResponse('添加失败')
		elif equipmentopt == 'remove':
			id = request.POST['equipmentid']
			inv = usr.getInventory()
			if not inv.delEquipment(id):
				return HttpResponse('删除失败')
			inv.save()
		elif equipmentopt == 'add_chip':
			id = request.POST['equipmentChipSelect']
			cnt = int(request.POST['tfEquipmentChipCount'])
			inv = usr.getInventory()
			if inv.addEquipmentChip(id, cnt) < 0:
				return HttpResponse('添加失败')
			inv.save()
		else:
			return HttpResponse('无效功能')
				
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
			cnt = int(request.POST['tfSkillCount'])
			inv = usr.getInventory()
			s = inv.addSkillCount(skillid, cnt)
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
		elif skillopt == 'add_chip':
			skillid = request.POST['skillChipSelect']
			cnt = int(request.POST['tfSkillChipCount'])
			inv = usr.getInventory()
			if inv.addSkillChip(skillid, cnt) < 0:
				return HttpResponse('添加失败')		
			inv.save()		
		else:
			return HttpResponse('无效功能')
		data = gm.show_profile(acc, usr)
		return render(request, 'profile.html', data)
	return HttpResponse('未知命令')
	
def gm_tool_set_item(request):
	data = {}
	if request.method == 'POST':
		skillopt = request.POST['itemopt']
		roleid = request.POST['roleid']	
		
		usr = user.get(roleid)		
		if not usr:
			return HttpResponse('玩家不存在')
		acc = usr.getAccount()		
		
		if skillopt == 'add':
			itemid = request.POST['itemSelect']
			cnt = request.POST['tfItemCount']
			cnt = int(cnt)
			inv = usr.getInventory()
			s = inv.addItemCount(itemid, cnt)
			inv.save()
			if not s:
				return HttpResponse('添加失败')
			data = gm.show_profile(acc, usr)
		elif skillopt == 'remove':
			id = request.POST['itemid']
			inv = usr.getInventory()			
			if inv.delItem(id) == 0:
				return HttpResponse('删除失败')			
			inv.save()		
			data = gm.show_profile(acc, usr)
		return render(request, 'profile.html', data)
	return HttpResponse('未知命令')
	
def gm_tool_set_medal(request):
	data = {}
	if request.method == 'POST':
		medalopt = request.POST['medalopt']
		roleid = request.POST['roleid']
		
		usr = user.get(roleid)
		if not usr:
			return HttpResponse('玩家不存在')
		acc = usr.getAccount()
			
		if medalopt == 'add':
			medalid = request.POST['medalSelect']
			chipnum = int(request.POST['chipSelect'])
			cnt = int(request.POST['tfChipCount'])
			inv = usr.getInventory()
			mc = inv.addMedalChip(medalid, chipnum, cnt)
			medal.newMedal(usr, medalid, chipnum, cnt)				
			if not mc:
				return HttpResponse('删除失败')
			inv.save()
			data = gm.show_profile(acc, usr)
		return render(request, 'profile.html', data)
	return HttpResponse('未知命令')
				
				
				
		
		
		
	