#coding:utf-8
#!/usr/bin/env python

import sys
import xlrd
from xlrd import USE_MMAP
from django.http import HttpResponse
from gclib.json import json
from gclib.utility import str_to_time

class excel_import:
	@staticmethod
	def monster_import(request):
		if request.method == 'POST':
			monster_file = request.FILES.get('monster_file')
			if not monster_file:
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
				level = int(row[8])
				star = int(row[9])
				attackType = int(row[10])
				position = int(row[11])
				immunity = int(row[12])
				strength = int(row[13])
				intelligence = int(row[14])
				artifice = int(row[15])
				hit = int(row[16])
				dodge = int(row[17])
				critical = int(row[18])
				tenacity = int(row[19])
				block =  int(row[20])
				wreck = int(row[21])
				hp = int(row[22])
				attack = int(row[23])
				pr = int(row[24])
				mr = int(row[25])
				pa = int(row[26])
				#ma = int(row[27])
				pe = int(row[28])				#Pysical Extra
				#me = int(row[29])				#Magical Extra
				pi = int(row[30])				#Pysical Immune
				#mi = int(row[31])				#Magical Immune
				
				skill = []
				if row[32] and row[36] and row[41]:
					skill.append({'id':row[32], 'level':int(row[36]), 'probability':int(row[41])})
				if row[33] and row[37] and row[42]:
					skill.append({'id':row[33], 'level':int(row[37]), 'probability':int(row[42])})
				if row[34] and row[38] and row[43]:
					skill.append({'id':row[34], 'level':int(row[38]), 'probability':int(row[43])})
				if row[35] and row[39] and row[44]:
					skill.append({'id':row[35], 'level':int(row[39]), 'probability':int(row[44])})
				
				dropid = row[40]
				
				pt = int(row[45])
				#mt = int(row[46])
				pd = int(row[47])
				md = int(row[48])				
				
				monsterConf = {}
				monsterConf['monsterId'] = monsterId
				monsterConf['imageId'] = imageId
				monsterConf['icon'] = icon
				monsterConf['name'] = name
				monsterConf['type'] = type
				monsterConf['nature'] = nature
				monsterConf['level'] = level
				monsterConf['star'] = star
				monsterConf['attackType'] = attackType
				monsterConf['position'] = position
				monsterConf['immunity'] = immunity
				monsterConf['strength'] = strength
				monsterConf['intelligence'] = intelligence
				monsterConf['artifice'] = artifice
				monsterConf['hit'] = hit
				monsterConf['dodge'] = dodge
				monsterConf['critical'] = critical
				monsterConf['tenacity'] = tenacity
				monsterConf['block'] = block
				monsterConf['wreck'] = wreck
				monsterConf['hp'] = hp
				monsterConf['attack'] = attack
				monsterConf['pr'] = pr
				monsterConf['mr'] = mr
				monsterConf['pa'] = pa
				#monsterConf['ma'] = ma
				monsterConf['pe'] = pe
				#monsterConf['me'] = me
				monsterConf['pi'] = pi
				#monsterConf['mi'] = mi
				monsterConf['level'] = level
				monsterConf['hp'] = hp
				monsterConf['attack'] = attack
				monsterConf['pr'] = pr
				monsterConf['mr'] = mr
				monsterConf['pa'] = pa
				#monsterConf['ma'] = ma
				monsterConf['skill'] = skill
				monsterConf['pt'] = pt
				#monsterConf['mt'] = mt
				monsterConf['pd'] = pd
				monsterConf['md'] = md
				conf[monsterId] = monsterConf
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('monster_import')
				
	@staticmethod
	def garcha_import(request):
		if request.method == 'POST':
			garcha_file = request.FILES.get('garcha_file')
			if not garcha_file:
				return HttpResponse('抽奖武将xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, garcha_file.read())
			sheet = wb.sheet_by_index(0)
			
			conf = []
			for rownum in range(1,sheet.nrows):
				row = sheet.row_values(rownum)
				
				vip_level = int(row[0])
				garcha_10000_free_time_score = int(row[1])
				garcha_10000_time_score = int(row[2])
				garcha_10000_free_luck_score = int(row[3])
				garcha_10000_luck_score = int(row[4])
				garcha_100_free_time_score = int(row[5])
				garcha_100_time_score = int(row[6])
				garcha_100_free_luck_score = int(row[7])
				garcha_100_luck_score = int(row[8])
				
				garchaConf = {}
				garchaConf['garcha_10000_free_time_score'] = garcha_10000_free_time_score
				garchaConf['garcha_10000_time_score'] = garcha_10000_time_score
				garchaConf['garcha_10000_free_luck_score'] = garcha_10000_free_luck_score
				garchaConf['garcha_10000_luck_score'] = garcha_10000_luck_score
				garchaConf['garcha_100_free_time_score'] = garcha_100_free_time_score
				garchaConf['garcha_100_time_score'] = garcha_100_time_score
				garchaConf['garcha_100_free_luck_score'] = garcha_100_free_luck_score
				garchaConf['garcha_100_luck_score'] = garcha_100_luck_score
				
				while len(conf) < vip_level + 1:
					conf.append({})
				
				conf[vip_level]	= garchaConf
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('garcha_import')	
		
				
				
#			sheets = []
#			sheets.append(wb.sheet_by_index(0))
#			sheets.append(wb.sheet_by_index(1))
#			sheets.append(wb.sheet_by_index(2))
#			sheets.append(wb.sheet_by_index(3))
#			sheets.append(wb.sheet_by_index(4))
#			
#			conf = []
#			for sheet in sheets:s
#				garchaCataConf = {}
#				cardConf = []
#				total_prob = 0
#				for rownum in range(4, sheet.nrows):
#					row = sheet.row_values(rownum)
#					cardid = row[0]
#					name = row[1]				
#					level = row[2]				
#					prob = row[3]					
#					key = int(prob)
#					garchaConf = {}
#					garchaConf['cardId'] = cardid
#					garchaConf['name'] = name				
#					garchaConf['level'] = level
#					garchaConf['prob'] = prob
#					total_prob = total_prob + prob
#					cardConf.append(garchaConf)				
#				garchaCataConf['card'] = cardConf
#				garchaCataConf['totalProb'] = total_prob
#				conf.append(garchaCataConf)
#			return HttpResponse(json.dumps(conf, sort_keys=True))
#		return HttpResponse('garcha_import')
	
	@staticmethod
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
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('prompt_import')
	
	@staticmethod
	def level_import(request):
		if request.method == 'POST':
			level_file = request.FILES.get('level_file')
			if not level_file:
				return HttpResponse('等级xlsx文件未上传')			
		
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, level_file.read())
			sheet = wb.sheet_by_index(0)
		
			conf = []
			for rownum in range(5,sheet.nrows):
				row = sheet.row_values(rownum)
				level = int(row[0])
				exp = int(row[1])
				stamina = int(row[2])
				sp = int(row[3])
				friend = int(row[4])
				
				levelConf = {}
				levelConf['levelExp'] = exp
				levelConf['stamina'] = stamina
				levelConf['sp'] = sp
				levelConf['friend'] = friend
				
				while len(conf) < level:
					conf.append({})
					
				conf[level - 1] = levelConf
							
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('prompt_import')
		
	@staticmethod
	def skill_import(request):
		if request.method == 'POST':
			skill_file = request.FILES.get('skill_file')		
			if not skill_file:
				return HttpResponse('技能xlsx文件未上传')
								
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, skill_file.read())			
			sheet = wb.sheet_by_index(0)		
			
			conf = {}
			for rownum in range(4,sheet.nrows):
				row = sheet.row_values(rownum)	
				skillid = row[0]
				name = row[1]
				icon = row[2]
				cooldown = row[3]
				quality = row[4]
				initExp = row[5]
				type = row[6]
				desc = row[7]
				nature = row[9]
				maxLevel = row[10]
				triggerType = row[11]
				isActive = row[12]
				#startEffect = row[13]
				#inprocessEffect = row[14]
				#finishEffect = row[15]
				result = []
				if row[16]:
					result.append(row[16])
				if row[17]:
					result.append(row[17])
				if row[18]:
					result.append(row[18])
				if row[19]:
					result.append(row[19])			
				if row[20]:
					result.append(row[20])
				mp = int(row[21])
				exp = int(row[22])
				probability = int(row[23])
				chip = int(row[24])
				position = int(row[25])
					
				skillConf = {}
				skillConf['name'] = name
				skillConf['icon'] = icon
				skillConf['cooldown'] = cooldown
				skillConf['quality'] = quality
				skillConf['initExp'] = initExp
				skillConf['type'] = type
				skillConf['desc'] = desc
				skillConf['nature'] = nature
				skillConf['maxLevel'] = maxLevel
				skillConf['triggerType'] = triggerType
				skillConf['isActive'] = isActive
