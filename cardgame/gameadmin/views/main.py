#coding:utf-8
#!/usr/bin/env python

from django.shortcuts import render
from gclib.DBConnection import DBConnection
from django.http import HttpResponse
from gclib.json import json
from gclib.config import config
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
1
def garcha(request):
	return generalConfigRequestProcess(request, 'garcha')	
	
def equipment(request):
	return generalConfigRequestProcess(request, 'equipment')

def strength_probability(request):
	return generalConfigRequestProcess(request, 'strength_probability')

def strength_price(request):
	return generalConfigRequestProcess(request, 'strength_price')

def luckycat_level(request):
	return generalConfigRequestProcess(request, 'luckycat_level')
	
def luckycat_bless(request):
	return generalConfigRequestProcess(request, 'luckycat_bless')

def luckycat_fortune(request):
	return generalConfigRequestProcess(request, 'luckycat_fortune')
	
def luck(request):
	return generalConfigRequestProcess(request, 'luck')
	
def language(request):
	return generalConfigRequestProcess(request, 'language')
	
def stone(request):
	return generalConfigRequestProcess(request, 'stone')
	
def stone_probability(request):
	return generalConfigRequestProcess(request, 'stone_probability')
	
def stone_level(request):
	return generalConfigRequestProcess(request, 'stone_level')
	
def trp_price(request):
	return generalConfigRequestProcess(request, 'trp_price')

def trp(request):
	return generalConfigRequestProcess(request, 'trp')
				
def generalConfigRequestProcess(request, confname):
	if request.method == 'POST':
		confstr = request.POST['config']
		try:
			config.setConfig(confname, confstr)		
			return render(request, 'index.html', {})
		except:
			return render(request, confname + '.html', {'config':confstr})
	else:
		confstr = config.getConfigStr(confname)		
		if confstr != None:			
			return render(request, confname + '.html', {'config': confstr})
		else:
			config.createConfig(confname)			
			return render(request, confname + '.html', {'config':''})

def monster_import(request):
	if request.method == 'POST':
		monster_file = request.FILES.get('monster_file')
		if monster_file == None:
			return HttpResponse('怪物xlsx文件未上传')
		
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, monster_file.read())
		
		sheet = wb.sheet_by_index(2)
		conf = {}
				
		for rownum in range(3, sheet.nrows):
			row = sheet.row_values(rownum)
			monsterId = row[0]
			imageId = row[1]
			icon = row[2]
			name = row[3]
			type = row[5]
			nature = row[7]
			distance = row[8]
			level = row[9]
			hp = row[10]
			attack = row[11]
			recovery = row[12]
			agile = row[13]
			prob = row[14]
			skillId = []
			skillId.append(row[15])
			if row[16] != '':
				skillId.append(row[16])
			if row[17] != '':
				skillId.append(row[17])
			if row[18] != '':
				skillId.append(row[18])
			
			monsterConf = {}
			monsterConf['monsterId'] = monsterId
			monsterConf['imageId'] = imageId
			monsterConf['icon'] = icon
			monsterConf['name'] = name
			monsterConf['type'] = type
			monsterConf['nature'] = nature
			monsterConf['distance'] = distance
			monsterConf['level'] = level
			monsterConf['hp'] = hp
			monsterConf['attack'] = attack
			monsterConf['recovery'] = recovery
			monsterConf['agile'] = agile
			monsterConf['probability'] = prob
			monsterConf['skillId'] = skillId
			conf[monsterId] = monsterConf
		return HttpResponse(json.dumps(conf))
	return HttpResponse('monster_import')
			
			
