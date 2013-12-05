#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.cache import cache
from arenarank.models import ladder

def show_ladder(request):
	
	ld = ladder.instace('ladder')
	
	return HttpResponse('show_ladder')
	
def stand_ladder(request):
	pass