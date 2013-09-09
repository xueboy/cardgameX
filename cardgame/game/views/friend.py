#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson



def friend_request(request):
	usr = request.user
	friendid = request.GET['friend_id']
	friend = user.get(friendid)
	if friend != None:		
		friend.addFriendRequest(usr.roleid, usr)
	return HttpResponse(gcjson.dumps('OK'))
		
		
def friend_confirm(request):
	usr = request.user
	isConfirm = request.GET['is_confirm']
	friendid = request.GET['friend_id']
	friend = user.get(friendid)
	if friend != None:		
		usr.confirmFriendRequest(friend, isConfirm)		
	return HttpResponse(gcjson.dumps({'friends': usr.friends, 'friend_request': usr.friend_request}))


def search_friend(request):
	usr = request.user
	
	friendname = request.GET['friend_name']
	
	from game.models.account import account
	from game.models.user import user
	friendid = account.getRoleid(friendname)
	
	friend = user.get(friendid)
	if friend != None:
		return HttpResponse(gcjson.dumps({'friend':friend.getFriendData()}))
	else:
		return HttpResponse(gcjson.dumps({'friend': {}}))