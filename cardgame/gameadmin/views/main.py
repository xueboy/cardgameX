#coding:utf-8
#!/usr/bin/env python

from django.shortcuts import render
from gclib.DBConnection import DBConnection
from django.http import HttpResponse
from gclib.gcjson import gcjson
from gclib.gcconfig import gcconfig
import xlrd
from xlrd import USE_MMAP
import sys

def index(request):
	return render(request, 'index.html', {})


def dungeon(request):
	return generalConfigRequestProcess(request, 'dungeon')		
				
def level(request):
	return generalConfigRequestProcess(request, 'level')				
				
def monster(request):
	return generalConfigRequestProcess(request, 'monster')			
				
def game(request):
	return generalConfigRequestProcess(request, 'game')

def skill(request):
	return generalConfigRequestProcess(request, 'skill')
	
def pet(request):
	return generalConfigRequestProcess(request, 'pet')
	
def pet_level(request):
	return generalConfigRequestProcess(request, 'pet_level')
	
def prompt(request):
	return generalConfigRequestProcess(request, 'prompt')

def garcha(request):
	return generalConfigRequestProcess(request, 'garcha')	

				
def generalConfigRequestProcess(request, confname):
	if request.method == 'POST':
		confstr = request.POST['config']
		try:
			gcconfig.setConfig(confname, confstr)		
			return render(request, 'index.html', {})
		except:
			return render(request, confname + '.html', {'config':confstr})
	else:
		conf = gcconfig.getConfigStr(confname)		
		if conf != None:			
			return render(request, confname + '.html', {'config': gcconfig.getConfigStr(confname)})
		else:
			gcconfig.createConfig(confname)			
			return render(request, confname + '.html', {'config':''})
				
def garcha_import(request):
	if request.method == 'POST':
		garcha_file = request.FILES.get('garcha_file')
		if garcha_file == None:
			return HttpResponse('抽奖武将xlsx文件未上传')
			
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, garcha_file.read())
		sheet = wb.sheet_by_index(0)
		
		conf = {}
		for rownum in range(4, sheet.nrows):
			row = sheet.row_values(rownum)
			cardid = row[0]
			name = row[1]
			star = row[2]
			level = row[3]
			group = row[5]
			prob = row[6]
			
			key = int(prob)
			garchaConf = {}
			garchaConf['cardId'] = cardid
			garchaConf['name'] = name
			garchaConf['star'] = star
			garchaConf['level'] = level
			garchaConf['group'] = group
			
			if not conf.has_key(key):
				conf[key] = []
			conf[key].append(garchaConf)
		return HttpResponse(gcjson.dumps(conf))
	return HttpResponse('garcha_import')

def prompt_import(request):
	if request.method == 'POST':
		prompt_file = request.FILES.get('prompt_file')
		if prompt_file == None:
			return HttpResponse('小帖士xlsx文件未上传')
			
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, prompt_file.read())
		sheet = wb.sheet_by_index(0)
		
		conf = {}
		for rownum in range(3,sheet.nrows):
			row = sheet.row_values(rownum)
			promptid = row[0]
			prompt = row[1]
			conf[promptid] = prompt
			
		return HttpResponse(gcjson.dumps(conf))
	return HttpResponse('prompt_import')


def level_import(request):
	if request.method == 'POST':
		level_file = request.FILES.get('level_file')
		if level_file == None:
			return HttpResponse('等级xlsx文件未上传')			
	
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, level_file.read())
		sheet = wb.sheet_by_index(0)
	
		conf = {}
		for rownum in range(6,sheet.nrows):
			row = sheet.row_values(rownum)
			level = row[0]
			exp = row[1]
			sp = row[2]
			leadership = row[3]
			friend = row[4]
			
			levelConf = {}
			levelConf['levelExp'] = int(exp)
			levelConf['sp'] = int(sp)
			levelConf['leadership'] = int(leadership)
			levelConf['friend'] = int(friend)
			levelConf[str(int(level))] = conf
		return HttpResponse(gcjson.dumps(conf))
	return HttpResponse('prompt_import')
	
