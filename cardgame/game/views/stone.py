#coding:utf-8
#!/usr/bin/env python

from game.routine.stone import stone

def visit(request):
	
	usr = request.user
	level = int(request.GET['vlevel'])
	return stone.visit(usr, level)
	
def visit_gem(request):
	
	usr = request.user
	level = int(request.GET['vlevel'])
	return stone.visit_gem(usr, level)
	
	
def levelup(request):
	
	
	