def garcha_import(request):
	if request.method == 'POST':
		garcha_file = request.FILES.get('garcha_file')
		if garcha_file == None:
			return HttpResponse('抽奖武将xlsx文件未上传')
			
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, garcha_file.read())
		sheets = []
		sheets.append(wb.sheet_by_index(0))
		sheets.append(wb.sheet_by_index(1))
		sheets.append(wb.sheet_by_index(2))
		sheets.append(wb.sheet_by_index(3))
		sheets.append(wb.sheet_by_index(4))
		
		conf = []
		for sheet in sheets:
			garchaCataConf = {}
			cardConf = []
			total_prob = 0
			for rownum in range(4, sheet.nrows):
				row = sheet.row_values(rownum)
				cardid = row[0]
				name = row[1]				
				level = row[2]				
				prob = row[3]
				
				key = int(prob)
				garchaConf = {}
				garchaConf['cardId'] = cardid
				garchaConf['name'] = name				
				garchaConf['level'] = level
				garchaConf['prob'] = prob
				total_prob = total_prob + prob
				cardConf.append(garchaConf)				
			garchaCataConf['card'] = cardConf
			garchaCataConf['totalProb'] = total_prob
			conf.append(garchaCataConf)
		return HttpResponse(json.dumps(conf))
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
			
		return HttpResponse(json.dumps(conf))
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
			conf[str(int(level))] = levelConf
		return HttpResponse(json.dumps(conf))
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
		
		return HttpResponse(json.dumps(conf))
		
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
			petid = unicode(row[3])
			model = unicode(row[4])
			icon = unicode(row[5])
			name = unicode(row[6])
			type = unicode(row[8])
			nature = unicode(row[11])
			attacktype = int(row[12])
			control = int(row[13])
			controllevel = int(row[14])
			immunity = int(row[15])
			immunitylevel = int(row[16])
			star = int(row[17])
			strength = int(row[18])
			intelligence = int(row[19])
			artifice = int(row[20])
			hit = int(row[21])
			dodge = int(row[22])
			critical = int(row[23])
			tenacity = int(row[24])
			block = int(row[25])
			wreck = int(row[26])
			maxlevel = int(row[27])
			hp = int(row[28])
			hpgrowth = int(row[29])
			attack = int(row[30])
			attackgrowth = int(row[31])
			pr = int(row[32])	#Physical Resistance
			prgrowth = int(row[33])
			mr = int(row[34])
			mrgrowth = int(row[35])	#Magical Resistance
			pa = int(row[36])	#Physical Amplification
			pagrowth = int(row[37])
			ma = int(row[38])	#Magical Amplification
			magrowth = int(row[39])			
			skillid = [unicode(row[40])]
			if unicode(row[41]):
				skillid.append(unicode(row[41]))
			if unicode(row[42]):
				skillid.append(unicode(row[42]))
			if unicode(row[43]):
				skillid.append(unicode(row[43]))
			evoId = unicode(row[44])
			evoObjectId = []
			if row[45]:
				evoObjectId.append(unicode(row[45]))
			if row[46]:
				evoObjectId.append(unicode(row[46]))
			if row[47]:
				evoObjectId.append(unicode(row[47]))
			if row[48]:
				evoObjectId.append(unicode(row[48]))
			evoPrice = int(row[49])
			desc = unicode(row[50])
			luck = []
			if unicode(row[51]):
				luck.append(unicode(row[51]))
			if unicode(row[52]):
				luck.append(unicode(row[52]))
			if unicode(row[53]):
				luck.append(unicode(row[53]))
			if unicode(row[54]):
				luck.append(unicode(row[54]))
			petConf = {}
			petConf['model'] = model
			petConf['icon'] = icon
			petConf['name'] = name
			petConf['type'] = type
			petConf['nature'] = nature
			petConf['attacktype'] = attacktype
			petConf['control'] = control
			petConf['controllevel'] = controllevel
			petConf['immunity'] = immunity			
			petConf['immunitylevel'] = immunitylevel
			petConf['star'] = star
			petConf['strength'] = strength
			petConf['intelligence'] = intelligence
			petConf['artifice'] = artifice
			petConf['hit'] = hit
			petConf['dodge'] = dodge
			petConf['critical'] = critical
			petConf['tenacity'] = tenacity
			petConf['block'] = block
			petConf['wreck'] = wreck			
			petConf['maxlevel'] = maxlevel
			petConf['hp'] = hp
			petConf['hpgrowth'] = hpgrowth			
			petConf['attack'] = attack
			petConf['attackgrowth'] = attackgrowth
			petConf['pr'] = pr
			petConf['prgrowth'] = prgrowth
			petConf['mr'] = mr
			petConf['mrgrowth'] = mrgrowth
			petConf['pa'] = pa
			petConf['pagrowth'] = pagrowth
			petConf['ma'] = ma
			petConf['magrowth'] = magrowth			
			petConf['skillid'] = skillid
			petConf['evoId'] = evoId
			petConf['evoObjectId'] = evoObjectId
			petConf['evoPrice'] = evoPrice
			petConf['desc'] = desc
			petConf['luck'] = luck
			conf[str(petid)] = petConf
		return HttpResponse(json.dumps(conf))
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
			star5Exp = int(row[5])
			levelConf = [star1Exp, star2Exp, star3Exp, star4Exp, star5Exp]			
			conf[str(level)] = levelConf
		return HttpResponse(json.dumps(conf))
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
		return HttpResponse(json.dumps(Conf))
	return HttpResponse('dungeon_import')
	
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
		if boss1 != '' and boss1 != '0.0':
			wave['boss'][boss1] = {}
		
	if dropConf.has_key(str(boss2)):
		wave['boss'][boss2] = dropConf[str(boss2)]
	else:
		if boss2 != '' and boss2 != '0.0':
			wave['boss'][boss2] = {}
		
	if dropConf.has_key(str(boss3)):
		wave['boss'][boss3] = dropConf[str(boss3)]
	else:
		if boss3 != '' and boss3 != '0.0':
			wave['boss'][boss3] = {}
		
	if dropConf.has_key(str(boss4)):
		wave['boss'][boss4] = dropConf[str(boss4)]
	else: 
		if boss4 != '' and boss4 != '0.0':
			wave['boss'][boss4] = {}
		
	if dropConf.has_key(str(boss5)):
		wave['boss'][boss5] = dropConf[str(boss5)]
	else: 
		if boss5 != '' and boss5 != '0.0':
			wave['boss'][boss5] = {}
		
	if dropConf.has_key(str(boss6)):
		wave['boss'][boss6] = dropConf[str(boss6)]
	else:
		if boss6 != '' and boss6 != '0.0':
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
	