def skill_import(request):
	if request.method == 'POST':
		skill_file = request.FILES.get('skill_file')		
		if skill_file == None:
			return HttpResponse('技能xlsx文件未上传')
							
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, skill_file.read())			
		sheet = wb.sheet_by_index(0)		
		
		conf = {}
		for rownum in range(4,sheet.nrows):
			row = sheet.row_values(rownum)	
			skillid = row[0]
			name = row[1]
			icon = row[2]
			prob = row[3]
			desc = row[4]
			nature = row[6]
			maxLevel = row[7]
			triggerType = row[8]
			type = row[9]
			startEffect = row[10]
			inprocessEffect = row[11]
			finishEffect = row[12]
			
			fun1id = row[13]
			if fun1id != 0.0:				
				fun1name = row[14]
				fun1nature = []
				#fun1nature.append(row[15])
				fun1nature.append(int(row[16]))
				#fun1nature.append(row[17])
				fun1nature.append(int(row[18]))
				fun1target = row[19]
				fun1valueType = row[21]
				fun1value = row[22]
				fun1levelUp = row[23]
				fun1buffid = row[24]
				fun1duration = row[25]			
			
			fun2id = row[26]				
			if fun2id != 0.0:				
				fun2name = row[27]
				fun2nature = []
				fun2nature.append(int(row[28]))
				fun2nature.append(int(row[29]))
				fun2nature.append(int(row[30]))
				fun2nature.append(int(row[31]))
				fun2target = row[32]
				fun2valueType = row[34]
				fun2value = row[35]
				fun2levelUp = row[36]
				fun2buffid = row[37]
				fun2duration = row[38]
				
			skillConf = {}
			skillConf['name'] = name
			skillConf['icon'] = icon
			skillConf['prob'] = prob
			skillConf['desc'] = desc
			skillConf['nature'] = nature
			skillConf['maxLevel'] = maxLevel
			skillConf['triggerType'] = triggerType
			skillConf['type'] = type
			skillConf['startEffect'] = startEffect
			skillConf['inprocessEffect'] = inprocessEffect
			skillConf['finishEffect'] = finishEffect
			skillConf['function'] = {}
			
			if fun1id != 0.0:
				funConf = {}
				funConf['name'] = fun1name
				funConf['nature'] = fun1nature
				funConf['target'] = fun1target
				funConf['valueType'] = fun1valueType
				funConf['valueAmount'] = fun1value
				funConf['levelup'] = fun1levelUp
				funConf['buffid'] = fun1buffid
				funConf['duration'] = fun1duration
				skillConf['function'][str(fun1id)] = funConf
			
			if fun2id != 0.0:
				funConf = {}
				funConf['name'] = fun2name
				funConf['nature'] = fun2nature
				funConf['target'] = fun2target
				funConf['valueType'] = fun2valueType
				funConf['valueAmount'] = fun2value
				funConf['levelup'] = fun2levelUp
				funConf['buffid'] = fun2buffid
				funConf['duration'] = fun2duration
				skillConf['function'][str(fun2id)] = funConf
			conf[str(skillid)] = skillConf
		
		return HttpResponse(gcjson.dumps(conf))
		
	return HttpResponse('skill_import')
			
def pet_import(request):
	if request.method == 'POST':
		pet_file = request.FILES.get('pet_file')
		if pet_file == None:
			return HttpResponse("宠物xlsx文件未上传")
		
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, pet_file.read())
		sheet = wb.sheet_by_index(1)
		
		conf = {}
		for rownum in range(3, sheet.nrows):
			row = sheet.row_values(rownum)
			petid = row[3]
			imageid = row[4]
			icon = row[5]
			name = row[6]
			type = row[8]
			leadership = row[10]
			nature = row[12]
			star = row[13]
			maxLevel = row[14]
			hp = row[15]
			attack = row[16]
			recover = row[17]
			agile = row[18]
			skillid = row[19]
			evoPrice = row[23]
			evoId = row[24]
			evoObjectId = []
			evoObjectId.append(str(row[25]))
			evoObjectId.append(str(row[26]))
			evoObjectId.append(str(row[27]))
			evoObjectId.append(str(row[28]))
			desc = row[29]
			petConf = {}
			petConf['imageId'] = imageid
			petConf['icon'] = icon
			petConf['name'] = name
			petConf['type'] = type
			petConf['leadership'] = leadership
			petConf['nature'] = nature
			petConf['star'] = star
			petConf['maxLevel'] = maxLevel
			petConf['hp'] = hp
			petConf['attack'] = attack
			petConf['recover'] = recover
			petConf['agile'] = agile
			petConf['skillId'] = skillid
			petConf['evoPrice'] = evoPrice
			petConf['evoId'] = evoId
			petConf['evoMaterial'] = evoObjectId
			petConf['describe'] = desc
			conf[str(petid)] = petConf
		return HttpResponse(gcjson.dumps(conf))
	return HttpResponse('pet_import')
									
