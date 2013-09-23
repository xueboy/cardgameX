#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson
from game.routine.pet import pet

def set_team(request):
 	 usr = request.user
 	 inv = usr.getInventory()
 	 cardid1 = request.GET['card_id1']
 	 cardid2 = request.GET['card_id2']
 	 cardid3 = request.GET['card_id3']
 	 cardid4 = request.GET['card_id4']
 	 team = inv.setTeam(cardid1, cardid2, cardid3, cardid4)
 	 inv.save()
 	 return HttpResponse(gcjson.dumps(team))


def set_leader(request):
	usr = request.user
	inv = usr.getInventory()
	cardid = request.GET['card_id']	
	team = inv.setLeader(cardid)
	inv.save()
	return HttpResponse(gcjson.dumps(team))
	
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
	return HttpResponse(gcjson.dumps({'update_card':dest, 'delete_card':source}))
		
def garcha(request):
	usr = request.user
	
	garchaType = request.GET['type']	