﻿#coding:utf-8
#!/usr/bin/env python

from gclib.account import account as gcaccount
from game.models.user import user

class account(gcaccount):		
		
	@classmethod 
	def accountObject(self):
		return account()
		
	def userObject(self):
		return user()
		
	def __init__(self):
		gcaccount.__init__(self)
		
	
	