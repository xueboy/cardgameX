#coding:utf-8\
#!/usr/bin/env python

import hashlib
import os
import math
from django.http import HttpResponse
from gclib.utility import getAccountId
from game.models.account import account
from game.routine.avatar import avatar


from game.models.user import user

def set_avatar(request):
	
	gender = request.GET['gender']
	body = request.body	
	usr = request.user
		
	m = hashlib.md5(avatar)
	usr.avatar_id = avatar.setAvatar(usr.roleid, body)
	
	usr.save()	
	if usr.avatar_id:
		return {'avatar_id':usr.avatar_id}
	else:
		return {msg:'avator_io_error'}	
		
def get_avatar(request):
	avatar_id = request.GET['role_id']	
	body = avatar.getAvatar(avatar_id)
	return {}, HttpResponse(body, mimetype="image/png")

def get_avatar_id(request):
	roleid = request.GET['role_id']	
	return {'avatar_md5':avatar.getAvatarId(roleid)}			
			
def idle(request):
	return {}
	
def show(request):	
	roleid = request.GET['role_id']	
	other = user.get(roleid)
	if not other:
		return {'msg':'user_not_exist'}
	
	otNw = other.getNetwork()
	data = {}
	data['name'] = other.name
	data['level'] = other.level
	data['message'] = otNw.message	
	return data
	
	
def locate(request):
	
	longitude = request.GET['longitude']
	latitude = request.GET['latitude']	
	usr = request.user
	accountid = getAccountId(request)
	account.locate(accountid, longitude, latitude)
	return {}
	
def nearby(request):
	
	
	longitude = float(request.GET['longitude'])
	latitude = float(request.GET['latitude']	)
	usr = request.user
	
	raidus = 1000
	
	earth_radius = 6378137
	rad = math.pi
	
	degree = (24901*1609)/360.0
	raidusMile = raidus
	dpmLat = 1 / degree
	radiusLat = dpmLat * raidusMile
	minLat = latitude - radiusLat
	maxLat = latitude + radiusLat
	
	mpdLng = degree * math.cos(latitude * (math.pi / 180))
	dpmLng = 1 / mpdLng
	radiusLng = dpmLng*raidusMile;  
	minLng = longitude - radiusLng;  
	maxLng = longitude + radiusLng;
  
	res = account.getRange(minLng, maxLng, minLat, maxLat)
	data = []
	for r in res:
		d = {}
		roleid = r[0]
		longitude = r[1]
		latitude = r[2]
		d['roleid'] = roleid
		d['longitude'] = longitude
		d['latitude'] = latitude
		d['avatar_id'] = avatar.getAvatarId(roleid)
		data.append(d)
  	
	return data