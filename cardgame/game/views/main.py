#coding:utf-8\
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.json import *
from gclib.curl import curl
from game.utility.config import config as conf
from game.models.account import account
from gclib.utility import HttpResponse500, beginRequest, onUserLogin, currentTime, endRequest
from game.models.user import user
from game.models.network import network
import game.views.dungeon
import game.views.gm
import game.views.card
import game.views.friend
import game.views.profile
import game.views.equipment
import game.views.luckycat
import game.views.stone
import sys
#from PIL import Image
#import StringIO


viewsmap = {
	'dungeon':sys.modules['game.views.dungeon'],
	'gm':sys.modules['game.views.gm'],
	'card':sys.modules['game.views.card'],
	'friend':sys.modules['game.views.friend'],
	'profile': sys.modules['game.views.profile'],
	'equipment': sys.modules['game.views.equipment'],
	'luckycat': sys.modules['game.views.luckycat'],
	'stone': sys.modules['game.views.stone'],
}

def index(request):
	username = request.GET['username']
	pwd = request.GET['password']
	acc = account.login(username, pwd)
	if acc != None:
		if not acc.nickname:
			return HttpResponse(json.dumps({'msg':'nickname_should_set_before'}))
			return http
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
		usr.notify = {}
		usr.save()
		return HttpResponse(json.dumps(data))
	return HttpResponse(json.dumps({'msg':'account_name_not_exist'}))


def info(request):
	
	info = {}	
	info[u'status'] = u'OK'
	#info['greet'] = u'ÄãºÃ'
	info['dungeon_md5'] = conf.getClientConfigMd5('dungeon')
	info['level_md5'] = conf.getClientConfigMd5('level')
	info['game_md5'] = conf.getClientConfigMd5('game')
	info['pet_md5'] = conf.getClientConfigMd5('pet')
	info['monster_md5'] = conf.getClientConfigMd5('monster')
	info['skill_md5'] = conf.getClientConfigMd5('skill')
	info['pet_level_md5'] = conf.getClientConfigMd5('pet_level')
	info['prompt_md5'] = conf.getClientConfigMd5('prompt')
	info['equipment_md5'] = conf.getClientConfigMd5('equipment')
	info['strength_price_md5'] = conf.getClientConfigMd5('strength_price')
	info['strength_probability_md5'] = conf.getClientConfigMd5('strength_probability')
	info['luck_md5'] = conf.getClientConfigMd5('luck')
	info['language_md5'] = conf.getClientConfigMd5('language')	
	info['stone_md5'] = conf.getClientConfigMd5('stone')
	info['stone_probability_md5'] = conf.getClientConfigMd5('stone_probability')
	info['stone_level_md5'] = conf.getClientConfigMd5('stone_level')
	info['trp_price_md5'] = conf.getClientConfigMd5('trp_price')
	info['trp_md5'] = conf.getClientConfigMd5('trp')
	return HttpResponse(json.dumps({'info':info}))
		
	
def config(request):
#	try:	
#		beginRequest(request,user)
#	except KeyError:
#		return info(request)
	data = {}	
	dungeon_config_md5 = request.GET['dungeon_md5']
	level_config_md5 = request.GET['level_md5']
	game_config_md5 = request.GET['game_md5']
	pet_config_md5 = request.GET['pet_md5']
	monster_config_md5 = request.GET['monster_md5']
	skill_config_md5 = request.GET['skill_md5']
	pet_level_config_md5 = request.GET['pet_level_md5']
	prompt_config_md5 = request.GET['prompt_md5']
	equipment_config_md5 = request.GET['equipment_md5']
	strength_price_config_md5 = request.GET['strength_price_md5']
	strength_probability_config_md5 = request.GET['strength_probability_md5']
	
	data['dungeon'] = ''
	data['level'] = ''
	data['game'] = ''
	data['pet'] = ''
	data['monster'] = ''
	data['skill'] = ''
	data['pet_level'] = ''
	data['prompt'] = ''
	data['equipment'] = ''
	data['strength_price'] = ''
	data['strength_probability'] = ''
	
	
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
	if equipment_config_md5 != conf.getClientConfigMd5('equipment'):
		data['equipment'] = conf.getClientConfig('equipment')
	if strength_price_config_md5 != conf.getClientConfigMd5('strength_price'):
		data['strength_price'] = conf.getClientConfig('strength_price')
	if strength_probability_config_md5 != conf.getClientConfigMd5('strength_probability'):
		data['strength_probability'] = conf.getClientConfig('strength_probability')
	p = json.dumps(data)
	return HttpResponse(p)
	
