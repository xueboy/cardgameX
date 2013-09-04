#coding:utf-8
#!/usr/bin/env python

from gcjson import gcjson
from DBConnection import DBConnection
import md5


class config:
	
	@staticmethod 
	def getConfigStr(confname):
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM config WHERE confname = %s", [confname])
		if len(res) > 0:
			return res[0][2]
		else:
			return ''	
	
	@staticmethod 
	def getConfig(confname):
		return gcjson.loads(config.getConfigStr(confname))			
				
	@staticmethod 
	def getMd5(confname):		
		confobj = config.getConfig(confname)
		confpurestr = gcjson.dumps(confobj)	
		m = md5.new()		
		m.update(confpurestr)		
		return m.hexdigest().decode('utf-8')
			
	@staticmethod
	def createConfig(confname):
		conn = DBConnection.getConnection()
		conn.excute("INSERT INTO config (confname, conf) VALUES (%s, '')", [confname])
		
	@staticmethod
	def setConfig(confname, confstr):
		confjson = gcjson.loads(confstr)		
		conn = DBConnection.getConnection();
		conn.excute("UPDATE config SET conf = %s WHERE confname = %s", [confstr, confname])
		
	
	