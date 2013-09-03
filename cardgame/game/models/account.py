#coding:utf-8
#!/usr/bin/env python

from gclib.gcaccount import gcaccount
from game.models.user import user

class account(gcaccount):		
		
	@classmethod 
	def accountObject(self):
		return account()
		
	def userObject(self):
		return user()
	