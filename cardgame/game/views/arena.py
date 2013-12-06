#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from cardgame.settings import ARENE_SERVER

def show_ladder(request):	
	usr = request.user	
	return curl.url(ARENE_SERVER +  '/arena/show_ladder/', None, {'roleid':str(usr.roleid)})
		
def stand_ladder(request):
	usr = request.user
	return curl.url(ARENE_SERVER +  '/arena/stand_ladder/', None, {'roleid':str(usr.roleid)})
		