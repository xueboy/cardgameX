#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import randint
from cardgame.settings import ARENE_SERVER
from game.models.user import user
from game.routine.arena import arena
from game.utility.config import config


def show_ladder(request):
	usr = request.user
	return json.loads(curl.url(ARENE_SERVER +  '/arena/show_ladder/', None, {'roleid':str(usr.roleid)}))

def stand_ladder(request):
	usr = request.user
	return arena.stand_ladder(usr)

def show_all(request):
	return arena.show_all()

def challenge(request):
	usr = request.user
	defenceRoleid = request.GET['defence_roleid']
	return arena.challenge(usr, defenceRoleid)

def defeate(request):
	usr = request.user
	return arena.defeate(usr)

def convert(request):
	mediumCount = request.GET['medium_count']
	mediumCount = int(mediumCount)

	usr = request.user
	gameConf = config.getConfig('game')

	pointConsume = mediumCount * gameConf['arena_medium_price']

	res = curl.url(ARENE_SERVER +  '/arena/convert/', None, {'roleid':str(usr.roleid), 'score':pointConsume})
	from django.http import HttpResponse
	res = json.loads(res)

	if res.has_key('msg'):
		return res

	mediumId = gameConf['arena_medium_id']
	inv = usr.getInventory()
	updateIt, newIt = inv.addItemCount(mediumId, mediumCount)
	inv.save()

	data = {}
	if updateIt:
		data['update_item_array'] = updateIt
	if newIt:
		data['add_item_array'] = newIt
	return data

def score(request):
	usr = request.user	
	return arena.score(usr.roleid)
