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
				
def card(request):
	return generalConfigRequestProcess(request, 'card')
	
def game(request):
	return generalConfigRequestProcess(request, 'game')

def skill(request):
	return generalConfigRequestProcess(request, 'skill')
	
def pet_level(request):
	return generalConfigRequestProcess(request, 'pet_level')
				
				
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
				
def level_import(request):
	if request.method == 'POST':
		level_file = request.FILES.get('level_file')
		if level_file == None:
			return HttpResponse('等级文件未上传')
	
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
	
def skill_import(request):
	if request.method == 'POST':
		skill_file = request.FILES.get('skill_file')		
							
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, dungeon_file.read())			
		sheet = wb.sheet_by_index(0)		
		
		conf = {}
		for rownum in range(4,sheet.nrows):
			row = sheet.row_values(rownum)	
			skillid = row[0]
			name = row[1]
			icon = row[2]
			rate = row[3]
			desc = row[4]
			nature = row[5]
			maxLevel = row[6]
			triggerType = row[7]
			type = row[8]
			startEffect = row[9]
			inprocessEffect = row[10]
			finishEffect = row[11]
			
			
def pet_level_import(request):
	if request.method == 'POST':
		pet_level_file = request.FILES.get('pet_level_file')
		
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
			dropCard = row[17]
			dropCardLevel = row[18]
			dropCardProb = row[20]
			dropItem = row[21]
			dropItemProb = row[22]
			dropEquipment = row[23]
			dropEquipmentProb = row[26]
			dropMoney = int(row[28])
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
			fieldId = row[6]
			fieldName = row[7]
			stamina = int(row[9])
			exp = int(row[11])
			difficult = int(row[12])
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
			fieldConf['wave'] = read_waves(row, dropConf)
			dunConf['field'].append(fieldConf)
		Conf.append(dunConf)
			
			
	return HttpResponse(gcjson.dumps(Conf))
	
def read_waves(row, dropConf):	
	waveConf = []	
	wave = read_wave(row, 13, dropConf)	
	waveConf.append(wave)	
	wave = read_wave(row, 27, dropConf)
	if wave:
		waveConf.append(wave)
		wave = read_wave(row, 41, dropConf)
		if wave:
			waveConf.append(wave)
			wave = read_wave(row, 55, dropConf)
			if wave:
				waveConf.append(wave)
				wave = read_wave(row, 69, dropConf)
				if wave:
					waveConf.append(wave)
					wave = read_wave(row, 83, dropConf)
					if wave:
						waveConf.append(wave)
						wave = read_wave(row, 97, dropConf)
						if wave:
							waveConf.append(wave)
							wave = read_wave(row, 111, dropConf)
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