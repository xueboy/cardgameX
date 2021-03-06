﻿#coding:utf-8
#!/usr/bin/env python

import hashlib
import os
import math
from django.http import HttpResponse
from gclib.utility import getAccountId
from gclib.DBConnection import DBConnection
from game.utility.config import config
from game.models.account import account
from game.routine.avatar import avatar
from game.routine.signin import signin
from game.models.user import user
from game.routine.levelup import levelup
from game.routine.arena import arena
from game.routine.invite import invite
from game.routine.pet import pet
from game.routine.explore import explore as exploreR

def set_avatar(request):	
	"""
	设置avatar
	"""
	
	body = request.body	
	usr = request.user
		
	m = hashlib.md5(body)
	usr.avatar_id = avatar.setAvatar(usr.roleid, body)
	arena.set_avatar_id(usr.roleid, usr.avatar_id)
	
	usr.save()	
	if usr.avatar_id:
		return {'avatar_id':usr.avatar_id}
	else:
		return {msg:'avator_io_error'}	
		
def get_avatar(request):
	"""
	得到avatar
	"""
	avatar_id = request.GET['role_id']	
	body = avatar.getAvatar(avatar_id)
	return {}, HttpResponse(body, mimetype="image/png")

def get_avatar_id(request):
	"""
	得到avatar id
	"""
	roleid = request.GET['role_id']	
	return {'avatar_md5':avatar.getAvatarId(roleid)}			
			
def idle(request):
	"""
	空闲
	"""
	return {}
	
def show(request):	
	"""
	显示
	"""
	roleid = request.GET['role_id']	
	other = user.get(roleid)
	if not other:
		return {'msg':'user_not_exist'}
	
	otNw = other.getNetwork()
	data = {}
	data['roleid'] = other.roleid
	data['name'] = other.name
	data['gender'] = other.gender	
	data['level'] = other.level
	data['vip_level'] = other.vip['level']
	data['message'] = otNw.message	
	return data
	
	
def locate(request):
	"""
	定位
	"""
	longitude = request.GET['longitude']
	latitude = request.GET['latitude']	
	
	longitude = float(longitude)
	latitude = float(latitude)
	
	if longitude > 180 or longitude < -180:
		return {'msg':'parameter_bad'}
	if latitude > 360 or latitude < -360:
		return {'msg':'parameter_bad'}	
	usr = request.user
	accountid = getAccountId(request)
	usr.longitude = longitude
	usr.latitude = latitude
	account.locate(accountid, longitude, latitude)
	usr.save()
	return {}
	
def nearby(request):
	"""
	显示周围玩家
	"""
	gameConf = config.getConfig('game')
	
	longitude = float(request.GET['longitude'])
	latitude = float(request.GET['latitude']	)
	usr = request.user	
	raidus = gameConf['player_near_by_raidus']		
	degree = (24901*1609)/360.0
	raidusMile = raidus
	dpmLat = 1 / degree
	radiusLat = dpmLat * raidusMile
	minLat = latitude - radiusLat
	maxLat = latitude + radiusLat
	
	mpdLng = degree * math.cos(latitude * (math.pi / 180))
	dpmLng = 1 / mpdLng
	radiusLng = dpmLng * raidusMile;  
	minLng = longitude - radiusLng;  
	maxLng = longitude + radiusLng;
  
	res = account.getRange(minLng, maxLng, minLat, maxLat, gameConf['player_near_by_count'])
	data = []
	for r in res:
		d = {}
		roleid = r[0]
		longitude = r[1]
		latitude = r[2]
		player = user.get(roleid)
		if not player:
			continue
		d['roleid'] = roleid
		d['longitude'] = longitude
		d['latitude'] = latitude
		d['avatar_id'] = avatar.getAvatarId(roleid)
		d['name'] = player.name
		d['level'] = player.level
		d['gender'] = player.gender
		data.append(d)  	
	return {'player':data}
	
def sign_in(request):	
	"""
	签到
	"""
	usr = request.user	
	return signin.do_signin(usr)
	
def levelup_award(request):
	"""
	升级奖励
	"""
	usr = request.user
	level = int(request.GET['level'])
	return levelup.award(usr, level)
	
def meal(request):
	"""
	用餐
	"""
	usr = request.user
	return signin.meal(usr)
	
def continue_award(request):
	"""
	连续登陆奖励
	"""
	usr = request.user
	no = request.GET['no']
	return signin.continue_award(usr)
	
def draw_award(request):
	"""
	开服登陆奖励
	"""
	usr = request.user
	position = int(request.GET['position'])
	return signin.draw_award(usr, position)
	
def detail(request):
	"""
	玩家详细信息
	"""
	roleid = request.GET['role_id']	
	other = user.get(roleid)
	if not other:
		return {'msg':'user_not_exist'}	
	return other.getBattleData()
	
def scene(request):
	"""
	场影中玩家
	"""
	idx = int(request.GET['index'])
	sql = 'SELECT roleid from account WHERE roleid <> 0 ORDER BY lastlogin, gender LIMIT %s, %s'	
	conn = DBConnection.getConnection()
	gameConf = config.getConfig('game')
	data = {}
	data['player'] = []
	res = conn.query(sql, [idx, gameConf['scene_player_count']])	
	for rid in res:		
		try:
			u = user.get(rid[0])
			if u:
				data['player'].append(u.getSceneData())
		except:
			pass
	
	return data
			
def pk(request):
	"""
	PK
	"""
	roleid = request.GET['roleid']
	other = user.get(roleid)
	if not other:
		return {'msg':'usr_not_exist'}
	pvpData= other.pvpProperty()	
	return {'pvpProperty':pvpData}
		
		
def invite_code(request):
	"""
	邀请码
	"""
	invCode = request.GET['invite_code']	
	usr = request.user	
	return invite.enterInviteCode(usr, invCode)
	
def invite_award(request):
	"""
	邀请奖励
	"""
	invCount = int(request.GET['invite_count'])
	usr = request.user
	return invite.inviteAward(usr, invCount)
	
def get_born_card(request):
	"""
	领取出生宠物
	"""
	cardid = request.GET['cardid']
	usr = request.user		
	return pet.select_born_pet(usr, cardid)
	
def explore(request):
	"""
	探索
	"""
	usr = request.user
	return exploreR.explore(usr)
	
def explore_buy_critical(request):
	"""
	探索购买暴击
	"""
	usr = request.user
	return exploreR.buy_critical_times(usr)