#				skillConf['startEffect'] = startEffect
#				skillConf['inprocessEffect'] = inprocessEffect
#				skillConf['finishEffect'] = finishEffect
				skillConf['result'] = result				
				skillConf['mp'] = mp
				skillConf['exp'] = exp
				skillConf['probability'] = probability
				skillConf['chip'] = chip
				skillConf['position'] = position
				
				conf[unicode(skillid)] = skillConf
			
			return HttpResponse(json.dumps(conf, sort_keys=True))			
		return HttpResponse('skill_import')
		
	@staticmethod
	def skill_level_import(request):
		if request.method == 'POST':
			skill_level_file = request.FILES.get('skill_level_file')		
			if not skill_level_file:
				return HttpResponse('技能等级xlsx文件未上传')
								
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, skill_level_file.read())
			sheet = wb.sheet_by_index(3)		
			
			conf = []
			for rownum in range(4,sheet.nrows):
				row = sheet.row_values(rownum)				
				level = int(row[0])
				exp = int(row[1])
				while len(conf) < level:
					conf.append({})				
				conf[level - 1] = exp			
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('skill_level_import')	
		
		
	@staticmethod
	def skill_effect_import(request):
		if request.method == 'POST':
			skill_effect_file = request.FILES.get('skill_effect_file')		
			if not skill_effect_file:
				return HttpResponse('技能效果xlsx文件未上传')
								
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, skill_effect_file.read())
			sheet = wb.sheet_by_index(1)			
			conf = {}
			for rownum in range(4,sheet.nrows):
				row = sheet.row_values(rownum)
				skillEffid = row[0]
				fcId = row[1]
				fcSuit = int(row[3])
				valueType = int(row[5])
				coefficient = float(row[6])
				fcValue = int(row[7])
				Lvup = float(row[8])
				buffId = row[9]
				fcDuration = int(row[10])
				isDisperse = int(row[11])
				triggerType = int(row[12])
				
				skillEffectConf = {}
				skillEffectConf['fcId'] = fcId
				skillEffectConf['fcSuit'] = fcSuit
				skillEffectConf['valueType'] = valueType
				skillEffectConf['coefficient'] = coefficient
				skillEffectConf['fcValue'] = fcValue
				skillEffectConf['Lvup'] = Lvup
				skillEffectConf['buffId'] = buffId
				skillEffectConf['fcDuration'] = fcDuration
				skillEffectConf['isDisperse'] = isDisperse
				skillEffectConf['triggerType'] = triggerType
				
				conf[skillEffid] = skillEffectConf
				
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('skill_effect_import')
				
	@staticmethod
	def pet_import(request):
		if request.method == 'POST':
			pet_file = request.FILES.get('pet_file')
			if not pet_file:
				return HttpResponse('宠物xlsx文件未上传')
			
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
				quality = int(row[17])
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
				attackgrowth = float(row[31])
				pr = int(row[32])	#Physical Resistance
				prgrowth = int(row[33])
				mr = int(row[34])
				mrgrowth = int(row[35])	#Magical Resistance
				pa = int(row[36])	#Physical Amplification
				pagrowth = int(row[37])
				#ma = int(row[38])	#Magical Amplification
				#magrowth = int(row[39])			
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
				chip = int(row[56])
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
				petConf['quality'] = quality
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
				#petConf['ma'] = ma
				#petConf['magrowth'] = magrowth			
				petConf['skillid'] = skillid
				petConf['evoId'] = evoId
				petConf['evoObjectId'] = evoObjectId
				petConf['evoPrice'] = evoPrice
				petConf['desc'] = desc
				petConf['luck'] = luck				
				petConf['chip'] = chip
				conf[str(petid)] = petConf
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('pet_import')
								
	@staticmethod		
	def pet_level_import(request):
		if request.method == 'POST':
			pet_level_file = request.FILES.get('pet_level_file')
			if not pet_level_file:
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
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('pet_level_import')
					
	@staticmethod
	def dungeon_import(request):
		if request.method == 'POST':
			dungeon_file = request.FILES.get('dungeon_file')		
			if not dungeon_file:
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
				dropid = row[40]				
				dropConf[str(monsterId)] = dropid				
			
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
				dayCount = int(row[10])
				stamina = int(row[11])
				exp = int(row[13])
				difficult = int(row[14])
				mayDrop1 = row[15]
				mayDrop2 = row[16]
				dropId = row[17]
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
				fieldConf['dayCount'] = dayCount
				#fieldConf['difficult'] = difficult
				fieldConf['mayDrop'] = [mayDrop1, mayDrop2]
				fieldConf['dropid'] = dropId
				fieldConf['wave'] = excel_import.read_waves(row, dropConf)
				dunConf['field'].append(fieldConf)
			Conf.append(dunConf)			
			return HttpResponse(json.dumps(Conf, sort_keys=True))
		return HttpResponse('dungeon_import')
		
	@staticmethod
	def read_waves(row, dropConf):	
		waveConf = []			
		wave = excel_import.read_wave(row, 20, dropConf)
		if wave:
			waveConf.append(wave)	
			wave = excel_import.read_wave(row, 35, dropConf)
			if wave:
				waveConf.append(wave)
				wave = excel_import.read_wave(row, 50, dropConf)
				if wave:
					waveConf.append(wave)
			#		wave = excel_import.read_wave(row, 65, dropConf)	
			#		if wave:
			#			waveConf.append(wave)
			#			wave = excel_import.read_wave(row, 80, dropConf)
			#			if wave:
			#				waveConf.append(wave)
			#				wave = excel_import.read_wave(row, 95, dropConf)
			#				if wave:
			#					waveConf.append(wave)
			#					wave = excel_import.read_wave(row, 110, dropConf)
			#					if wave:
			#						waveConf.append(wave)
			#						wave = excel_import.read_wave(row, 125, dropConf)
			#						if wave:
			#							waveConf.append(wave)	
		return waveConf
		
	@staticmethod
	def read_wave(row, idx, dropConf):
		wave = {}
		wave['monster'] = []
		wave['drop'] = {}
		monster1 = str(row[idx + 0])
		monster2 = str(row[idx + 1])
		monster3 = str(row[idx + 2])
		monster4 = str(row[idx + 3])
		monster5 = str(row[idx + 4])
		monster6 = str(row[idx + 5])
		
		boss1 = str(row[idx + 6])
		boss2 = str(row[idx + 7])
		boss3 = str(row[idx + 8])
		boss4 = str(row[idx + 9])
		boss5 = str(row[idx + 10])
		boss6 = str(row[idx + 11])
		
		if (monster1 == '' or monster1 == '0' or monster1 == '0.0') and (boss1 == '' or boss1 == '0' or boss1 == '0.0'):		
			return None	
		
		
		if monster1 != '' and monster1 != '0.0':
			if dropConf.has_key(monster1):				
				wave['drop'][monster1] = dropConf[monster1]
			wave['monster'].append(monster1)		
		
		if monster2 != '' and monster2 != '0.0':
			if dropConf.has_key(monster2):
				wave['drop'][monster2] = dropConf[monster2]				
			wave['monster'].append(monster2)
			
		if monster3 != '' and monster3 != '0.0':
			if dropConf.has_key(monster3):
				wave['drop'][monster3] = dropConf[monster3]
			wave['monster'].append(monster3)		
			
		if monster4 != '' and monster4 != '0.0':
			if dropConf.has_key(monster4):
				wave['drop'][monster4] = dropConf[monster4]
			wave['monster'].append(monster4)
					
		if monster5 != '' and monster5 != '0.0':
			if dropConf.has_key(monster5):
				wave['drop'][monster5] = dropConf[monster5]
			wave['monster'].append(monster5)
		
		if monster6 != '' and monster6 != '0.0':
			if dropConf.has_key(monster6):
				wave['drop'][monster6] = dropConf[monster6]
			wave['monster'].append(monster6)
			
				
		wave['boss'] = []
		
		if boss1 != '' and boss1 != '0.0':
			if dropConf.has_key(boss1):
				wave['drop'][boss1] = dropConf[boss1]
			wave['boss'].append(boss1)
		
		if boss2 != '' and boss2 != '0.0':
			if dropConf.has_key(boss2):
				wave['drop'][boss2] = dropConf[boss2]
			wave['boss'].append(boss2)
		
		if boss3 != '' and boss3 != '0.0':
			if dropConf.has_key(boss3):
				wave['drop'][boss3] = dropConf[boss3]
			wave['boss'].append(boss3)
			
		if boss4 != '' and boss4 != '0.0':
			if dropConf.has_key(boss4):
				wave['drop'][boss4] = dropConf[boss4]
			wave['boss'].append(boss4)
			
		if boss5 != '' and boss5 != '0.0':
			if dropConf.has_key(boss5):
				wave['drop'][boss5] = dropConf[boss5]
			wave['boss'].append(boss5)
			
		if boss6 != '' and boss6 != '0.0':
			if dropConf.has_key(boss6):
				wave['drop'][boss6] = dropConf[boss6]
			wave['boss'].append(boss6)
		
		ls = str(row[idx + 12]).split(',')
		wave['count'] =  [ int( eval(x) ) for x in ls if x ]		
		ls = str(row[idx + 13]).split(',')
		wave['count_prob'] = [ int( eval(x) ) for x in ls if x ]		
		wave['more'] = int(row[idx + 14])
		
		return wave
		
	@staticmethod
	def equipment_import(request):
		if request.method == 'POST':
			equipment_file = request.FILES.get('equipment_file')
			if not equipment_file:
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
				position = int(row[4])
				stack = row[5]
				nature = row[7]
				quality = row[9]
				levelreq = int(row[10])
				hp = int(row[11])
				hpgrowth = int(row[12])
				pa = int(row[13])
				pagrowth = int(row[14])
				#ma = int(row[15])
				#magrowth = int(row[16])
				pd = int(row[17])
				pdgrowth = int(row[18])
				md = int(row[19])
				mdgrowth = int(row[20])
				pt = int(row[21])
				ptgrowth = int(row[22])
				#mt = int(row[23])
				#mtgrowth = int(row[24])
				chip = int(row[25])
				price = int(row[28])
				desc = row[29]				
				
				equipmentConf = {}
				equipmentConf['eqid'] = eqid
				equipmentConf['name'] = name
				equipmentConf['icon'] = icon
				equipmentConf['type'] = type
				equipmentConf['position'] = position
				equipmentConf['stack'] = stack
				equipmentConf['nature'] = nature
				equipmentConf['quality'] = quality
				equipmentConf['levelreq'] = levelreq
				equipmentConf['hp'] = hp
				equipmentConf['hpgrowth'] = hpgrowth
				equipmentConf['pa'] = pa
				equipmentConf['pagrowth'] = pagrowth
				#equipmentConf['ma'] = ma
				#equipmentConf['magrowth'] = magrowth
				equipmentConf['pd'] = pd
				equipmentConf['pdgrowth'] = pdgrowth
				equipmentConf['md'] = md
				equipmentConf['mdgrowth'] = mdgrowth
				equipmentConf['pt'] = pt
				equipmentConf['ptgrowth'] = ptgrowth
				#equipmentConf['mt'] = mt
				#equipmentConf['mtgrowth'] = mtgrowth
				equipmentConf['chip'] = chip
				equipmentConf['price'] = price
				equipmentConf['desc'] = desc			
				
				conf[eqid] = equipmentConf
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('equipment_import')		
		
	@staticmethod
	def strength_price_import(request):
		if request.method == 'POST':
			strength_price_file = request.FILES.get('strength_price_file')
			if not strength_price_file:
				return HttpResponse('强化价格xlsx文件未上传')			
		
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, strength_price_file.read())
			sheet = wb.sheet_by_index(1)
		
			conf = {}
			for rownum in range(4,sheet.nrows):
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
				priceConf[level - 1] = price
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('strength_price_import')
		
	@staticmethod
	def luckycat_bless_import(request):
		if request.method == 'POST':
			luckycat_bless_file = request.FILES.get('luckycat_bless_file')
			if not luckycat_bless_file:
				return HttpResponse('招财猫祝福xlsx文件未上传')			
		
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, luckycat_bless_file.read())
			sheet = wb.sheet_by_index(1)
		
			conf = {}
			for rownum in range(3,sheet.nrows):
				row = sheet.row_values(rownum)
				
				blessid = row[0]				
				icon = row[1]
				desc = row[2]
				probability = row[3]
				triggerProbability = row[4]
				blessTypeStr = row[5]
				value = row[6]				
				blessConf = {}
				blessConf['blessid'] = blessid				
				blessConf['icon'] = icon
				blessConf['desc'] = desc
				blessConf['probability'] = probability
				blessConf['triggerProbability'] = triggerProbability
				blessConf['blessTypeStr'] = blessTypeStr
				blessConf['value'] = value
				conf[blessid] = blessConf
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('luckycat_bless_import')
		
	@staticmethod
	def luckycat_profit_import(request):
		if request.method == 'POST':
			luckycat_profit_file = request.FILES.get('luckycat_profit_file')
			if not luckycat_profit_file:
				return HttpResponse('招财猫日常收益xlsx未上传')
			
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, luckycat_profit_file.read())
			sheet = wb.sheet_by_index(2)
			
			conf = []
			
			for rownum in range(3, sheet.nrows):
				row = sheet.row_values(rownum)
				
				level = int(row[0])
				beckonProfit = int(row[1])
				blessProfit = int(row[2])
				agreeProfit = int(row[3])
				
				while len(conf) < level:
					conf.append({})
					
				conf[level - 1]['beckonProfit']= beckonProfit
				conf[level - 1]['blessProfit'] = blessProfit
				conf[level - 1]['agreeProfit'] = agreeProfit
			
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('luckycat_profit')
					
		
	@staticmethod
	def luck_import(request):
		if request.method == 'POST':
			luck_file = request.FILES.get('luck_file')
			if not luck_file:
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
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('luck_import')
		
	@staticmethod
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
							
				strid = unicode(int(row[0]))
				chinese = row[2]
				lanConf = {}
				#lanConf['strid'] = strid
				lanConf[strid] = chinese
				conf[strid] = chinese
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('language_import')
	
	@staticmethod
	def stone_import(request):
		if request.method == 'POST':
			stone_file = request.FILES.get('stone_file')
			if not stone_file:
				return HttpResponse('宝石xlsx文件未上传')
			
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, stone_file.read())
			sheet = wb.sheet_by_index(1)
					
			conf = {}
			for rownum in range(4,sheet.nrows):
				row = sheet.row_values(rownum)
				stoneid = row[0]
				quality = int(row[3])
				name = row[4]
				icon = row[5]			
				typestr = row[6]
				type = int(row[7])
				value = int(row[8])
				gravel = int(row[9])
				level = int(row[10])
				exp = int(row[11])
				
				stoneConf = {}
				stoneConf['stoneid'] = stoneid
				stoneConf['quality'] = quality
				stoneConf['name'] = name
				stoneConf['icon'] = icon
				stoneConf['typestr'] = typestr
				stoneConf['type'] = type
				stoneConf['val'] = value
				stoneConf['gravel'] = gravel
				stoneConf['level'] = level
				stoneConf['exp'] = exp
				
				if not conf.has_key(stoneid):
					conf[stoneid] = []
					
				while len(conf[stoneid]) < level:
					conf[stoneid].append({})
				
				conf[stoneid][level - 1] = stoneConf		
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('stone_import')
		
	@staticmethod
	def stone_probability_import(request):
		if request.method == 'POST':
			stone_probability_file = request.FILES.get('stone_probability_file')
			if not stone_probability_file:
				return HttpResponse('宝石概率xlsx文件未上传')
			
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, stone_probability_file.read())
			sheet = wb.sheet_by_index(0)
					
			conf = {}
			
			visitProbRow = sheet.row_values(2)
			
			visit1Prob = int(visitProbRow[1])
			visit2Prob = int(visitProbRow[2])
			visit3Prob = int(visitProbRow[3])
			visit4Prob = int(visitProbRow[4])
			visit5Prob = int(visitProbRow[5])
			
			conf['visitProb'] = [visit1Prob, visit2Prob, visit3Prob, visit4Prob, visit5Prob]
			
			visitGoldRow = sheet.row_values(3)
			visit1Gold = int(visitGoldRow[1])
			visit2Gold = int(visitGoldRow[2])
			visit3Gold = int(visitGoldRow[3])
			visit4Gold = int(visitGoldRow[4])
			visit5Gold = int(visitGoldRow[5])
			
			conf['visitGold'] = [visit1Gold, visit2Gold, visit3Gold, visit4Gold, visit5Gold]
			
			visitGemRow = sheet.row_values(4)
			visit1Gem = int(visitGemRow[1])
			visit2Gem = int(visitGemRow[2])
			visit3Gem = int(visitGemRow[3])
			visit4Gem = int(visitGemRow[4])
			visit5Gem = int(visitGemRow[5])
			
			conf['visitGem'] = [visit1Gem, visit2Gem, visit3Gem, visit4Gem, visit5Gem]
			
	
			stoneCol = sheet.col_values(0)
			level1Col = sheet.col_values(1)
			level2Col = sheet.col_values(2)
			level3Col = sheet.col_values(3)
			level4Col = sheet.col_values(4)
			level5Col = sheet.col_values(5)
			
			conf['visit'] = []
			
			excel_import.read_stone_level(stoneCol, level1Col, conf, 1)
			excel_import.read_stone_level(stoneCol, level2Col, conf, 2)
			excel_import.read_stone_level(stoneCol, level3Col, conf, 3)
			excel_import.read_stone_level(stoneCol, level4Col, conf, 4)
			excel_import.read_stone_level(stoneCol, level5Col, conf, 5)
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('stone_probability_import')

	@staticmethod
	def trp_price_import(request):
		if request.method == 'POST':
			trp_price_file = request.FILES.get('trp_price_file')
			if not trp_price_file:
				return HttpResponse('培养价格xlsx文件未上传')			
			
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
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('trp_price_import')
		
	@staticmethod	
	def trp_import(request):
		if request.method == 'POST':
			trp_file = request.FILES.get('trp_file')
			if not trp_file:
				return HttpResponse('培养点xlsx文件未上传')			
			
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
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('trp_import')
		
	@staticmethod
	def trp_probability_import(request):
		if request.method == 'POST':
			trp_probability_file = request.FILES.get('trp_probability_file')
			if not trp_probability_file:
				return HttpResponse('培养概率xlsx文件未上传')
			
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, trp_probability_file.read())
			sheet = wb.sheet_by_index(0)
					
			conf = {'point':[], 'training3':[], 'training2':[], 'training1':[], 'training':[] }
			
			for rownum in range(1,sheet.nrows):
				row = sheet.row_values(rownum)
				conf['point'].append(row[0])
				conf['training3'].append(row[1])
				conf['training2'].append(row[2])
				conf['training1'].append(row[3])
				conf['training'].append(row[4])
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('trp_probability_import')
				
		
	
	@staticmethod
	def educate_import(request):
		if request.method == 'POST':
			educate_file = request.FILES.get('educate_file')
			if not educate_file:
				return HttpResponse('训练xlsx文件未上传')			
			
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, educate_file.read())
			sheet = wb.sheet_by_index(0)
					
			conf = []
			
			for rownum in range(4,sheet.nrows):
				row = sheet.row_values(rownum)
				
				level = int(row[0])
				gold = int(row[1])
				expptm = int(row[2])
				
				while len(conf) < level:
					conf.append({})
				
				educateConf = {}
				educateConf['gold'] = gold
				educateConf['expptm'] = expptm
					
				conf[level - 1] = educateConf
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('educate_import')
		
	@staticmethod
	def educate_grade_import(request):
		if request.method == 'POST':
			educate_grade_file = request.FILES.get('educate_grade_file')
			if not educate_grade_file:
				return HttpResponse('训练档次xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, educate_grade_file.read())
			sheet = wb.sheet_by_index(1)
					
			conf = []
			
			for rownum in range(2,sheet.nrows):
				row = sheet.row_values(rownum)				
				trainer = row[0]
				grade = int(row[1])
				goldPrice = 0
				gemPrice = int(row[2])
				probability = int(row[3])
				rate = float(row[4])
				vip = int(row[5])
				
				gradeConf = {}
				gradeConf['trainer'] = trainer
				gradeConf['price'] = {}
				gradeConf['price']['gem'] = gemPrice
				gradeConf['price']['gold'] = goldPrice
				gradeConf['probability'] = probability
				gradeConf['rate'] = rate
				gradeConf['vip'] = vip
				
				while len(conf) < grade:
					conf.append({})			
				
				conf[grade - 1] = gradeConf
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('educate_grade_import')
		
	@staticmethod
	def almanac_combination_import(request):
		if request.method == 'POST':
			almanac_combination_file = request.FILES.get('almanac_combination_file')
			if not almanac_combination_file:
				return HttpResponse('图鉴组合xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, almanac_combination_file.read())
			sheet = wb.sheet_by_index(0)
					
			conf = {}
			
			for rownum in range(3,sheet.nrows):
				row = sheet.row_values(rownum)
				almanacCombinationid = row[0]
				if row[1] == '':
					combinCardid = []
				else:
					combinCardid = row[1].split(',')
				if row[2] == '':
					combinSkillid = []
				else:
					combinSkillid = row[2].split(',')
				if row[3]	== '':
					combinEquipmentid = []
				else:
					combinEquipmentid = row[3].split(',')		
				
				dropid = row[4]
				typestr = row[25]
				type = int(row[26])
				value = row[27]				
				
				almanacConf = {}
				almanacConf['combin_cardid'] = combinCardid
				almanacConf['combin_skillid'] = combinSkillid
				almanacConf['combin_equipmentid'] = combinEquipmentid
				almanacConf['dropid'] = dropid
				almanacConf['typestr'] = typestr
				almanacConf['type'] = type
				almanacConf['val'] = value
				
				conf[almanacCombinationid] = almanacConf
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('almanac_import')
				
				
	@staticmethod
	def reborn_import(request):
		if request.method == 'POST':
			reborn_file = request.FILES.get('reborn_file')
			if not reborn_file:
				return HttpResponse('转生xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, reborn_file.read())
			sheet = wb.sheet_by_index(0)					
			conf = []
			
			for rownum in range(1,sheet.nrows):
				row = sheet.row_values(rownum)
				level = int(row[0])
				star_max = int(row[1])				
				star = []
				star.append({'star':row[2], 'probability': row[3]})
				star.append({'star':row[4], 'probability': row[5]})
				star.append({'star':row[6], 'probability': row[7]})
				star.append({'star':row[8], 'probability': row[9]})
				star.append({'star':row[10], 'probability': row[11]})
				
				rebornConf = {}
				rebornConf['level'] = level
				rebornConf['star_max'] = star_max				
				rebornConf['star'] = star
				conf.append(rebornConf)
				sorted(conf, key = lambda s:s['level'])			
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('reborn_import')
	
	@staticmethod
	def ladder_score_import(request):
		if request.method == 'POST':
			reborn_file = request.FILES.get('ladder_score_file')
			if not reborn_file:
				return HttpResponse('天梯分数xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, reborn_file.read())
			sheet = wb.sheet_by_index(0)					
			conf = []
			
			for rownum in range(1,sheet.nrows):
				row = sheet.row_values(rownum)
				no = int(row[0])
				score = int(row[1])				
				while len(conf) < no:
					conf.append(0)					
				conf[no - 1] = score
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('ladder_score_import')			
	
	@staticmethod
	def name_import(request):
		if request.method == 'POST':
			name_file = request.FILES.get('name_file')
			if not name_file:
				return HttpResponse('姓名xlsx文件未上传')
					
			conf = {}
			conf['surname'] = []
			conf['male_name'] = []
			conf['female_name'] = []
									
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, name_file.read())
			sheet = wb.sheet_by_index(0)
			
			for rownum in range(3,sheet.nrows):
				row = sheet.row_values(rownum)
				conf['surname'].append(row[0])
			
			sheet = wb.sheet_by_index(1)		
			for rownum in range(3,sheet.nrows):
				row = sheet.row_values(rownum)
				conf['male_name'].append(row[0])
			
			sheet = wb.sheet_by_index(2)		
			for rownum in range(3,sheet.nrows):
				row = sheet.row_values(rownum)
				conf['female_name'].append(row[0])	
				
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('name_import')
		
	@staticmethod
	def arena_loot_import(request):
		if request.method == 'POST':
			arena_loot_file = request.FILES.get('arena_loot_file')
			if not arena_loot_file:
				return HttpResponse('竞技场战利品xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, arena_loot_file.read())
			sheet = wb.sheet_by_index(0)
					
			conf = []			
			for rownum in range(1,sheet.nrows):
				row = sheet.row_values(rownum)
				
				level = int(row[0])
				gold = int(row[1])
				exp = int(row[2])
				drop = row[3]
				skillid = row[7]		
				
				while len(conf) < level:
					conf.append({})
					
				arenaLootConf = {}
				arenaLootConf['gold'] = gold
				arenaLootConf['exp'] = exp				
				arenaLootConf['drop'] = drop				
				conf[level - 1] = arenaLootConf
				
			return HttpResponse(json.dumps(conf, sort_keys=True))			
		return HttpResponse('arena_loot_import')
								
	@staticmethod
	def drop_import(request):
		if request.method == 'POST':
			drop_file = request.FILES.get('drop_file')
			if not drop_file:
				return HttpResponse('掉落xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, drop_file.read())
			sheet = wb.sheet_by_index(0)
			conf = {}
			for rownum in range(3, sheet.nrows):
				row = sheet.row_values(rownum)
				dropid = row[0]
				dropstr = row[1]
				isClient = int(row[2])
				
				conf[dropid] = {'drop':excel_import.make_drop_dic(dropstr), 'isClient':isClient}
			
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('drop_import')
				
	@staticmethod
	def make_drop_dic(s):
		dic = []
		item = s.split(',')
		for i in item:
			f = i.split(':')
			if f[0] == 'card':
				dic.append(excel_import.drop_card(f))
			elif f[0] == 'sk':
				dic.append(excel_import.drop_skill(f))
			elif f[0] == 'eq':
				dic.append(excel_import.drop_equipment(f))
			elif f[0] == 'item':
				dic.append(excel_import.drop_item(f))
			elif f[0] == 'stone':
				dic.append(excel_import.drop_stone(f))
			elif f[0] == 'gem':
				dic.append(excel_import.drop_gem(f))
			elif f[0] == 'st':
				dic.append(excel_import.drop_stamina(f))
			elif f[0] == 'sp':
				dic.append(excel_import.drop_sp(f))
			elif f[0] == 'exp':
				dic.append(excel_import.drop_exp(f))
			elif f[0] == 'gold':
				dic.append(excel_import.drop_gold(f))
			elif f[0] == 'skchip':
				dic.append(excel_import.drop_skill_chip(f))
			elif f[0] == 'eqchip':
				dic.append(excel_import.drop_equipment_chip(f))
			elif f[0] == 'cardchip':
				dic.append(excel_import.drop_card_chip(f))
			else:
				dic.append({'unknow':i})			
			
		return dic
		
	@staticmethod
	def drop_card(arr):
		return {'type':'card', 'id':arr[1], 'probability':int(arr[2]),'count':int(arr[3]), 'level':arr[4]}
	
	@staticmethod		
	def drop_skill(arr):	
		return {'type':'sk', 'id':arr[1], 'probability':int(arr[2]),'count':int(arr[3]), 'level':arr[4]}
	
	@staticmethod
	def drop_equipment(arr):
		return {'type':'eq', 'id':arr[1], 'probability':int(arr[2]),'count':int(arr[3]), 'level':arr[4]}
	
	@staticmethod
	def drop_item(arr):
		return {'type':'item', 'id':arr[1], 'probability':int(arr[2]),'count':int(arr[3]), 'level':arr[4]}
	
	@staticmethod
	def drop_stone(arr):
		return {'type':'stone', 'id':arr[1], 'probability':int(arr[2]),'count':int(arr[3]), 'level':arr[4]}
	
	@staticmethod
	def drop_gem(arr):
		return {'type':'gem','probability':int(arr[2]),'count':int(arr[3])}
	
	@staticmethod
	def drop_stamina(arr):
		return {'type':'st','probability':int(arr[2]),'count':int(arr[3])}
	
	@staticmethod		
	def drop_sp(arr):
		return {'type':'sp','probability':int(arr[2]),'count':int(arr[3])}
	
	@staticmethod		
	def drop_gold(arr):
		return {'type':'gold','probability':int(arr[2]),'count':int(arr[3])}
	
	@staticmethod		
	def drop_exp(arr):
		return {'type':'exp','probability':int(arr[2]),'count':int(arr[3])}
	
	@staticmethod
	def drop_skill_chip(arr):
		return {'type':'skchip', 'id':arr[1], 'probability':int(arr[2]),'count':int(arr[3])}
			
	@staticmethod
	def drop_equipment_chip(arr):
		return {'type':'eqchip', 'id':arr[1], 'probability':int(arr[2]),'count':int(arr[3])}
			
	@staticmethod
	def drop_card_chip(arr):
		return {'type':'cardchip', 'id':arr[1], 'probability':int(arr[2]),'count':int(arr[3])}
	
	@staticmethod
	def dialog_import(request):
		if request.method == 'POST':
			dialog_file = request.FILES.get('dialog_file')
			if not dialog_file:
				return HttpResponse('对话xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, dialog_file.read())
			sheet = wb.sheet_by_index(2)
					
			conf = {}
			for rownum in range(3,sheet.nrows):
				row = sheet.row_values(rownum)
				dialogid = row[0]
				npcid = row[1]
				text = row[2]
				
				dialog = {}
				dialog['npcid'] = npcid
				dialog['info'] = text
				
				if not conf.has_key(dialogid):
					conf[dialogid] = []
				conf[dialogid].append(dialog)
					
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('dialog_import')
					
	@staticmethod
	def drama_import(request):	
		if request.method == 'POST':
			drama_file = request.FILES.get('drama_file')
			if not drama_file:
				return HttpResponse('剧情xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, drama_file.read())
			sheet = wb.sheet_by_index(1)
					
			conf = {}
			for rownum in range(3,sheet.nrows):
				row = sheet.row_values(rownum)
				
				type = int(row[0])
				dramaid = row[1]
				repeat = row[2]
				dialogid = row[3]
				drama = {}
				drama['repeat'] = repeat
				drama['talkId'] = dialogid
				
				if not conf.has_key(type):
					conf[type] = {}
				conf[type][dramaid] = drama
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('drama_import')
	
	@staticmethod
	def quest_import(request):
		if request.method == 'POST':
			quest_file = request.FILES.get('quest_file')
			if not quest_file:
				return HttpResponse('任务xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, quest_file.read())
			sheet = wb.sheet_by_index(0)
					
			conf = {}
			for rownum in range(4,sheet.nrows):
				row = sheet.row_values(rownum)
				questid = row[0]
				name = row[1]
				mainType = row[2]
				type = row[3]
				level = int(row[4])
				isFirst = int(row[5])
				nextId = row[6]
				image = row[7]
				repeatCount = int(row[8])
				talkId = row[9]
				finishType = int(row[10])
				finishValue = row[11]
				trigerIcon = row[20]
				dropid = row[21]
				desc = row[30]
				isOpen = row[31]
				beginTime = row[32]
				endTime = row[33]
								
				questConf = {}
				questConf['name'] = name
				questConf['mainType'] = mainType
				questConf['type'] = type
				questConf['level'] = level
				questConf['isFirst'] = isFirst
				questConf['nextId'] = nextId
				questConf['repeatCount'] = repeatCount
				questConf['talkId'] = talkId
				questConf['finishType'] = excel_import.quest_get_cond_str(finishType)
				questConf['finishValue'] = excel_import.quest_get_conf_value(questConf['finishType'], finishValue)
				questConf['trigerIcon'] = trigerIcon
				questConf['dropid'] = dropid
				questConf['desc'] = desc
				questConf['isOpen'] = isOpen
				questConf['beginTime'] = 0
				if beginTime:
					questConf['beginTime'] = str_to_time(beginTime)
				questConf['endTime'] = 0
				if endTime:
					questConf['endTime'] = str_to_time(endTime)
				conf[questid] = questConf
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('quest_import')
		
	@staticmethod
	def quest_get_cond_str(v):
		if v == 1:
			return 'dungeon_id'
		if v == 2:
			return 'talk_npc_id'
		if v == 3:
			return 'charge_cumulate'
		if v == 4:
			return 'yell_count'
		if v == 5:
			return 'friend_count'
		if v == 6:
			return 'vip_item_buy_count'
		if v == 7:
			return 'arena_win_count'
		if v == 8:
			return 'dungeon_win_count'
		return ''
	
	@staticmethod
	def quest_get_conf_value(v, value):
		if v == 'dungeon_id':
			return value.split(',')[0:2]
		if v == 'talk_npc_id':
			return value
		if v == 'charge_cumulate':
			return int(value)
		if v == 'yell_count':
			return int(value)
		if v == 'friend_count':
			return int(value)
		if v == 'vip_item_buy_count':
			s = v.split(',')
			return [s[0], int(s[1])]
		if v == 'arena_win_count':
			return int(value)
		if v == 'dungeon_win_count':
			return int(value)		
	
	@staticmethod
	def item_import(request):
		if request.method == 'POST':
			item_file = request.FILES.get('item_file')
			if not item_file:
				return HttpResponse('道具xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, item_file.read())
			sheet = wb.sheet_by_index(0)
					
			conf = {}
			for rownum in range(2,sheet.nrows):
				row = sheet.row_values(rownum)
				itemid = row[0]
				name = row[1]
				level_required_min = int(row[2])
				level_required_max = int(row[3])
				icon = row[4]
				model = row[5]
				fun_str = row[6]
				desc = row[7]
				stack = int(row[8])
				
				itemConf = {}
				itemConf['name'] = name				
				itemConf['level_required_min'] = level_required_min
				itemConf['level_required_max'] = level_required_max
				itemConf['icon'] = icon
				itemConf['model'] = model
				itemConf['fun'] = excel_import.make_fun_dic(fun_str)
				itemConf['desc'] = desc
				itemConf['stack'] = stack
				conf[itemid] = itemConf			
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('item_import')
				
	@staticmethod
	def make_fun_dic(s):
		dic = {}
		item = s.split(',')
		for i in item:
			c = i.split(':')
			dic[c[0]] = c[1:]
		return dic	
	
	@staticmethod
	def tower_monster_import(request):		
		if request.method == 'POST':
			tower_monster_file = request.FILES.get('tower_monster_file')
			if not tower_monster_file:
				return HttpResponse('神武塔Npcxlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, tower_monster_file.read())
			sheet = wb.sheet_by_index(0)
					
			conf = []
			for rownum in range(2,sheet.nrows):
				row = sheet.row_values(rownum)
				
				floor = int(row[0])
				
				ezPlayerCount = [int(i) for i in row[1].split(',')]
				ezSpeed = int(row[2])
				ezMonster = []
				if row[3]:
					ezMonster.append(row[3])
				if row[4]:
					ezMonster.append(row[4])
				if row[5]:
					ezMonster.append(row[5])
				if row[6]:				
					ezMonster.append(row[6])
				if row[7]:
					ezMonster.append(row[7])
				
				mdPlayerCount = [int(i) for i in  row[8].split(',')]
				mdSpeed = int(row[9])
				mdMonster = []
				if row[10]:
					mdMonster.append(row[10])
				if row[11]:
					mdMonster.append(row[11])
				if row[12]:
					mdMonster.append(row[12])
				if row[13]:
					mdMonster.append(row[13])
				if row[14]:
					mdMonster.append(row[14])	
				
				hdPlayerCount = [int(i) for i in row[15].split(',')]
				hdSpeed = int(row[16])
				hdMonster = []
				if row[17]:
					hdMonster.append(row[17])		
				if row[18]:
					hdMonster.append(row[18])
				if row[19]:
					hdMonster.append(row[19])
				if row[20]:
					hdMonster.append(row[20])
				if row[21]:
					hdMonster.append(row[21])
				
				dropid = row[22]
				
				ezMonsterCount = [int(i) for i in row[23].split(',')]
				mdMonsterCount = [int(i) for i in row[24].split(',')]
				hdMonsterCount = [int(i) for i in row[25].split(',')]
				
				towerMonsterConf = {}
				towerMonsterConf['easyPlayerCount'] = ezPlayerCount
				towerMonsterConf['easySpeed'] = ezSpeed
				towerMonsterConf['easyMonster'] = ezMonster
				towerMonsterConf['middlePlayerCount'] = mdPlayerCount
				towerMonsterConf['middleSpeed'] = mdSpeed
				towerMonsterConf['middleMonster'] = mdMonster
				towerMonsterConf['hardPlayerCount'] = hdPlayerCount
				towerMonsterConf['hardSpeed'] = hdSpeed
				towerMonsterConf['hardMonster'] = hdMonster
				towerMonsterConf['dropid'] = dropid
				towerMonsterConf['easyMonsterCount'] = ezMonsterCount
				towerMonsterConf['middleMonsterCount']= mdMonsterCount
				towerMonsterConf['hardMonsterCount'] = hdMonsterCount
				
				while len(conf) < floor:
					conf.append({})
				conf[floor - 1] = towerMonsterConf
				
			return HttpResponse(json.dumps(conf))
		return HttpResponse('tower_monster_import')
		
	@staticmethod
	def tower_markup_import(request):
		if request.method == 'POST':
			tower_markup_file = request.FILES.get('tower_markup_file')
			if not tower_markup_file:
				return HttpResponse('神武塔开局属性xlsx文件未上传')
						
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, tower_markup_file.read())
			sheet = wb.sheet_by_index(1)
					
			conf = []
			for rownum in range(2,sheet.nrows):
				row = sheet.row_values(rownum)
				floor = int(row[0])
				markup = int(row[1])
				
				while len(conf) < floor:
					conf.append(0)
				conf[floor - 1] = markup				
			return HttpResponse(json.dumps(conf))			
		return HttpResponse('tower_markup_import')
		
	@staticmethod
	def tower_award_import(request):
		if request.method == 'POST':
			tower_award_file = request.FILES.get('tower_award_file')
			if not tower_award_file:
				return HttpResponse('神武塔奖励xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, tower_award_file.read())
			sheet = wb.sheet_by_index(3)
					
			conf = {}
			for rownum in range(2,sheet.nrows):
				row = sheet.row_values(rownum)
				floor = str(int(row[0]))
				award = []
				if row[1]:
					award.append(row[1])
				if row[2]:
					award.append(row[2])
				if row[3]:
					award.append(row[3])
					
				conf[floor] = award
			return HttpResponse(json.dumps(conf))
		return HttpResponse('tower_award_import')
		
	@staticmethod
	def medal_import(request):
		if request.method == 'POST':
			medal_file = request.FILES.get('medal_file')
			if not medal_file:
				return HttpResponse('勋章设定xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, medal_file.read())
			sheet = wb.sheet_by_index(3)
			
			conf = {}
			for rownum in range(4,sheet.nrows):
				row = sheet.row_values(rownum)
				modelid = row[0]
				quality = int(row[1])
				name = row[2]
				icon = row[3]				
				gravel = int(row[4])
				chip = int(row[5])
				desc = row[6]
				chipicon = []
				if row[7]:
					chipicon.append(row[7])
				if row[8]:
					chipicon.append(row[8])
				if row[9]:
					chipicon.append(row[9])
				if row[10]:
					chipicon.append(row[10])
				if row[11]:
					chipicon.append(row[11])
				if row[12]:
					chipicon.append(row[12])
				
				medalConf = {}
				medalConf['modelid'] = modelid
				medalConf['quality'] = quality
				medalConf['name'] = name
				medalConf['icon'] = icon
				medalConf['gravel'] = gravel
				medalConf['chip'] = chip
				medalConf['desc'] = desc
				medalConf['chipicon'] = chipicon
				
				conf[modelid] = medalConf
				
			return HttpResponse(json.dumps(conf))
		return HttpResponse('medal_import')
				
			
	@staticmethod
	def medal_loot_import(request):
		if request.method == 'POST':
			medal_loot_file = request.FILES.get('medal_loot_file')
			if not medal_loot_file:
				return HttpResponse('勋章战利品设定xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, medal_loot_file.read())
			sheet = wb.sheet_by_index(1)
			
			conf = []
			for rownum in range(1,sheet.nrows):
				row = sheet.row_values(rownum)					
				
				level = int(row[0])
				gold = int(row[1])
				exp = int(row[2])
				skillid = row[3]
				skilllevel = int(row[4])
				cardid = row[5]
				cardlevel = int(row[6])				
				
				while len(conf) < level:
					conf.append({})
					
				medalLootConf = {}
				medalLootConf['gold'] = gold
				medalLootConf['exp'] = exp
				medalLootConf['skillid'] = skillid
				medalLootConf['skilllevel'] = skilllevel
				medalLootConf['cardid'] = cardid
				medalLootConf['cardlevel'] = cardlevel				
				conf[level - 1] = medalLootConf
				
			return HttpResponse(json.dumps(conf, sort_keys=True))			
		return HttpResponse('arena_loot_import')
		
	@staticmethod
	def medal_level_import(request):
		if request.method == 'POST':
			medal_level_file = request.FILES.get('medal_level_file')
			if not medal_level_file:
				return HttpResponse('勋章等级设定xlsx文件未上传')
			
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, medal_level_file.read())
			sheet = wb.sheet_by_index(0)
			
			conf = {}			
			
			for rownum in range(4,sheet.nrows):
				row = sheet.row_values(rownum)					
			
				medalid = row[0]
				typestr = row[3]
				type = int(row[4])
				value = int(row[5])
				level = int(row[6])
				exp = int(row[7])
				
				if not conf.has_key(medalid):
					conf[medalid] = []
				
				while len(conf[medalid]) < level:
					conf[medalid].append({})
				
				conf[medalid][level - 1]['typestr'] = typestr
				conf[medalid][level - 1]['type'] = type
				conf[medalid][level - 1]['val'] = value
				conf[medalid][level - 1]['exp'] = exp		
			return HttpResponse(json.dumps(conf, sort_keys=True))			
		return HttpResponse('medal_level_import')
		
	@staticmethod
	def mall_price_import(request):
		if request.method == 'POST':
			mall_price_file = request.FILES.get('mall_price_file')
			if not mall_price_file:
				return HttpResponse('商城价格设定xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, mall_price_file.read())
			sheet = wb.sheet_by_index(0)
			
			conf = []
			
			for rownum in range(3, sheet.nrows):
				row = sheet.row_values(rownum)
				
				mallPriceid = row[0]
				itemid = row[1]
				gemPrice = int(row[2])
				gemPromote = int(row[3])
				goldPrice = int(row[4])
				goldPromote = int(row[5])
				type = int(row[6])
				order = int(row[7])
				
				mallPriceConf = {}
				mallPriceConf['mallPriceid'] = mallPriceid
				mallPriceConf['itemid'] = itemid
				mallPriceConf['gemPrice'] = gemPrice
				mallPriceConf['gemPromote'] = gemPromote
				mallPriceConf['goldPrice'] = goldPrice
				mallPriceConf['goldPromote'] = goldPromote
				mallPriceConf['type'] = type
				mallPriceConf['order'] = order
				
				conf.append(mallPriceConf)
			return HttpResponse(json.dumps(conf, sort_keys=True))
		return HttpResponse('mall_price_import')
		
		
	@staticmethod
	def practice_property_import(request):
		if request.method == 'POST':
			practice_property_file = request.FILES.get('practice_property_file')
			if not practice_property_file:
				return HttpResponse('修练属性xlsx文件未上传')
			
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, practice_property_file.read())
			sheet = wb.sheet_by_index(0)
			
			conf = {}
			
			critical_property = []
			tenacity_property = []
			block_property = []
			wreck_property = []
			
			for rownum in range(1, sheet.nrows):
				row = sheet.row_values(rownum)
				level = int(row[0])
				critical = int(row[1])
				tenacity = int(row[2])
				block = int(row[3])
				wreck = int(row[4])
				
				while len(critical_property) < (level + 1):
					critical_property.append(0)
				while len(tenacity_property) < (level + 1):
					tenacity_property.append(0)
				while len(block_property) < (level + 1):
					block_property.append(0)
				while len(wreck_property) < (level + 1):
					wreck_property.append(0)
				
				critical_property[level] = critical
				tenacity_property[level] = tenacity
				block_property[level] = block
				wreck_property[level] = wreck
				
			conf['critical_property'] = critical_property
			conf['tenacity_property'] = tenacity_property
			conf['block_property'] = block_property
			conf['wreck_property'] = wreck_property
			
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('practice_level_import')
		
	@staticmethod
	def practice_level_import(request):
		if request.method == 'POST':
			practice_level_file = request.FILES.get('practice_level_file')
			if not practice_level_file:
				return HttpResponse('修练等级xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, practice_level_file.read())
			sheet = wb.sheet_by_index(1)
			
			conf = {}
			
			critical_level = []
			tenacity_level = []
			block_level = []
			wreck_level = []
			
			for rownum in range(1, sheet.nrows):
				row = sheet.row_values(rownum)
				level = int(row[0])
				critical = int(row[1])
				tenacity = int(row[2])
				block = int(row[3])
				wreck = int(row[4])
				
				while len(critical_level) < (level + 1):
					critical_level.append(0)
				while len(tenacity_level) < (level + 1):
					tenacity_level.append(0)
				while len(block_level) < (level + 1):
					block_level.append(0)
				while len(wreck_level) < (level + 1):
					wreck_level.append(0)
				
				critical_level[level] = critical
				tenacity_level[level] = tenacity
				block_level[level] = block
				wreck_level[level] = wreck
				
			conf['critical_level'] = critical_level
			conf['tenacity_level'] = tenacity_level
			conf['block_level'] = block_level
			conf['wreck_level'] = wreck_level
			
			card_chip_point = []			
			
			sheet = wb.sheet_by_index(2)
			
			for rownum in range(3, sheet.nrows):
				row = sheet.row_values(rownum)
				quality = int(row[0])
				chip_point = int(row[1])
				
				while len(card_chip_point) < quality:
					card_chip_point.append(0)
				
				card_chip_point[quality - 1] = chip_point
				
			conf['card_point'] = card_chip_point
			
			skill_chip_point = []
			
			sheet = wb.sheet_by_index(3)
			
			for rownum in range(3, sheet.nrows):
				row = sheet.row_values(rownum)
				quality = int(row[0])
				chip_point = int(row[1])
				
				while len(skill_chip_point) < quality:
					skill_chip_point.append(0)
				
				skill_chip_point[quality - 1] = chip_point
				
			conf['skill_point'] = skill_chip_point
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('practice_level_file')
			
			
	@staticmethod
	def slotmachine_import(request):
		if request.method == 'POST':
			slotmachine_file = request.FILES.get('slotmachine_file')
			if not slotmachine_file:
				return HttpResponse('老虎机xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, slotmachine_file.read())
			sheet = wb.sheet_by_index(0)
			
			conf = {'rate':[], 'price':[]}
			
			for rownum in range(2, sheet.nrows):
				row = sheet.row_values(rownum)
				
				benefit = float(row[0])
				probability = int(row[1])
				conf['rate'].append({'benefit': benefit, 'probability': probability})
					
			sheet = wb.sheet_by_index(1)
			
			for rownum in range(1, sheet.nrows):
				row = sheet.row_values(rownum)
				
				num = int(row[0])
				price = int(row[1])
				
				while len(conf['price']) < num:
					conf['price'].append(0)
					
				conf['price'][num - 1] = price
			
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('slotmachine_import')
		
	@staticmethod
	def vip_import(request):		
		if request.method == 'POST':
			vip_file = request.FILES.get('vip_file')
			if not vip_file:
				return HttpResponse('老虎机xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, vip_file.read())
			sheet = wb.sheet_by_index(0)
			
			conf = {}
			
			for rownum in range(2, sheet.nrows):
				row = sheet.row_values(rownum)
				
				name = row[1]
				
				vip1 = row[2]
				vip2 = row[3]
				vip3 = row[4]
				vip4 = row[5]
				vip5 = row[6]
				vip6 = row[7]
				vip7 = row[8]
				vip8 = row[9]
				vip9 = row[10]
				vip10 = row[11]
				
				if name == 'gift':
					conf[name] = [vip1, vip2, vip3, vip4, vip5, vip6, vip7, vip8, vip9, vip10]
				elif name:
					conf[name] = [int(vip1), int(vip2), int(vip3), int(vip4), int(vip5), int(vip6), int(vip7), int(vip8), int(vip9), int(vip10)]
				
			
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('vip_import')
		
	@staticmethod
	def potential_price_import(request):
		if request.method == 'POST':
			potential_price_file = request.FILES.get('potential_price_file')
			if not potential_price_file:
				return HttpResponse('潜力激发价格xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, potential_price_file.read())
			sheet = wb.sheet_by_index(0)
			
			conf = []
			
			for rownum in range(1, sheet.nrows):
				row = sheet.row_values(rownum)
				
				level = int(row[0])
				price = int(row[1])
				
				while len(conf) < level:
					conf.append(0)
				conf[level - 1] = price
				
			return HttpResponse(json.dumps(conf, sort_keys = True))	
		return HttpResponse('protential_price_import')
		
	@staticmethod
	def email_import(request):
		if request.method == 'POST':
			email_file = request.FILES.get('email_file')
			if not email_file:
				return HttpResponse('邮件xlsx文件未上传')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, email_file.read())
			sheet = wb.sheet_by_index(0)			
			conf = {}			
			for rownum in range(3, sheet.nrows):
				row = sheet.row_values(rownum)
				
				emailid = row[0]
				optype = row[1]
				opvaule = row[2]
				email_title = row[3]
				email_text = row[4]
				dropid = row[5]
				
				emailConf = {}
				emailConf['optype'] = optype
				emailConf['opvaule'] = opvaule
				emailConf['email_title'] = email_title
				emailConf['email_text'] = email_text
				emailConf['dropid'] = dropid
				
				conf[emailid] = emailConf
				
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('email_import')
		
	@staticmethod
	def gift_import(request):
		if request.method == 'POST':
			gift_file = request.FILES.get('gift_file')
			if not gift_file:
				return HttpResponse('礼物')
				
			wb = xlrd.open_workbook(None, sys.stdout, 0, USE_MMAP, gift_file.read())
			sheet = wb.sheet_by_index(1)
			conf = {}
			
			for rownum in range(3, sheet.nrows):
				row = sheet.row_values(rownum)
				
				item = str(int(row[0]))
				ps = row[1]
				memo = row[2]
				broadcast = row[3]
				gold = int(row[4])
				gem = int(row[5])
				exp = int(row[6])
				tuhao = int(row[7])
				charm = int(row[8])
				
				giftConf = {}
				giftConf['ps'] = ps
				giftConf['memo'] = memo
				giftConf['broadcast'] = broadcast
				giftConf['gold'] = gold
				giftConf['gem'] = gem
				giftConf['exp'] = exp
				giftConf['tuhao'] = tuhao
				giftConf['charm'] = charm
				
				conf[item] = giftConf
			return HttpResponse(json.dumps(conf, sort_keys = True))
		return HttpResponse('gift_import')
				