def pet_level_import(request):
	if request.method == 'POST':
		pet_level_file = request.FILES.get('pet_level_file')
		if pet_level_file == None:
			return HttpResponse('宠物等级xlsx文件未上传')
		
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, pet_level_file.read())
		sheet = wb.sheet_by_index(0)
		
		conf = {}
		for rownum in range(3, sheet.nrows):
			row = sheet.row_values(rownum)
			level = str(int(row[0]))
			star1Exp = int(row[1])
			star2Exp = int(row[2])
			star3Exp = int(row[3])
			star4Exp = int(row[4])
			levelConf = []
			levelConf.append(star1Exp)
			levelConf.append(star2Exp)
			levelConf.append(star3Exp)
			levelConf.append(star4Exp)
			conf[str(level)] = levelConf
		return HttpResponse(gcjson.dumps(conf))
	return HttpResponse('pet_level_import')
				
def dungeon_import(request):
	if request.method == 'POST':
		dungeon_file = request.FILES.get('dungeon_file')		
		if dungeon_file == None:
			return HttpResponse('关卡xlsx文件未上传')			
					
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, dungeon_file.read())			
		dungeon_sheet = wb.sheet_by_index(0)
		drop_sheet = wb.sheet_by_index(2)		
				
		dropConf = {}
		for rownum in range(4,drop_sheet.nrows):
			row = drop_sheet.row_values(rownum)
			monsterId = str(row[0])
			if monsterId == '' or monsterId == '0.0':
				continue
			dropCard = row[18]
			dropCardLevel = row[19]
			dropCardProb = row[21]
			dropItem = row[22]
			dropItemProb = row[23]
			dropEquipment = row[24]
			dropEquipmentProb = row[27]
			dropMoney = int(row[29])
			dropConf[str(monsterId)] = {}
			cardConf = {}
			if dropCard != '':
				cardConf['id'] = dropCard
				cardConf['level'] = int(dropCardLevel)
				cardConf['drop'] = int(dropCardProb)
			itemConf = {}
			if dropItem != '':
				itemConf['id'] = dropItem
				itemConf['drop'] = int(dropItemProb)
			equipmentConf = {}
			if dropEquipment != '':
				equipmentConf['id'] = dropEquipment
				equipmentConf['drop'] = int(dropEquipmentProb)
			dropConf[str(monsterId)]['money'] = dropMoney
			dropConf[str(monsterId)]['card'] = cardConf
			dropConf[str(monsterId)]['item'] = itemConf
			dropConf[str(monsterId)]['equipment'] = equipmentConf			
		
		Conf = []
		dunConf = {'battleId':''}
		fieldConf = None
		waveConf = None
		if dropConf.has_key(''):
			return HttpResponse('1')
		
		for rownum in range(4,dungeon_sheet.nrows):
			row = dungeon_sheet.row_values(rownum)
			battleId = row[1]
			rule = int(row[2])
			battleName = row[3]
			imageId = row[5]
			fieldId = row[7]
			fieldName = row[8]
			stamina = int(row[10])
			exp = int(row[12])
			difficult = int(row[13])
			mayDrop1 = row[14]
			mayDrop2 = row[15]
			if dunConf['battleId'] != battleId:
				if dunConf['battleId'] != '':
					Conf.append(dunConf)
				dunConf = {}
				dunConf['battleId'] = battleId
				dunConf['rule'] = rule
				dunConf['battleName'] = battleName
				dunConf['imageId'] = imageId
				dunConf['field'] = []				
			fieldConf = {}			
			fieldConf['fieldId'] = fieldId
			fieldConf['fieldName'] = fieldName
			fieldConf['stamina'] = stamina
			fieldConf['exp'] = exp
			fieldConf['difficult'] = difficult
			fieldConf['mayDrop'] = [mayDrop1, mayDrop2]
			fieldConf['wave'] = read_waves(row, dropConf)
			dunConf['field'].append(fieldConf)
		Conf.append(dunConf)
			
			
	return HttpResponse(gcjson.dumps(Conf))
	