def equipment_import(request):
	if request.method == 'POST':
		equipment_file = request.FILES.get('equipment_file')
		if equipment_file == None:
			return HttpResponse('装备xlsx文件未上传')			
	
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, equipment_file.read())
		sheet = wb.sheet_by_index(0)
	
		conf = {}
		for rownum in range(4,sheet.nrows):
			row = sheet.row_values(rownum)
			eqid = row[0]
			name = row[1]
			icon = row[2]
			type = row[3]
			position = row[4]
			stack = row[5]
			nature = row[7]
			quality = row[9]
			levelreq = row[10]			
			hp = row[11]
			hpgrowth = row[12]
			pa = row[13]
			pagrowth = row[14]
			ma = row[15]
			magrowth = row[16]
			pd = row[17]
			pdgrowth = row[18]
			md = row[19]
			mdgrowth = row[20]
			pt = row[21]
			ptgrowth = row[22]
			mt = row[23]
			mtgrowth = row[24]
			price = row[28]
			desc = row[29]
			
			
			equipmentConf = {}
			equipmentConf['eqid'] = eqid
			equipmentConf['name'] = name
			equipmentConf['icon'] = icon
			equipmentConf['type'] = type
			equipmentConf['position'] = int(position)
			equipmentConf['stack'] = stack
			equipmentConf['nature'] = nature
			equipmentConf['quality'] = quality
			equipmentConf['levelreq'] = int(levelreq)			
			equipmentConf['hp'] = int(hp)
			equipmentConf['hpgrowth'] = int(hpgrowth)
			equipmentConf['pa'] = int(pa)
			equipmentConf['pagrowth'] = int(pagrowth)
			equipmentConf['ma'] = int(ma)
			equipmentConf['magrowth'] = int(magrowth)
			equipmentConf['pd'] = int(pd)
			equipmentConf['pdgrowth'] = int(pdgrowth)
			equipmentConf['md'] = int(md)
			equipmentConf['mdgrowth'] = int(mdgrowth)
			equipmentConf['pt'] = int(pt)
			equipmentConf['ptgrowth'] = int(ptgrowth)
			equipmentConf['mt'] = int(mt)
			equipmentConf['mtgrowth'] = int(mtgrowth)			
			equipmentConf['price'] = int(price)
			equipmentConf['desc'] = desc			
			
			conf[eqid] = equipmentConf
		return HttpResponse(json.dumps(conf))
	return HttpResponse('equipment_import')
	
	
def strength_price_import(request):
	if request.method == 'POST':
		strength_price_file = request.FILES.get('strength_price_file')
		if strength_price_file == None:
			return HttpResponse('强化价格xlsx文件未上传')			
	
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, strength_price_file.read())
		sheet = wb.sheet_by_index(1)
	
		conf = {}
		for rownum in range(3,sheet.nrows):
			row = sheet.row_values(rownum)
		
			quality = row[1]
			level = int(row[2])
			price = int(row[3])
			probability = int(row[4])
		
			if level < 1:
				return HttpResponse('level can not less 1')
			if not conf.has_key(quality):
				conf[quality] = []
		
			priceConf = conf[quality]
			
			while len(priceConf) < level:
				priceConf.append({})			
			priceConf[level - 1] = {'price':price}
			
		return HttpResponse(json.dumps(conf))
	return HttpResponse('strength_price_import')
	
	
