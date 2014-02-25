#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
import time
import datetime
import calendar
import random

from gclib.exception import NotHaveNickname, NotLogin
from gclib.cache import cache, cachekey_usr_session_profix

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
	
def getAccountId(request):
	return request.session['account_id']
	
def onAccountLogin(request, acc):
	request.session['account_id'] = acc.id	
	acc.onLogin()
	return acc

def cache_session_key(roleid):
	return cachekey_usr_session_profix + str(roleid)

def onUserLogin(request, usr):
	request.session['user_id'] = usr.id
	request.session.save()
	cskey  = cache_session_key(usr.id)	
	cache.mc_setValue(cskey, request.session.session_key)
	usr.accountid = request.session['account_id']
	return usr.onLogin()

def beginRequest(request,cls):
	
	if not request.session.has_key('account_id'):
		raise NotLogin	
	if not request.session.has_key('user_id'):
		raise NotHaveNickname

	userid = request.session['user_id']
	cskey = cache_session_key(userid)	
	session_key = cache.mc_getValue(cskey)	
	if request.session.session_key != session_key:
		logout(request)
		raise NotLogin
	
	usr = cls.get(userid)
	usr.accountid = request.session['account_id']	
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

def currentTime():
	return int(time.time())
	
def dayTime():
	return int(time.time()) % (60 * 60 * 24)

def logout(request):
	request.session.flush()
	
	
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

def randbigint():
	return random.randint(0, 1000000)

def retrieval_object(func):
	"""
	mark this funtion return a object whith need to save db.
	"""
	def retrieval_fun(obj):		
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
	return exipre_time > t
	
def is_same_day(t1, t2):
	if not t1:
		return False
	if not t2:
		return False
		
	t1tm = time.gmtime(t1)	
	t2tm = time.gmtime(t2)	
	return (t1tm.tm_year == t2tm.tm_year) and (t1tm.tm_mon == t2tm.tm_mon) and (t1tm.tm_mday == t2tm.tm_mday)
	
def day_diff(t1, t2):
	d1 = datetime.datetime.fromtimestamp(t1)
	d2 = datetime.datetime.fromtimestamp(t2)
	return (d1 - d2).days

def str_to_time(s):
	return int(time.mktime(datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').timetuple()))
	
def str_to_day_time(s):
	return datetime.datetime.strptime(s, '%H:%M:%S').time()

def str_to_date_time(s):
	return datetime.datetime.strptime(s, '%Y-%m-%d').time()
	
def time_to_str(t):
	return datetime.strftime(t, '%Y-%m-%d %H:%M:%S')
	
def day_time_to_str(t):
	return datetime.strftime(t, '%H:%M:%S')

def time_to_day_time(t):
	return datetime.datetime.fromtimestamp(t).time()
	
def is_in_day_period(td1, td2, t):		
		nowDayTime = time_to_day_time(t)		
		if td1 > nowDayTime or td2 < nowDayTime:
			return False
		return True
	
	
	