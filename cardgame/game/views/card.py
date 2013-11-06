#coding:utf-8
#!/usr/bin/env python

from gclib.json import json
from game.routine.pet import pet
from game.routine.garcha import garcha as garchaR
from game.models.inventory import inventory

def set_team(request):
 	 usr = request.user
 	 inv = usr.getInventory()
 	 cardid1 = request.GET['card_id1']
 	 cardid2 = request.GET['card_id2']
 	 cardid3 = request.GET['card_id3']
 	 cardid4 = request.GET['card_id4']
 	 cardid5 = request.GET['card_id5']
 	 cardid6 = request.GET['card_id6']
 	 team = inv.setTeam(cardid1, cardid2, cardid3, cardid4, cardid5, cardid6) 	 
 	 return {'team':team, 'slots': inv.getSlots()}

	
def level_up(request):
	usr = request.user
	
	sourceCard1 = ''
	sourceCard2 = ''
	sourceCard3 = ''
	sourceCard4 = ''
	sourceCard5 = ''
	sourceCard6 = ''	
	
	destCard = request.GET['dest_card']
	sourceCard1 = request.GET['source_card1']
	if request.GET.has_key('source_card2'):
		sourceCard2 = request.GET['source_card2']	
	if request.GET.has_key('source_card3'):
		sourceCard3 = request.GET['source_card3']	
	if request.GET.has_key('source_card4'):
		sourceCard4 = request.GET['source_card4']		
	if request.GET.has_key('source_card5'):
		sourceCard5 = request.GET['source_card5']	
	if request.GET.has_key('source_card6'):
		sourceCard6 = request.GET['source_card6']	
	
	sourceCardId = []
	if sourceCard1 != '':
		sourceCardId.append(sourceCard1)
	if sourceCard2 != '':
		sourceCardId.append(sourceCard2)
	if sourceCard3 != '':
		sourceCardId.append(sourceCard3)
	if sourceCard4 != '':
		sourceCardId.append(sourceCard4)
	if sourceCard5 != '':
		sourceCardId.append(sourceCard5)
	if sourceCard6 != '':
		sourceCardId.append(sourceCard6)		
		
	dest, source = pet.levelup(usr, destCard, sourceCardId)
	return {'update_card':dest, 'delete_card':source}
		
def garcha(request):
	usr = request.user
	
	garchaAmount = request.GET['amount']
	if garchaAmount == '1':
		garchaAmount = 10
	elif garchaAmount == '2':
		garchaAmount = 100
	elif garchaAmount == '3':
		garchaAmount = 10000
	else:
		return {'msg':'parameter_bad'}
	res = garchaR.garcha_once(usr, garchaAmount)	
	return res
	
def training(request):
 	usr = request.user
 	
 	id = request.GET['id']
 	traininglevel = request.GET['training_level']
 	
 	return pet.training(usr, id, traininglevel) 	
 	
def sell(request):
	
	usr = request.user
	id = request.GET['id']
	return pet.sell(usr, id)
	
def training_confirm(request):
	usr = request.user	
	return pet.trainConfirm(usr)

