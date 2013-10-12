#coding:utf-8\
#!/usr/bin/env python

import hashlib
import os
from django.http import HttpResponse
from cardgame.settings import STATIC_ROOT

def set_avatar(request):
	
	gender = request.GET['gender']
	avatar = request.body	
	usr = request.user
		
	usr.gender = gender
	if gender != "female":
		usr.gender = 'male'
	
	m = hashlib.md5(avatar)
	usr.avatar_id = m.hexdigest()
	print(m.hexdigest())
	
	file_title = "".join([str(usr.roleid), ".avt"])
	file_name = "/".join([STATIC_ROOT, "avatar", file_title])		
	f = open(file_name, "wb")
	f.write(avatar)
	f.close()
	usr.save()	
	return {'avatar_id':usr.avatar_id}
		
def get_avatar(request):
	avatar_id = request.GET['role_id']	
	file_title = "".join([avatar_id, ".avt"])
	file_name = "/".join([STATIC_ROOT, "avatar", file_title])
	
	f = open(file_name, 'rb')
	avatar = f.read()
	f.close()
	return {}, HttpResponse(avatar, mimetype="image/png")

def get_avatar_id(request):
	avatar_id = request.GET['role_id']
	file_title = "".join([avatar_id, ".avt"])
	file_name = "/".join([STATIC_ROOT, "avatar", file_title])
	
	try:
		f = open(file_name, 'rb')
		avatar = f.read()
		f.close()	
		m = hashlib.md5(avatar)		
		return {'avatar_md5':m.hexdigest()}
	except:
		return {'avatar_md5':''}