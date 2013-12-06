#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from gclib.cache import cache
from gclib.json import json
from arenarank.models import ladder

def show_ladder(request):	
			
	roleid = request.REQUEST['roleid'][0]	
	ld = ladder.instance('ladder')
	return HttpResponse(json.dumps( ld.show(roleid)))	
	
def stand_ladder(request):
	
	roleid = request.REQUEST['roleid'][0]
	
	ld = ladder.instance('ladder')
	return HttpResponse(json.dumps(ld.stand(roleid)))
	