def get_config(request):
	
	configkey = request.GET['config']	
	data = conf.getClientConfig(configkey)	
	return HttpResponse(json.dumps(data))
	
def api(request, m, f):
	try:
		usr = beginRequest(request,user)
	except KeyError:
		return info(request)
	if viewsmap.has_key(m) :		
		fun = getattr(viewsmap[m], f)		
		ret = fun(request)		
		if not isinstance(ret, tuple):		
			notify = endRequest(request)
			yell = usr.yell_listen()
			if yell:
				notify.update(yell)
			if notify:
				ret.update({'notify':notify})		
			return HttpResponse(json.dumps(ret))
		else:
			return ret[1]
	return HttpResponse('api')


def account_new(request):
	
	accountName = request.GET['account_name']
	password = request.GET['password']	
	res = account.new(accountName, password)	
	return HttpResponse(json.dumps(res))

def test(request):	
	
	#url = r'http://127.0.0.1:1235/?cmd=save&type=test&id=587'
	#f = curl.url(url)
	#print f	
	#return HttpResponse(f, mimetype="text/plain")
	
	data = {}
	data['notify'] = {}
	data['notify']['notify_email'] = {}
	data['notify']['notify_email']['1'] = {"name": "test2", "level": 1, "roleid": 2, "id": "3", "create_time": 1381734253, "last_login": 1381734250, "type": "firend_request", "avatar_id": "e7cc74f1d4f389976bb41ee5cf33d1c4", "leader": ""}
	data['notify']['notify_email']['2'] = {"name": "test2", "level": 1, "roleid": 2, "id": "3", "create_time": 1381734253, "last_login": 1381734250, "type": "firend_request", "avatar_id": "e7cc74f1d4f389976bb41ee5cf33d1c4", "leader": ""}
	data['notify']['notify_mail'] = {}
	data['notify']['notify_mail']['1'] = {'roleid':1, 'name':'test1', 'level': '1', 'leader' : "", 'last_login' : 1381734250, 'create_time': 1381734253, 'avatar_id': 'e7cc74f1d4f389976bb41ee5cf33d1c4', 'mail': 'testmail', 'send_time':1381734253}
	data['notify']['notify_mail']['2'] = {'roleid':1, 'name':'test1', 'level': '1', 'leader' : "", 'last_login' : 1381734250, 'create_time': 1381734253, 'avatar_id': 'e7cc74f1d4f389976bb41ee5cf33d1c4', 'mail': 'testmail', 'send_time':1381734253}
	data['notify']['notify_message'] = {}
	data['notify']['notify_message']['1'] = {'roleid':1, 'name':'test1', 'level': '1', 'leader' : "", 'last_login' : 1381734250, 'create_time': 1381734253, 'avatar_id': 'e7cc74f1d4f389976bb41ee5cf33d1c4', 'message': 'testmail', 'send_time':1381734253}
	data['notify']['notify_message']['2'] = {'roleid':1, 'name':'test1', 'level': '1', 'leader' : "", 'last_login' : 1381734250, 'create_time': 1381734253, 'avatar_id': 'e7cc74f1d4f389976bb41ee5cf33d1c4', 'message': 'testmail', 'send_time':1381734253}

	return HttpResponse(json.dumps(data))