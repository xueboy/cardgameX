﻿#coding:utf-8
#!/usr/bin/env python

from gclib.json import json
from game.models.account import account
from game.models.user import user
from game.routine.gift import gift as giftR

def request(request):
	"""
	请求加好友
	"""
	usr = request.user
	friendid = request.GET['friend_id']
	friendid = int(friendid)
	if friendid == usr.roleid:
		return {'msg':'friend_can_not_self'}
	friend = user.get(int(friendid))
	if friend != None:		
		usrNw = usr.getNetwork()
		data = usrNw.addFriendRequest(friend)
		if data.has_key('msg'):
			return data
		return {'friend':data}
	return {'msg':'friend_not_exist'}
		
def friend_anwser(request):
	"""
	回应好友请求
	"""
	usr = request.user
	request_id = request.GET['request_id']
	option = request.GET['option']	
	usrNw = usr.getNetwork()
	return usrNw.friendRequestAnswer(request_id, option)

def search(request):
	"""
	寻找好友
	"""
	usr = request.user	
	friendname = request.GET['friend_name']
	
	friendid = account.getRoleid(friendname)
	if friendid == 0:
		return {'friend': {}}
	friend = user.get(friendid)	
	if friend != None:
		return {'friend':friend.getFriendData()}
	else:
		return {'friend': {}}
			
def delete(request):
	"""
	删除好友
	"""
	usr = request.user	
	friendid = request.GET['friend_id']
	usrNw = usr.getNetwork()
	friend = user.get(friendid)
	if not friend:
		return {'msg':'friend_not_exist'}
	return usrNw.deleteFriend(friend)	
			
def message(request):
	"""
	留言
	"""
	friendid = int(request.GET['friend_id'])
	msg = request.GET['message']
	usr = request.user
	toUser = None
	if friendid == usr.roleid:
		toUser = usr
	else:
		toUser = user.get(friendid)
	if toUser:	
		usrNw = usr.getNetwork()
		toUserNw = toUser.getNetwork()
		if toUserNw.isBan(usr.roleid):
			return {'msg':'user_is_in_ban'}
		usrNw.sendMessage(toUser, msg)
		return {}		
	return {'msg':'friend_not_exist'}
		
def get_message(request):
	"""
	刷新留言
	"""
	friendid = request.GET['friend_id']
	friend = user.get(friendid)
	if not friend:
		return {'msg':'friend_not_exist'}
	friendNw = friend.getNetwork()
	
	return {'message':friendNw.message}
	
		
def message_delete(request):
	"""
	删除留言
	"""
	messageid = request.GET['message_id']
	usr = request.user
	usrNw = usr.getNetwork()
	usrNw.deleteMessage(messageid)
	return {'message_delete': messageid}
	

def mail(request):
	"""
	发送私信
	"""
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
		
def delete_mail(request):
	"""
	删除私信
	"""
	friendid = request.GET['friend_id']
	mailid = request.GET['mail_id']
	usr = request.user
	usrNw = usr.getNetwork()
	usrNw.deleteMail(friendid, mailid)
	return {'mailid': mailid}
		
def delete_friend_mail(request):
	"""
	删除好友私信
	"""
	friendid = request.GET['friend_id']	
	usr = request.user
	usrNw = usr.getNetwork()
	usrNw.deleteFriendMail(friendid)
	return {}


def email_read(request):
	"""
	阅读邮件
	"""
	emailid = request.GET['id']
	
	usr = request.user
	usrNw = usr.getNetwork()	
	ret = usrNw.emailMarkReaded(emailid)
	if ret.has_key(emailid):
		return ret
	return {'update_email':ret}

def email_open(request):
	"""
	打开邮件
	"""
	emailid = request.GET['id']
	
	usr = request.user
	usrNw = usr.getNetwork()
	return usrNw.emailOpen(emailid)

def email_delete(request):
	"""
	删除邮件
	"""
	emailid = request.GET['id']
	
	usr = request.user
	usrNw = usr.getNetwork()
	return usrNw.emailDelete(emailid)
	
		
def ban(request):
	"""
	阻止好友
	"""
	banid = request.GET['ban_id']
	
	usr = request.user
	banUser = user.get(banid)
	if banUser:
		usrNw = usr.getNetwork()
		usrNw.ban(banid, banUser.name)
		return {}		
	return {'msg':'friend_not_exist'}
	
def yell(request):	
	"""
	世界聊天
	"""
	message = request.GET['message']
	usr = request.user
	usrNw = usr.getNetwork()
	return usrNw.yell(usr.name, message)
	
def gift(request):
	"""
	送礼
	"""
	item = request.GET['item']
	usr = request.user
	friendid = request.GET['friendid']
	return giftR.send_gift(usr, item, friendid)
	
def gift_ladder(request):
	"""
	送礼排行榜
	"""
	tp = request.GET['type']
	begin = request.GET['begin']
	end = request.GET['end']
	usr = request.user
	return giftR.gift_ladder(usr, tp, begin, end)
	