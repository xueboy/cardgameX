#coding:utf-8
#!/usr/bin/env python

from django.shortcuts import render
from gclib.DBConnection import DBConnection
from django.http import HttpResponse
from gclib.gcjson import gcjson

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
				
				
def generalConfigRequestProcess(request, confname):
	if request.method == 'POST':
		confstr = request.POST['config']
		try:
			confjson = gcjson.loads(confstr)		
			conn = DBConnection.getConnection();
			conn.excute("UPDATE config SET conf = %s WHERE confname = %s", [confstr, confname])
			return render(request, 'index.html', {})
		except:
			return render(request, confname + '.html', {'config':confstr})
	else:
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM config WHERE confname = %s", [confname])
		if len(res) == 1:			
			return render(request, confname + '.html', {'config': res[0][2]})
		else:
			conn.excute("INSERT INTO config (confname, conf) VALUES (%s, '')", [confname])
			return render(request, confname + '.html', {'config':''})