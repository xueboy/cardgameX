#coding:utf-8
#!/usr/bin/env python

from game.routine.educate import educate


def call(request):
	"""
	召唤训练师
	"""
	usr = request.user
	return educate.call(usr)
	
def start(request):
	"""
	开始训练
	"""
	usr = request.user
	edu_slot_pos = int(request.GET['edu_slot'])
	cardid = request.GET['card']
	return educate.start(usr, edu_slot_pos, cardid)
	
def stop(request):
	"""
	停卡训练
	"""
	usr = request.user
	edu_slot_pos = int(request.GET['edu_slot'])
	return educate.stop(usr, edu_slot_pos)

def open_slot(request):
	"""
	打开槽位
	"""
	usr = request.user	
	return educate.open_edu_solt(usr)
	