#coding:utf-8
#!/usr/bin/env python

from game.routine.educate import educate


def call(request):
	usr = request.user
	return educate.call(usr)
	
def start(request):
	usr = request.user
	edu_slot_pos = int(request.GET['edu_slot'])
	cardid = request.GET['card']
	return educate.start(usr, edu_slot_pos, cardid)
	
def stop(request):
	usr = request.user
	edu_slot_pos = int(request.GET['edu_slot'])
	return educate.stop(usr, edu_slot_pos)
