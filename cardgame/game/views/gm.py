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
	usr.save()
	inv.save()
	data = {}
	data['card'] = inv.getClientData()	
	return HttpResponse(gcjson.dumps(data))	

def del_card(request):
	name = int(request.GET['name'])
	usr = request.user
	inv = usr.getInventory()	
	if inv.delCard(name) == 0:
		return HttpResponse("del card field")	
	usr.save()	
	inv.save()
	return HttpResponse(gcjson.dumps({}))	
		