#coding:utf-8
#!/usr/bin/env python


from game.routine.practice import practice

def card_levelup(request):
	
	cardid = []
	
	cardid.append(request.GET['cardid1'])
	
	for i in range(2, 50):
		keyname = 'cardid' + str(i)
		if request.GET.has_key(keyname):
			cardid.append(request.GET[keyname])
		else:
			break
	tp = request.GET['type']
	usr = request.user
	return practice.card_levelup(usr, tp, cardid)
	
	
def card_chip_levelup(request):
	chipDic = {}
	
	chipDic[request.GET['card_id1']] = int(request.GET['chipnum1'])
	
	for i in range(2, 50):
		chipkeyname = 'card_id' + str(i)
		chipnumkeyname = 'chipnum' + str(i)
		
		if request.GET.has_key(chipkeyname):
			chipDic[chipkeyname] = int(chipnumkeyname)
		else:
			break
	tp = request.GET['type']
	usr = request.user
	return practice.card_chip_levelup(usr, tp, chipDic)
	
def skill_levelup(request):
	skillid = []
	
	skillid.append(request.GET['skillid1'])
	
	for i in range(2, 50):
		keyname = 'skillid' + str(i)
		if request.GET.has_key(keyname):
			skillid.append(request.GET[keyname])
		else:
			break
	tp = request.GET['type']
	usr = request.user
	return practice.skill_levelup(usr, tp, skillid)
	
def skill_chip_levelup(request):
	chipDic = {}	
	chipDic[request.GET['skill_id1']] = int(request.GET['skillnum1'])
	
	for i in range(2, 50):
		chipkeyname = 'skill_id' + str(i)
		chipnumkeyname = 'chipnum' + str(i)
		
		if request.GET.has_key(chipkeyname):
			chipDic[chipkeyname] = int(chipnumkeyname)
		else:
			break
	tp = request.GET['type']
	usr = request.user
	return practice.skill_chip_levelup(usr, tp, chipDic)
