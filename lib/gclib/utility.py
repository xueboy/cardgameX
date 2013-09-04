#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
import time


def HttpResponse500():
	response = HttpResponse()
	response.status_code = 500
	return resonse

def onLogin(request, user):
	request.session['user_id'] = user.id

def amendRequest(request,cls):
	userid = request.session['user_id']
	usr = cls.get(userid)
	print cls, userid
	request.user = usr
	usr.update1()
		
		
def currentTime():
	return int(time.time())