def luckycat_level_import(request):
	if request.method == 'POST':
		luckycat_level_file = request.FILES.get('luckycat_level_file')
		if luckycat_level_file == None:
			return HttpResponse('招财猫等级xlsx文件未上传')			
	
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, luckycat_level_file.read())
		sheet = wb.sheet_by_index(0)
	
		conf = []
		for rownum in range(3,sheet.nrows):
			row = sheet.row_values(rownum)
			
			level = int(row[0])
			exp = int(row[1])
			levelupgold = int(row[2])
			luckygold = int(row[3])
			
			while(level >= len(conf)):
				conf.append({})
			
			levelConf = {}
			levelConf['level'] = level
			levelConf['exp'] = exp
			levelConf['levelupGold'] = levelupgold
			levelConf['luckyGold'] = luckygold
			
			conf[level - 1] = levelConf
			
		return HttpResponse(json.dumps(conf))
	return HttpResponse('luckycat_level_import')
			
def luckycat_bless_import(request):
	if request.method == 'POST':
		luckycat_bless_file = request.FILES.get('luckycat_bless_file')
		if luckycat_bless_file == None:
			return HttpResponse('招财猫祝福xlsx文件未上传')			
	
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, luckycat_bless_file.read())
		sheet = wb.sheet_by_index(2)
	
		conf = {}
		for rownum in range(3,sheet.nrows):
			row = sheet.row_values(rownum)
			
			blessid = row[0]
			blessName = row[1]
			icon = row[2]
			desc = row[3]
			probability = row[4]
			price = row[5]
			
			blessConf = {}
			blessConf['blessid'] = blessid
			blessConf['name'] = blessName
			blessConf['icon'] = icon
			blessConf['desc'] = desc
			blessConf['probability'] = probability
			blessConf['price'] = price
			conf[blessid] = blessConf
			
		return HttpResponse(json.dumps(conf))
	return HttpResponse('luckycat_bless_import')
	
def luck_import(request):
	if request.method == 'POST':
		luck_file = request.FILES.get('luck_file')
		if luck_file == None:
			return HttpResponse('缘xlsx文件未上传')			
	
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, luck_file.read())
		sheet = wb.sheet_by_index(0)
				
		conf = {}
		for rownum in range(4,sheet.nrows):
			row = sheet.row_values(rownum)			
			luckid = row[0]
			name = row[1]			
			typestr =  row[3]
			type = row[4]
			valuetype = row[5]
			value = row[6]			
			luckConf = {}
			luckConf['luckid'] = luckid
			luckConf['name'] = name
			luckConf['typestr'] = typestr
			luckConf['valuetype'] = valuetype
			luckConf['type'] = type	
			luckConf['value'] = value
			conf[luckid] = luckConf
			
		return HttpResponse(json.dumps(conf))
	return HttpResponse('luck_import')
	
	
def language_import(request):
	if request.method == 'POST':
		language_file = request.FILES.get('language_file')
		if not language_file:
			return HttpResponse('语言xlsx文件未上传')			
	
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, language_file.read())
		sheet = wb.sheet_by_index(0)
				
		conf = {}
		for rownum in range(4,sheet.nrows):
			row = sheet.row_values(rownum)
						
			strid = row[1]
			chinese = row[2]
			lanConf = {}
			#lanConf['strid'] = strid
			lanConf['chinese'] = chinese
			conf[strid] = lanConf
		return HttpResponse(json.dumps(conf))
	return HttpResponse('language_import')
	
def stone_import(request):
	if request.method == 'POST':
		stone_file = request.FILES.get('stone_file')
		if not stone_file:
			return HttpResponse('宝石xlsx文件上传')
		
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, stone_file.read())
		sheet = wb.sheet_by_index(2)
				
		conf = {}
		for rownum in range(5,sheet.nrows):
			row = sheet.row_values(rownum)
			stoneid = row[0]
			quality = row[3]
			name = row[4]
			icon = row[5]			
			typestr = row[6]
			type = row[7]
			value = row[8]
			gravel = row[9]
			
			stoneConf = {}
			stoneConf['stoneid'] = stoneid
			stoneConf['quality'] = quality
			stoneConf['name'] = name
			stoneConf['icon'] = icon
			stoneConf['typestr'] = typestr
			stoneConf['type'] = type
			stoneConf['value'] = value
			stoneConf['gravel'] = gravel
			
			conf[stoneid] = stoneConf
			
		return HttpResponse(json.dumps(conf))
	return HttpResponse('stone_import')
	
	
