#coding:utf-8
#!/usr/bin/env python

from django.shortcuts import render



class gm:
	@staticmethod
	def show_profile(acc, usr):
		data = {}
		data['account_name'] = acc.username
		data['nickname'] = usr.name
		data['roleid'] = usr.roleid
		data['openid'] = acc.openid
		data['level'] = usr.level
		data['exp'] = usr.exp
		data['gold'] = usr.gold
		data['gem'] = usr.gem
		data['stamina'] = usr.stamina			
		
		return data
		