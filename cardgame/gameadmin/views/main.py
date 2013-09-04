#coding:utf-8
#!/usr/bin/env python

from django.shortcuts import render
from gclib.DBConnection import DBConnection
from django.http import HttpResponse
from gclib.gcjson import gcjson
from gclib.gcconfig import gcconfig

def index(request):
	return render(request, 'index.html', {})


def dungeon(request):
	return generalConfigRequestProcess(request, 'dungeon')		
				
def level(request):
	return generalConfigRequestProcess(request, 'level')				
				
def monster(request):
	return generalConfigRequestProcess(request, 'monster')			
				
def card(request):
	return generalConfigRequestProcess(request, 'card')
def game(request):
	return generalConfigRequestProcess(request, 'game')
				
				
def generalConfigRequestProcess(request, confname):
	if request.method == 'POST':
		confstr = request.POST['config']
		try:
			gcconfig.setConfig(confname, confstr)		
			return render(request, 'index.html', {})
		except:
			return render(request, confname + '.html', {'config':confstr})
	else:
		conf = gcconfig.getConfigStr(confname)		
		if conf != '':			
			return render(request, confname + '.html', {'config': gcconfig.getConfigStr(confname)})
		else:
			gcconfig.createConfig(confname)			
			return render(request, confname + '.html', {'config':''})