#coding:utf-8
#!/usr/bin/env python

from gclib.DBConnection import DBConnection
from django.shortcuts import render
from django.http import HttpResponse
from game.routine.arena import arena

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			
			conn = DBConnection.getConnection()
			res = conn.query("SELECT * FROM admin WHERE username = %s AND password = %s", [username, password])
			if len(res) == 1:
				return render(request, 'index.html', {})
			else:
				return HttpResponse(res)
			
	else:
		return render(request, 'login.html', {})
		
def arena_tool(request):
	ld = arena.show_all()
	return render(request, 'arena_tool.html',  {'ladder':ld})