def stone_probability_import(request):
	if request.method == 'POST':
		stone_probability_file = request.FILES.get('stone_probability_file')
		if not stone_probability_file:
			return HttpResponse('宝石概率xlsx文件上传')
		
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, stone_probability_file.read())
		sheet = wb.sheet_by_index(1)
				
		conf = {}
		
		visitProbRow = sheet.row_values(2)
		
		visit1Prob = int(visitProbRow[1])
		visit2Prob = int(visitProbRow[2])
		visit3Prob = int(visitProbRow[3])
		visit4Prob = int(visitProbRow[4])
		visit5Prob = int(visitProbRow[5])
		
		conf['visitProb'] = [visit1Prob, visit2Prob, visit3Prob, visit4Prob, visit5Prob]
		
		visitPriceRow = sheet.row_values(3)
		visit1Price = int(visitPriceRow[1])
		visit2Price = int(visitPriceRow[2])
		visit3Price = int(visitPriceRow[3])
		visit4Price = int(visitPriceRow[4])
		visit5Price = int(visitPriceRow[5])
		
		conf['visitPrice'] = [visit1Price, visit2Price, visit3Price, visit4Price, visit5Price]

		stoneCol = sheet.col_values(0)
		level1Col = sheet.col_values(1)
		level2Col = sheet.col_values(2)
		level3Col = sheet.col_values(3)
		level4Col = sheet.col_values(4)
		
		conf['visit'] = []
		
		read_stone_level(stoneCol, level1Col, conf, 1)
		read_stone_level(stoneCol, level2Col, conf, 2)
		read_stone_level(stoneCol, level3Col, conf, 3)
		read_stone_level(stoneCol, level4Col, conf, 4)			
		return HttpResponse(json.dumps(conf))
	return HttpResponse('stone_probability_import')

def read_stone_level(stoneCol, levelCol, conf, level):
	
	visitConf = {}	
	visitConf['gold'] = []
	visitConf['gem'] = []	
	
	for rownum in range(5, 10):
		levelgoldInfo = {}
		levelgoldInfo['probability'] = int(levelCol[rownum])
		levelgoldInfo['stone'] = stoneCol[rownum].split(',')
		visitConf['gold'].append(levelgoldInfo)
			
	for rownum in range(12, 18):
		levelgoldInfo = {}
		levelgoldInfo['probability'] = int(levelCol[rownum])
		levelgoldInfo['stone'] = stoneCol[rownum].split(',')
		visitConf['gem'].append(levelgoldInfo)
	conf['visit'].append(visitConf)
		
		
def stone_level_import(request):
	if request.method == 'POST':
		stone_level_file = request.FILES.get('stone_level_file')
		if not stone_level_file:
			return HttpResponse('宝石等级xlsx文件上传')
		
		
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, stone_level_file.read())
		sheet = wb.sheet_by_index(0)
				
		conf = {}
		
		for rownum in range(2,sheet.nrows):
			row = sheet.row_values(rownum)
			conf[str(rownum - 1)] = row[1:5]
				
		return HttpResponse(json.dumps(conf))
	return HttpResponse('stone_level_import')
	
def trp_price_import(request):
	if request.method == 'POST':
		trp_price_file = request.FILES.get('trp_price_file')
		if not trp_price_file:
			return HttpResponse('培养价格xlsx文件上传')
		
		
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, trp_price_file.read())
		sheet = wb.sheet_by_index(0)
				
		conf = []
		
		for rownum in range(3,sheet.nrows):
			row = sheet.row_values(rownum)
			level = int(row[0])
			price = int(row[1])
			
			while len(conf) < level:
				conf.append(0)
				
			conf[level -1] = price
			
		return HttpResponse(json.dumps(conf))
	return HttpResponse('trp_price_import')
	

	
def trp_import(request):
	if request.method == 'POST':
		trp_file = request.FILES.get('trp_file')
		if not trp_file:
			return HttpResponse('培养点xlsx文件上传')
		
		
		wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, trp_file.read())
		sheet = wb.sheet_by_index(1)
				
		conf = []
		
		for rownum in range(3,sheet.nrows):
			row = sheet.row_values(rownum)
			
			level = int(row[0])
			card_trp = int(row[1])
			skill_trp = int(row[2])
			while len(conf) < level:
				conf.append({})
			
			conf[level - 1] = {'card':card_trp, 'skill':skill_trp}
			
		return HttpResponse(json.dumps(conf))
	return HttpResponse('trp_import')
