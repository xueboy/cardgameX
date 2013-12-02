#coding:utf-8\
#!/usr/bin/env python

import sys
from django.http import HttpResponse
from gclib.json import *
from gclib.curl import curl
from game.utility.config import config as conf
from game.models.account import account
from gclib.utility import HttpResponse500, getAccount, beginRequest, onAccountLogin, onUserLogin, currentTime, endRequest, logout, saveUser
from gclib.exception import NotLogin, NotHaveNickname
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
import game.views.educate
import game.views.skill
import game.views.arena


viewsmap = {
	'dungeon':sys.modules['game.views.dungeon'],
	'gm':sys.modules['game.views.gm'],
	'card':sys.modules['game.views.card'],
	'friend':sys.modules['game.views.friend'],
	'profile': sys.modules['game.views.profile'],
	'equipment': sys.modules['game.views.equipment'],
	'luckycat': sys.modules['game.views.luckycat'],
	'stone': sys.modules['game.views.stone'],
	'educate': sys.modules['game.views.educate'],
	'skill': sys.modules['game.views.skill'],
	'arena' : sys.modules['game.views.arena'],
}

def index(request):
	account_name = request.GET['account_name']
	pwd = request.GET['password']
	acc = account.login(account_name, pwd)
	if acc != None:
		onAccountLogin(request, acc)
		if not acc.nickname:
			return HttpResponse(json.dumps({'msg':'nickname_should_set_before'}))
		usr = acc.getUser()
		if usr == None:
			raise Http500("server error")
			return HttpResponse500()
		onUserLogin(request, usr)
		usr.last_login = currentTime()
		
		data = usr.getLoginData()			
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
	info['educate_md5'] = conf.getClientConfigMd5('educate')
	info['educate_grade_md5'] = conf.getClientConfigMd5('educate_grade')
	info['almanac_combination_md5'] = conf.getClientConfigMd5('almanac_combination')
	info['reborn_md5'] = conf.getClientConfigMd5('reborn')
	return HttpResponse(json.dumps({'info':info}))


def get_config(request):
	
	configkey = request.GET['config']	
	data = conf.getClientConfig(configkey)	
	return HttpResponse(json.dumps(data))
	
def api(request, m, f):
	try:		
		usr = beginRequest(request,user)		
	except NotLogin:		
		return info(request)
	except NotHaveNickname:		
		return HttpResponse(json.dumps({'msg':'nickname_should_set_before'}))
		
	if viewsmap.has_key(m) :		
		fun = getattr(viewsmap[m], f)		
		ret = fun(request)
		saveUser(request)	
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


def new_account(request):
	
	accountName = request.GET['account_name']
	password = request.GET['password']	
	res = account.new(accountName, password)	
	return HttpResponse(json.dumps(res))
	
def set_nickname(request):
	
	nickname = request.GET['nickname']
	gender = request.GET['gender']
	
	if gender != 'male' and gender != 'female':
		return HttpResponse(json.dumps({'msg':'gender_out_of_except'}))	
	try:
		acc = getAccount(request, account)
	except NotLogin:
		return info(request)
	if acc.nickname:
		return HttpResponse(json.dumps({'msg':'nickname_already_have'}))
	acc.nickname = nickname
	acc.gender = gender
	usr = acc.makeUserAndBind(nickname, gender)		
	data = usr.getLoginData()	
	return HttpResponse(json.dumps(data))
	

def exit(request):
	logout(request)
	return HttpResponse('exist')


def test(request):	
	from gclib.cache import cache	
	#url = r'http://127.0.0.1:1235/?cmd=save&type=test&id=587'
	#f = curl.url(url)
	#print f	
	#return HttpResponse(f, mimetype="text/plain")	
#	data = {}
#	data['notify'] = {}
#	data['notify']['notify_email'] = {}
#	data['notify']['notify_email']['1'] = {"name": "test2", "level": 1, "roleid": 2, "id": "3", "create_time": 1381734253, "last_login": 1381734250, "type": "firend_request", "avatar_id": "e7cc74f1d4f389976bb41ee5cf33d1c4", "leader": ""}
#	data['notify']['notify_email']['2'] = {"name": "test2", "level": 1, "roleid": 2, "id": "3", "create_time": 1381734253, "last_login": 1381734250, "type": "firend_request", "avatar_id": "e7cc74f1d4f389976bb41ee5cf33d1c4", "leader": ""}
#	data['notify']['notify_mail'] = {}
#	data['notify']['notify_mail']['1'] = {'roleid':1, 'name':'test1', 'level': '1', 'leader' : "", 'last_login' : 1381734250, 'create_time': 1381734253, 'avatar_id': 'e7cc74f1d4f389976bb41ee5cf33d1c4', 'mail': 'testmail', 'send_time':1381734253}
#	data['notify']['notify_mail']['2'] = {'roleid':1, 'name':'test1', 'level': '1', 'leader' : "", 'last_login' : 1381734250, 'create_time': 1381734253, 'avatar_id': 'e7cc74f1d4f389976bb41ee5cf33d1c4', 'mail': 'testmail', 'send_time':1381734253}
#	data['notify']['notify_message'] = {}
#	data['notify']['notify_message']['1'] = {'roleid':1, 'name':'test1', 'level': '1', 'leader' : "", 'last_login' : 1381734250, 'create_time': 1381734253, 'avatar_id': 'e7cc74f1d4f389976bb41ee5cf33d1c4', 'message': 'testmail', 'send_time':1381734253}
#	data['notify']['notify_message']['2'] = {'roleid':1, 'name':'test1', 'level': '1', 'leader' : "", 'last_login' : 1381734250, 'create_time': 1381734253, 'avatar_id': 'e7cc74f1d4f389976bb41ee5cf33d1c4', 'message': 'testmail', 'send_time':1381734253}

	data = []
	for i in range(1000000):
		#rd = {"name": "test2", "level": 1, "roleid": 2, "id": "3", "create_time": 1381734253, "last_login": 1381734250, "type": "firend_request", "avatar_id": "e7cc74f1d4f389976bb41ee5cf33d1c4", "member": ['pet10052_2', 'pet10052_2', 'pet10052_2', 'pet10052_2', 'pet10052_2']}
		data.append(i)

	cache.loc_setValue('test_rank', data)
	dt = cache.loc_getValue('test_rank')
	#print dt
	#json.loads(dt)
	return HttpResponse(dt)