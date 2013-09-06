#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson

def friend_request(request):
	usr = request.user
	friendid = request.GET['friend_id']
	friend = user.get(friendid)
	if friend != None:		
		friend.addFriendRequest(usr.roleid, {'name': usr.name, 'level': usr.level, 'last_login': usr.last_login, 'leader': usr.leader})
	return HttpResponse(gcjson.dumps('OK'))
		
		
def friend_confirm(request):
	usr = request.user
	isConfirm = request.GET['is_confirm']
	friendid = request.GET['friend_id']
	friend = user.get(friendid)
	if friend != None:		
		usr.confirmFriendRequest(friend, isConfirm)		
	return HttpResponse(gcjson.dumps({'friends': usr.friends, 'friend_request': usr.friend_request}))
		