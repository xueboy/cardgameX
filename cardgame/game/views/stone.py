#coding:utf-8
#!/usr/bin/env python

from game.routine.stone import stone

def visit(request):
	
	usr = request.user
	return stone.visit(usr)
	
def visit_level(request):
	
	usr = request.user
	level = int(request.GET['vlevel'])
	return stone.visit_level(usr, level)
	