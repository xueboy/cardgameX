#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson
from game.utility.config import config as conf
from game.models.account import account
from gclib.utility import HttpResponse500, amendRequest, onLogin
from game.models.user import user



def index(request):
	username = request.GET['username']
	pwd = request.GET['password']
	acc = account.login(username, pwd)
	if acc != None:
		user = acc.getUser()
		if user == None:
			raise Http500("server error")
			return HttpResponse500()
		onLogin(request, user)
		
		data = {}
		data['user'] = user.getClientData()
		dungeon = user.getDungeon()
		data['dungeon'] = dungeon.getClientData()		
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
	if dungeon_config_md5 != conf.getClientConfigMd5('dungeon'):
		data['dungeon'] = conf.getClientConfig('dungeon')
		data['dungeon_md5'] = conf.getClientConfig('dungeon')
	if level_config_md5 != conf.getClientConfig('level'):
		data['level'] = conf.getClientConfig('level')
		data['level_md5'] = conf.getClientConfig('level')	
	return HttpResponse(gcjson.dumps(data))
