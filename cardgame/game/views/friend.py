#coding:utf-8
#!/usr/bin/env python

from gclib.json import json
from game.models.account import account
from game.models.user import user

def request(request):
	usr = request.user
	friendid = request.GET['friend_id']
	friend = user.get(int(friendid))
	if friend != None:		
		usrNw = usr.getNetwork()
		data = usrNw.addFriendRequest(friend)		
		return {'friend':data}
	return {'msg':'friend_not_exist'}
		
def email_anwser(request):
	usr = request.user
	mailid = request.GET['email_id']
	option = request.GET['option']	
	usrNw = usr.getNetwork()
	return usrNw.emailAnswer(mailid, option)

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
	friend = user.get(friendid)
	if not friend:
		return {'msg':'friend_not_exist'}
	return usrNw.deleteFriend(friend)	
			
def message(request):
	friendid = request.GET['friend_id']
	msg = request.GET['message']
	usr = request.user
	toUser = None
	if friendid == usr.roleid:
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
	return {'msg':'friend_not_exist'}
		
def message_delete(request):
	messageid = request.GET['message_id']
	usr = request.user
	usrNw = usr.getNetwork()
	usrNw.deleteMessage(messageid)
	return {'message_delete': messageid}
	

def mail(request):
	friendid = request.GET['friend_id']
	mail = request.GET['mail']
	usr = request.user	
	
	if friendid == usr.roleid:
		return {'msg':'friend_can_not_self'}
			
	toUser = user.get(friendid)
	if toUser:
		toUserNw = toUser.getNetwork()
		if toUserNw.isBan(usr.roleid):
			return {'msg':'user_is_in_ban'}
		usrNw = usr.getNetwork()
		usrNw.sendMail(toUser, mail)
		return {}
	return {'msg':'friend_not_exist'}

def email_read(request):
	emailid = request.GET['email_id']
	
	usr = request.user
	usrNw = usr.getNetwork()	
	ret = usrNw.emailMarkReaded(emailid)
	return {'update_email':ret}

def email_delete(request):
	emailid = request.GET['email_id']
	
	usr = request.user
	usrNw = usr.getNetwork()
	return usrNw.emailDelete(emailid)
	
		
def ban(request):
	banid = request.GET['ban_id']
	
	usr = request.user
	banUser = user.get(banid)
	if banUser:
		usrNw = usr.getNetwork()
		usrNw.ban(banid, banUser.name)
		return {}		
	return {'msg':'friend_not_exist'}
	
def yell(request):	
	message = request.GET['message']
	usr = request.user
	usrNw = usr.getNetwork()
	return usrNw.yell(usr.name, message)