#coding:utf-8
#!/usr/bin/env python

from gcjson import gcjson
from DBConnection import DBConnection
from gccache import gccache
import md5


class gcconfig:
	
	@staticmethod 
	def getConfigStr(confname):
		conn = DBConnection.getConnection()
		res = conn.query("SELECT * FROM config WHERE confname = %s", [confname])
		if len(res) > 0:
			return res[0][2]
		else:
			return None
	
	@staticmethod 
	def getConfig(confname):
		conf = gccache.loc_getValue('config:' + confname)
		if conf == None:
			conf = gcjson.loads(gcconfig.getConfigStr(confname))
			gccache.loc_setValue('config:' + confname, conf)
		#conf = gcjson.loads(gcconfig.getConfigStr(confname))
		return conf
				
	@staticmethod 
	def getMd5(confobj):		
		confpurestr = gcjson.dumps(confobj).encode("utf-8")
		m = md5.new()		
		m.update(confpurestr)
		return m.hexdigest().decode('utf-8')
			
	@staticmethod
	def createConfig(confname):
		conn = DBConnection.getConnection()
		conn.excute("INSERT INTO config (confname, conf) VALUES (%s, '')", [confname])
		gccache.loc_delete('config:' + confname)
		
	@staticmethod
	def setConfig(confname, confstr):
		confjson = gcjson.loads(confstr)		
		conn = DBConnection.getConnection();
		conn.excute("UPDATE config SET conf = %s WHERE confname = %s", [confstr, confname])
		gccache.loc_delete('config:' + confname)
		
	
	