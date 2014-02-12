#coding:utf-8
#!/usr/bin/env python


from game.routine.practice import practice

def card_levelup(request):
	
	cardid = []
	for i in range(1, 50):
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
	for i in range(1, 50):
		chipkeyname = 'cardid' + str(i)
		chipnumkeyname = 'chipnum' + str(i)
		
		if request.GET.has_key(chipkeyname):
			chipDic[chipkeyname] = chipnumkeyname
		else:
			break
	tp = request.GET['type']
	usr = request.user
	return practice.card_chip_levelup(usr, tp, chipDic)
	
def skill_levelup(request):
	pass
	
def skill_chip_levelup(request):
	pass
