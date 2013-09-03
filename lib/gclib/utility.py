#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse


def HttpResponse500():
	response = HttpResponse()
	response.status_code = 500
	return resonse

def onLogin(request, user):
	request.session['user_id'] = user.id

def amendRequest(request):
	userid = request.session['user_id']	
	request.user = user.get(userid)