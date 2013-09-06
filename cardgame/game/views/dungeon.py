#coding:utf-8
#!/usr/bin/env python


from django.http import HttpResponse

def enter(request):
	return HttpResponse('enter dungeon')