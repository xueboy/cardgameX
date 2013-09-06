#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson


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