#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.cache import cache
from arenarank.models import ladder

def show_ladder(request):
	
	roleid = request.GET['roleid']
	
	ld = ladder.instace('ladder')
	ld.show(roleid)
	
	return HttpResponse('show_ladder')
	
def stand_ladder(request):
	pass