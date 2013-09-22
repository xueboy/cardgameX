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
	print(request.session.keys())
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
	seed = random.randint(0, total - 1)
	
	i = 0
	for p in probs:
		if seed < p:
			return i
		i = i + 1
		seed = seed - p
		
	raise Assertion( 'unexpect result')
	
def drop(weight):
	"""
	give a weight and test if drop
	"""
	seed = random.randint(0, 1000)
	return seed < weight
	
	
def randint():
	return random.randint(0, 1000)