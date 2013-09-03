#coding:utf-8
#!/usr/bin/env python

from django.shortcuts import render
from gclib.DBConnection import DBConnection
from django.http import HttpResponse
from gclib.gcjson import gcjson

def index(request):
	return render(request, 'index.html', {})


def dungeon(request):
	if request.method == 'POST':
		confstr = request.POST['config']
		try:
			confjson = gcjson.loads(confstr)		
			conn = DBConnection.getConnection();
			conn.excute("UPDATE config SET conf = %s WHERE confname = 'dungeon'", [confstr])
			return render(request, 'index.html', {})
		except:
			return render(request, 'dungeon.html', {'config':confstr})
	else:
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM config WHERE confname = %s", ['dungeon'])
		if len(res) == 1:			
			return render(request, 'dungeon.html', {'config': res[0][2]})
		else:
			conn.excute("INSERT INTO config (confname, conf) VALUES ('dungeon', '')", [])
			return render(request, 'dungeon.html', {'config':''})
				
def level(request):
	if request.method == 'POST':
		confstr = request.POST['config']
		try:
			confjson = gcjson.loads(confstr)		
			conn = DBConnection.getConnection();
			conn.excute("UPDATE config SET conf = %s WHERE confname = 'level'", [confstr])
			return render(request, 'index.html', {})
		except:
			return render(request, 'level.html', {'config':confstr})
	else:
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM config WHERE confname = %s", ['level'])
		if len(res) == 1:			
			return render(request, 'level.html', {'config': res[0][2]})
		else:
			conn.excute("INSERT INTO config (confname, conf) VALUES ('level', '')", [])
			return render(request, 'level.html', {'config':''})