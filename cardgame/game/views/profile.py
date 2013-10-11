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

	old_file_title = "".join([usr.avatar_id, ".avt"])
	old_file_name = "/".join([STATIC_ROOT, "avatar", old_file_title])
	usr.gender = gender
	if gender != "female":
		usr.gender = 'male'
	
	m = hashlib.md5(avatar)		
	avatar_id = "".join([m.hexdigest() , str(usr.roleid)])
	file_title = "".join([avatar_id, ".avt"])
	file_name = "/".join([STATIC_ROOT, "avatar", file_title])
	usr.avatar_id = avatar_id
	
	if old_file_name != file_name:
		f = open(file_name, "wb")
		f.write(avatar)
		f.close()
		usr.save()
		os.remove(old_file_name)
	return {'avatar_id':avatar_id}
		
def get_avatar(request):
	avatar_id = request.GET['avatar_id']	
	file_title = "".join([avatar_id, ".avt"])
	file_name = "/".join([STATIC_ROOT, "avatar", file_title])
	
	f = open(file_name, 'rb')
	avatar = f.read()
	f.close()
	return {}, HttpResponse(avatar, mimetype="image/png")
