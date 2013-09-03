#coding:utf-8
#!/usr/bin/env python
from gclib.gcjson import gcjson
from gclib.object import object
from gclib.DBConnection import DBConnection
from gclib.gcuser import gcuser


class gcaccount(object):
	@classmethod
	def login(cls,usrname, password):
		conn = DBConnection.getConnection()
		res = conn.query("SELECT roleid, openid FROM account WHERE username = %s AND passward = %s", [usrname, password])
		if len(res) == 1:
			acc = cls.accountObject()
			acc.username = usrname
			acc.roleid = res[0][0]
			acc.opendid = res[0][1]
			return acc
		return None
			
	def getUser(self):
		
		if self.roleid == 0:
			return gcaccount.makeUser(self)
					
		conn = DBConnection.getConnection()		
		res = conn.query("SELECT * FROM user WHERE id = %d", [self.roleid])
		if len(res) == 1:
			usr = self.userObject()			
			usr.load(gcjson.loads(res[0][1]))
			usr.id = self.roleid
			return usr
		else:
			return gcaccount.makeUser(self) 
	
	@staticmethod 
	def makeUser(acc):
		conn = DBConnection.getConnection()		
		usr = acc.userObject()
		usr.init(acc)
		data = gcjson.dumps(usr.getdata())
		conn.excute("INSERT INTO user (object) VALUES (%s)", [data])
		return usr
		
	def userObject(self):
		"""
		Must overwrite in subclass and return the subclass of gcuser object
		"""
		return None
	
	@classmethod 
	def accountObject():
		"""
		Must implement in subclass and return the subclass of gcaccount object
		"""
		return None