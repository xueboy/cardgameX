#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
import time
import random


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
	
def hit(probs):
	"""
	give a weight list and randmon choose a element depend on weights as probablity.
	"""
	total = sum(probs)
	seed = random.randint(0, total)
	
	i = 0
	for p in probs:
		if total < p:
			return i
		i = i + 1
		total = total - p
		
	raise Assertion( 'unexpect result')