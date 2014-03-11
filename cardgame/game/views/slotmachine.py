#coding:utf-8
#!/usr/bin/env python

from game.routine.slotmachine import slotmachine

def play(request):
	"""
	玩老虑机
	"""
	usr = request.user
	return slotmachine.play(usr)