def read_waves(row, dropConf):	
	waveConf = []	
	wave = read_wave(row, 16, dropConf)
	if wave:
		waveConf.append(wave)	
		wave = read_wave(row, 30, dropConf)
		if wave:
			waveConf.append(wave)
			wave = read_wave(row, 44, dropConf)
			if wave:
				waveConf.append(wave)
				wave = read_wave(row, 58, dropConf)	
				if wave:
					waveConf.append(wave)
					wave = read_wave(row, 72, dropConf)
					if wave:
						waveConf.append(wave)
						wave = read_wave(row, 86, dropConf)
						if wave:
							waveConf.append(wave)
							wave = read_wave(row, 100, dropConf)
							if wave:
								waveConf.append(wave)
								wave = read_wave(row, 114, dropConf)
								if wave:
									waveConf.append(wave)	
	return waveConf
	
def read_wave(row, idx, dropConf):
	wave = {}
	wave['monster'] = {}
	monster1 = str(row[idx + 0])
	monster2 = str(row[idx + 1])
	monster3 = str(row[idx + 2])
	monster4 = str(row[idx + 3])
	monster5 = str(row[idx + 4])
	if dropConf.has_key(str(monster1)):
		wave['monster'][monster1] = dropConf[str(monster1)]
	else:
		if monster1 != '' and monster1 != '0.0':
			wave['monster'][monster1] = {}
	
	if dropConf.has_key(str(monster2)):
		wave['monster'][monster2] = dropConf[str(monster2)]
	else:
		if monster2 != '' and monster2 != '0.0':
			wave['monster'][monster2] = {}
		
	if dropConf.has_key(str(monster3)):
		wave['monster'][monster3] = dropConf[str(monster3)]
	else: 
		if monster3 != '' and monster3 != '0.0':
			wave['monster'][monster3] = {}
		
	if dropConf.has_key(str(monster4)):
		wave['monster'][monster4] = dropConf[str(monster4)]
	else:
		if monster4 != '' and monster4 != '0.0':
			wave['monster'][monster4] = {}
		
	if dropConf.has_key(str(monster5)):
		wave['monster'][monster5] = dropConf[str(monster5)]
	else:
		if monster5 != '' and monster5 != '0.0':
			wave['monster'][monster5] = {}
			
	wave['boss'] = {}
			
	boss1 = str(row[idx + 5])
	boss2 = str(row[idx + 6])
	boss3 = str(row[idx + 7])
	boss4 = str(row[idx + 8])
	boss5 = str(row[idx + 9])
	boss6 = str(row[idx + 10])
	
	if dropConf.has_key(str(boss1)):
		wave['boss'][boss1] = dropConf[str(boss1)]
	else:
		if boss1 != '':
			wave['boss'][boss1] = {}
		
	if dropConf.has_key(str(boss2)):
		wave['boss'][boss2] = dropConf[str(boss2)]
	else:
		if boss2 != '':
			wave['boss'][boss2] = {}
		
	if dropConf.has_key(str(boss3)):
		wave['boss'][boss3] = dropConf[str(boss3)]
	else:
		if boss3 != '':
			wave['boss'][boss3] = {}
		
	if dropConf.has_key(str(boss4)):
		wave['boss'][boss4] = dropConf[str(boss4)]
	else: 
		if boss4 != '':
			wave['boss'][boss4] = {}
		
	if dropConf.has_key(str(boss5)):
		wave['boss'][boss5] = dropConf[str(boss5)]
	else: 
		if boss5 != '':
			wave['boss'][boss5] = {}
		
	if dropConf.has_key(str(boss6)):
		wave['boss'][boss6] = dropConf[str(boss6)]
	else:
		if boss6 != '':
			wave['boss'][boss6] = {}
	
	if (monster1 == '' or monster1 == '0' or monster1 == '0.0') and (boss1 == '' or boss1 == '0' or boss1 == '0.0'):		
		return None	
	
	ls = str(row[idx + 11]).split(',')
	wave['count'] =  [ int( eval(x) ) for x in ls if x ]
	if sum(wave['count']) == 0:
		return None
	ls = str(row[idx + 12]).split(',')
	wave['count_prob'] = [ int( eval(x) ) for x in ls if x ]
	if sum(wave['count_prob']) == 0:
		return None
	wave['more'] = int(row[idx + 13])
	return wave