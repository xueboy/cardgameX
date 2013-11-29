#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.cache import cache

def show_ladder(request):
	
	return HttpResponse('show_ladder')
	
def stand_ladder(request):
	pass