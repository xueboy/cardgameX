﻿#coding:utf-8
#!/usr/bin/env python

from gclib.object import object
from gclib.DBConnection import DBConnection

class gcuser(object):	
	def init(self, acc):
		self.id = 0
		return
		
	def update1(self):
		return
		
	def saveRoleId(self):
		conn = DBConnection.getConnection()		
		self.roleid = self.id
		conn.excute("UPDATE user SET roleid = %s WHERE id = %s", [self.roleid, self.id])		
		return None