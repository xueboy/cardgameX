#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson

def add_card(request):
	card_id = request.GET['card_id']	
	usr = request.user
	inv = usr.getInventory()	
	if inv.addCard(card_id) == None:
		return HttpResponse("add card field")	
	inv.save()
	data = {}
	data['card'] = inv.getClientData()	
	return HttpResponse(gcjson.dumps(data))	

def del_card(request):
	idx = int(request.GET['index'])
	usr = request.user
	inv = usr.getInventory()	
	if inv.delCard(idx) == 0:
		return HttpResponse("del card field")	
	inv.save()
	return HttpResponse(gcjson.dumps({}))	
		