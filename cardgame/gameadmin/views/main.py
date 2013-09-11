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
				
				
def generalConfigRequestProcess(request, confname):
	if request.method == 'POST':
		confstr = request.POST['config']
		#try:
		gcconfig.setConfig(confname, confstr)		
		return render(request, 'index.html', {})
		#except:
		#	return render(request, confname + '.html', {'config':confstr})
	else:
		conf = gcconfig.getConfigStr(confname)		
		if conf != '':			
			return render(request, confname + '.html', {'config': gcconfig.getConfigStr(confname)})
		else:
			gcconfig.createConfig(confname)			
			return render(request, confname + '.html', {'config':''})
				
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
			monsterId = row[0]
			dropCard = row[17]
			dropCardLevel = row[18]
			dropCardProb = row[20]
			dropItem = row[21]
			dropItemProb = row[22]
			dropEquipment = row[23]
			dropEquipmentProb = row[26]
			dropMoney = row[28]
			dropConf[str(monsterId)] = {}
			cardConf = {}
			cardConf['id'] = dropCard
			cardConf['level'] = dropCardLevel
			cardConf['drop'] = dropCardProb
			itemConf = {}
			itemConf['id'] = dropItem
			itemConf['drop'] = dropItemProb
			equipmentConf = {}
			equipmentConf['id'] = dropEquipment
			equipmentConf['drop'] = dropEquipmentProb
			dropConf[str(monsterId)]['money'] = dropMoney
			dropConf[str(monsterId)]['card'] = cardConf
			dropConf[str(monsterId)]['item'] = itemConf
			dropConf[str(monsterId)]['equipment'] = equipmentConf			
		
		Conf = []
		dunConf = {'battleId':''}
		fieldConf = None
		waveConf = None
		
		for rownum in range(4,dungeon_sheet.nrows):
			row = dungeon_sheet.row_values(rownum)
			battleId = row[1]
			rule = row[2]			
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
	monster1 = row[idx + 0]
	monster2 = row[idx + 1]
	monster3 = row[idx + 2]
	monster4 = row[idx + 3]
	monster5 = row[idx + 4]
	if dropConf.has_key(str(monster1)):
		wave['monster'][monster1] = dropConf[str(monster1)]
	else: 
		wave['monster'][monster1] = {}
	
	if dropConf.has_key(str(monster2)):
		wave['monster'][monster2] = dropConf[str(monster2)]
	else: 
		wave['monster'][monster2] = {}
		
	if dropConf.has_key(str(monster3)):
		wave['monster'][monster3] = dropConf[str(monster3)]
	else: 
		wave['monster'][monster3] = {}
		
	if dropConf.has_key(str(monster4)):
		wave['monster'][monster4] = dropConf[str(monster4)]
	else: 
		wave['monster'][monster4] = {}
		
	if dropConf.has_key(str(monster5)):
		wave['monster'][monster5] = dropConf[str(monster5)]
	else: 
		wave['monster'][monster5] = {}
			
	wave['boss'] = {}
			
	boss1 = row[idx + 5]
	boss2 = row[idx + 6]
	boss3 = row[idx + 7]
	boss4 = row[idx + 8]
	boss5 = row[idx + 9]
	boss6 = row[idx + 10]
	
	if dropConf.has_key(str(boss1)):
		wave['monster'][boss1] = dropConf[str(boss1)]
	else: 
		wave['monster'][boss1] = {}
		
	if dropConf.has_key(str(boss2)):
		wave['monster'][boss2] = dropConf[str(boss2)]
	else: 
		wave['monster'][boss2] = {}
		
	if dropConf.has_key(str(boss3)):
		wave['monster'][boss3] = dropConf[str(boss3)]
	else: 
		wave['monster'][boss3] = {}
		
	if dropConf.has_key(str(boss4)):
		wave['monster'][boss4] = dropConf[str(boss4)]
	else: 
		wave['monster'][boss4] = {}
		
	if dropConf.has_key(str(boss5)):
		wave['monster'][boss5] = dropConf[str(boss5)]
	else: 
		wave['monster'][boss5] = {}
		
	if dropConf.has_key(str(boss6)):
		wave['monster'][boss6] = dropConf[str(boss6)]
	else: 
		wave['monster'][boss6] = {}
	
	if monster1 == '' or monster1 == '0' and boss1 == '' or boss1 == '0':		
		return None	
	
	ls = str(row[idx + 11]).split(',')
	wave['count'] =  [ int( eval(x) ) for x in ls if x ]
	ls = str(row[idx + 12]).split(',')
	wave['count_prob'] = [ int( eval(x) ) for x in ls if x ]
	wave['more'] = int(row[idx + 13])
	return wave