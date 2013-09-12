#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.gcjson import gcjson
from game.models.account import account
from game.models.user import user

def request(request):
	usr = request.user
	friendid = request.GET['friend_id']
	friend = user.get(friendid)
	if friend != None:		
		data = friend.addFriendRequest(usr)		
		return HttpResponse(gcjson.dumps(data))		
	return HttpResponse(gcjson.dumps({friend:{}}))
		
		
def confirm(request):
	usr = request.user
	isConfirm = request.GET['is_confirm']
	friendid = request.GET['friend_id']
	friend = user.get(friendid)
	if friend != None:
		if usr.confirmFriendRequest(friend, isConfirm) == 0:
			HttpResponse(gcjson.dumps({'msg': 'friend_max_count'}))
	return HttpResponse(gcjson.dumps({'friend_new': friend.getFriendData(), 'friend_request_delete': friendid}))


def search(request):
	usr = request.user	
	friendname = request.GET['friend_name']
	#friendname = unicode(friendname,'unicode-escape')
	#friendname = eval('u"' + friendname + '"')
	#friendname = eval(friendname)
#	friendname= unicode(friendname,"utf-8") 
	#s = "'" + friendname + "'.decode('unicode_escape')"
	#friendname = eval( s)
	
	

	
	friendid = account.getRoleid(friendname)	
	friend = user.get(friendid)
	
	if friend != None:
		return HttpResponse(gcjson.dumps({'friend':friend.getFriendData()}))
	else:
		return HttpResponse(gcjson.dumps({'friend': {}}))
			
			
def delete(request):
	usr = request.user	
	friendid = request.GET['friend_id'].decode('utf-8')
	if usr.deleteFriend(friendid) == 1:
		return HttpResponse(gcjson.dumps({'friend_delete':friendid}))
	else:
		return HttpResponse(gcjson.dumps({'msg':'friend_not_exist'}))