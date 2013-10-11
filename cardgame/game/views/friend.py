#coding:utf-8
#!/usr/bin/env python

from gclib.gcjson import gcjson
from game.models.account import account
from game.models.user import user

def request(request):
	usr = request.user
	friendid = request.GET['friend_id']
	friend = user.get(int(friendid))
	if friend != None:		
		friendNw = friend.getNetwork()
		data = friendNw.addFriendRequest(usr)		
		return data
	return {friend:{}}
		
		
def confirm(request):
	usr = request.user
	isConfirm = request.GET['is_confirm']
	friendid = request.GET['friend_id']
	friend = user.get(int(friendid))	
	if friend != None:
		friendNw = friend.getNetwork()
		usrNw = usr.getNetwork()
		if usrNw.confirmFriendRequest(friend, isConfirm) == 0:
			return {'msg': 'friend_max_count'}
	if isConfirm == '0':
		return {'friend_request_delete': friendid}
	else:
		return {'friend_new': friend.getFriendData(), 'friend_request_delete': friendid}


def search(request):
	usr = request.user	
	friendname = request.GET['friend_name']
	
	friendid = account.getRoleid(friendname)	
	friend = user.get(friendid)	
	if friend != None:
		return {'friend':friend.getFriendData()}
	else:
		return {'friend': {}}
			
			
def delete(request):
	usr = request.user	
	friendid = request.GET['friend_id']
	usrNw = usr.getNetwork()
	if usrNw.deleteFriend(friendid) == 1:
		return {'friend_delete':friendid}
	else:
		return {'msg':'friend_not_exist'}
			
def message(request):
	friendid = request.GET['friend_id']
	msg = request.GET['message']
	usr = request.user
	toUser = None
	if friend_id == usr.roleid:
		toUser = usr
	else:
		toUser = user.get(int(friendid))
	if toUser:	
		usrNw = usr.getNetwork()
		toUserNw = toUser.getNetwork()
		if toUserNw.isBan(usr.roleid):
			return {'msg':'user_is_in_ban'}
		usrNw.sendMessage(toUser, msg)
		return {}			
	return {'msg':'friend_not_found'}
		
def mail(request):
	friendid = request.GET['friend_id']
	mail = request.GET['mail']
	usr = request.user	
	
	if friendid == usr.roleid:
		return {'msg':'friend_can_not_self'}
			
	toUser = user.get(friend_id)
	if toUser:
		if toUserNw.isBan(usr.roleid):
			return {'msg':'user_is_in_ban'}
		usrNw.sendMail(toUser, mail)
		return {}
	return {'msg':'friend_not_found'}

	
		
def ban(request):
	banid = request.GET['ban_id']
	
	usr = request.user
	banUser = user.get(banid)
	if banUser:
		usrNw = usr.getNetwork()
		usrNw.ban(banid, banUser.name)
		return {}		
	return {'msg':'friend_not_found'}
	