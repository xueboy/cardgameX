#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
import time
import datetime
import calendar
import random

from gclib.exception import NotHaveNickname, NotLogin


def HttpResponse500():
	response = HttpResponse()
	response.status_code = 500
	return resonse


def getAccount(request, cls):
	if not request.session.has_key('account_id'):
		raise NotLogin		
	accountid = request.session['account_id']
	acc = cls.get(accountid)
	return acc
	

def onAccountLogin(request, acc):
	request.session['account_id'] = acc.id
	acc.onLogin()
	return acc

def onUserLogin(request, usr):
	request.session['user_id'] = usr.id
	usr.onLogin()

def beginRequest(request,cls):
	
	if not request.session.has_key('account_id'):
		raise NotLogin		
	
	if not request.session.has_key('user_id'):
		raise NotHaveNickname
	userid = request.session['user_id']
	usr = cls.get(userid)
	if not usr:
		raise NotHaveNickname	
	request.user = usr
	usr.update()
	return usr

def endRequest(request):
	user = request.user
	notify = user.notify
	user.notify = {}
	user.save()
	return notify
		
def saveUser(request):
	usr = request.user
	if hasattr(usr, 'retriveled_object'):
		for obj in usr.retriveled_object:
			obj.do_save()
	usr.do_save()
	
		
def currentTime():
	return int(time.time())
	
def dayTime():
	return int(time.time()) % (60 * 60 * 24)

def logout(request):
	del request.session['user_id']
	del request.session['account_id']
	
	
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
	seed = randint()
	return seed < weight
	
	
def randint():
	return random.randint(0, 10000)
	
	
def retrieval_object(func):
	"""
	mark this funtion return a object whitch need to save db.
	"""
	def retrieval_fun(obj):
		print obj
		res = func(obj)
		if not hasattr(obj , 'retriveled_object'):
			obj.retriveled_object = set()
		obj.retriveled_object.add(res)
		
		return res
	return retrieval_fun
	
def is_expire(daytime, t):
	now = currentTime()
	tm = time.gmtime(now)	
	exipre_time = calendar.timegm([tm.tm_year, tm.tm_mon, tm.tm_mday, daytime / 3600, (daytime % 3600) / 60, daytime % 60])
	return exipre_time < t
	
def is_same_day(t1, t2):
	t1tm = time.gmtime(t1)
	t2tm = time.gmtime(t2)
	return (t1tm.tm_year == t2tm.tm_year) and (t1tm.tm_mon == t2tm.tm_mon) and (t1tm.tm_mday == t2tm.tm_mday)
	
def day_diff(t1, t2):
	d1 = datetime.datetime(t1)
	d2 = datetime.datetime(t2)
	return (d1 - d2).days

