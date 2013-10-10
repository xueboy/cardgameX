#coding:utf-8\
#!/usr/bin/env python

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gclib.gcjson import gcjson
from game.utility.config import config as conf
from game.models.account import account
from gclib.utility import HttpResponse500, beginRequest, onUserLogin, currentTime, endRequest
from game.models.user import user
import game.views.dungeon
import game.views.gm
import game.views.card
import game.views.friend
import game.views.profile
import sys
#from PIL import Image
#import StringIO


viewsmap = {
	'dungeon':sys.modules['game.views.dungeon'],
	'gm':sys.modules['game.views.gm'],
	'card':sys.modules['game.views.card'],
	'friend':sys.modules['game.views.friend'],
	'profile': sys.modules['game.views.profile']
}

def index(request):
	username = request.GET['username']
	pwd = request.GET['password']
	acc = account.login(username, pwd)
	if acc != None:
		usr = acc.getUser()
		if usr == None:
			raise Http500("server error")
			return HttpResponse500()
		onUserLogin(request, usr)
		usr.last_login = currentTime()
		
		data = {}
		usr.updateStamina()
		data.update(usr.getClientData())
		dun = usr.getDungeon()
		data['dungeon'] = dun.getClientData()
		inv = usr.getInventory()
		data.update(inv.getClientData())		
		nw = usr.getNetwork()
		data.update(nw.getClientData())		
		usr.save()
		return HttpResponse(gcjson.dumps(data))
	return HttpResponse("Hello, world. You're at the test page index.")


def info(request):
	
	info = {}	
	#info[u'dungeon_config_md5'] =  config.getMd5('dungeon')
	info[u'status'] = u'OK'
	#info['greet'] = u'ÄãºÃ'
	return HttpResponse(gcjson.dumps({'info':info}))
	
def config(request):	
	beginRequest(request,user)
	data = {}	
	dungeon_config_md5 = request.GET['dungeon_config_md5']
	level_config_md5 = request.GET['level_config_md5']
	game_config_md5 = request.GET['game_config_md5']
	pet_config_md5 = request.GET['pet_config_md5']
	monster_config_md5 = request.GET['monster_config_md5']
	skill_config_md5 = request.GET['skill_config_md5']
	pet_level_config_md5 = request.GET['pet_level_config_md5']
	prompt_config_md5 = request.GET['prompt_config_md5']
	
	
	if dungeon_config_md5 != conf.getClientConfigMd5('dungeon'):
		data['dungeon'] = conf.getClientConfig('dungeon')
	if level_config_md5 != conf.getClientConfigMd5('level'):
		data['level'] = conf.getClientConfig('level')
	if game_config_md5 != conf.getClientConfigMd5('game'):
		data['game'] = conf.getClientConfig('game')
	if pet_config_md5 != conf.getClientConfigMd5('pet'):
		data['pet'] = conf.getClientConfig('pet')
	if monster_config_md5 != conf.getClientConfigMd5('monster'):
		data['monster'] = conf.getClientConfig('monster')
	if skill_config_md5 != conf.getClientConfigMd5('skill'):
		data['skill'] = conf.getClientConfig('skill')
	if pet_level_config_md5 != conf.getClientConfigMd5('pet_level'):
		data['pet_level'] = conf.getClientConfig('pet_level')
	if prompt_config_md5 != conf.getClientConfigMd5('prompt'):
		data['prompt'] = conf.getClientConfig('prompt')
	p = gcjson.dumps(data)
	return HttpResponse(p)
	
def api(request, m, f):
	try:
		beginRequest(request,user)
	except KeyError:
		return info(request)
	if viewsmap.has_key(m) :		
		fun = getattr(viewsmap[m], f)		
		ret = fun(request)
		
		notify = endRequest(request)
		ret.update(notify)
		
		return HttpResponse(gcjson.dumps(ret))

	return HttpResponse('api')

@csrf_exempt
def test(request):	
	#print "aaa"
	f = request.body
	#img = Image.new()
	#img.putdata(f)
	#print f
	#img = Image.open(StringIO.StringIO(f))
	#print img
#	img.save(r"d:/img.png", "png")
	return HttpResponse(f, mimetype="image/png")
	
def setAvatar(request):
	f = request.body
	img = Image()
	imp.putdata()
	
	#img.
	
