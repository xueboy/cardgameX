#coding:utf-8\
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson
from game.utility.config import config as conf
from game.models.account import account
from gclib.utility import HttpResponse500, amendRequest, onLogin, currentTime
from game.models.user import user
import game.views.dungeon
import game.views.gm
from game.game_def import viewsmap





def index(request):
	username = request.GET['username']
	pwd = request.GET['password']
	acc = account.login(username, pwd)
	if acc != None:
		usr = acc.getUser()
		if usr == None:
			raise Http500("server error")
			return HttpResponse500()
		onLogin(request, usr)
		usr.last_login = currentTime()
		
		data = {}
		usr.updateStamina()
		data['user'] = usr.getClientData()
		dun = usr.getDungeon()
		data['dungeon'] = dun.getClientData()
		inv = usr.getInventory()
		data['inventory'] = inv.getClientData()
		return HttpResponse(gcjson.dumps(data))		
	return HttpResponse("Hello, world. You're at the test page index.")


def info(request):
	
	info = {}
	#info[u'dungeon_config_md5'] =  config.getMd5('dungeon')
	info[u'status'] = u'OK'
	return HttpResponse(gcjson.dumps(info))
	
def config(request):	
	amendRequest(request,user)
	data = {}	
	dungeon_config_md5 = request.GET['dungeon_config_md5']
	level_config_md5 = request.GET['level_config_md5']
	game_config_md5 = request.GET['game_config_md5']
	card_config_md5 = request.GET['card_config_md5']
	
	if dungeon_config_md5 != conf.getClientConfigMd5('dungeon'):
		data['dungeon'] = conf.getClientConfig('dungeon')
#		data['dungeon_md5'] = conf.getClientConfigMd5('dungeon')
	if level_config_md5 != conf.getClientConfigMd5('level'):
		data['level'] = conf.getClientConfig('level')
#		data['level_md5'] = conf.getClientConfigMd5('level')	
	if game_config_md5 != conf.getClientConfigMd5('game'):
		data['game'] = conf.getClientConfig('game')
	if card_config_md5 != conf.getClientConfigMd5('card'):
		data['card'] = conf.getClientConfig('card')
#		data['game_md5'] = conf.getClientConfigMd5('game')		
	return HttpResponse(gcjson.dumps(data))
	
def api(request, m, f):
	amendRequest(request,user)
	if viewsmap.has_key(m) :		
		fun = getattr(viewsmap[m], f)
		return fun(request)	
	return HttpResponse("url error.")
