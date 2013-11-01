#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
import time
import calendar
import random


def HttpResponse500():
	response = HttpResponse()
	response.status_code = 500
	return resonse

def onUserLogin(request, usr):
	request.session['user_id'] = usr.id
	usr.onLogin()

def beginRequest(request,cls):	
	userid = request.session['user_id']
	usr = cls.get(userid)
	request.user = usr
	usr.update()
	return usr

def endRequest(request):
	user = request.user
	notify = user.notify		
	user.notify = {}
	user.save()
	return notify
		
def currentTime():
	return int(time.time())
	
def dayTime():
	return int(time.time()) % (60 * 60 * 24)
	
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
	
	
def retrieval_object(func):
	"""
	mark this funtion return a object whitch need to save db.
	"""
	def retrieval_fun(obj):
		res = func(obj)
		if not hasattr(obj , 'retriveled_object'):
			obj.retriveled_object = set()
		obj.retriveled_object.add(res)
		return res
	return retrieval_fun
	
def is_expire(daytime):
	now = currentTime()
	tm = time.gmtime(now)	
	exipre_time = calendar.timegm([tm.tm_year, tm.tm_mon, tm.tm_mday, daytime / 3600, (daytime % 3600) / 60, daytime % 60])
	return exipre_time >= now