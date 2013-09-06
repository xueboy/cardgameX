#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
import time


def HttpResponse500():
	response = HttpResponse()
	response.status_code = 500
	return resonse

def onUserLogin(request, usr):
	request.session['user_id'] = usr.id
	usr.onLogin()

def amendRequest(request,cls):
	userid = request.session['user_id']
	usr = cls.get(userid)
	request.user = usr
	usr.update()
		
		
def currentTime():
	return int(time.time())