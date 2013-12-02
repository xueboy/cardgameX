#coding:utf-8
#!/usr/bin/env python

from gclib.json import json
from DBConnection import DBConnection
from gclib.cache import cache
import hashlib


class config:
	
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
		conf = cache.loc_getValue('config:' + confname)
		if not conf:
			conf = json.loads(config.getConfigStr(confname))
			cache.loc_setValue('config:' + confname, conf)
			conf = cache.loc_getValue('config:' + confname)
		#conf = json.loads(config.getConfigStr(confname))
		return conf
				
	@staticmethod 
	def getMd5(confobj):		
		confpurestr = json.dumps(confobj).encode("utf-8")
		m = hashlib.md5()		
		m.update(confpurestr)
		return m.hexdigest().decode('utf-8')
			
	@staticmethod
	def createConfig(confname):
		conn = DBConnection.getConnection()
		conn.excute("INSERT INTO config (confname, conf) VALUES (%s, '')", [confname])
		cache.loc_delete('config:' + confname)
		
	@staticmethod
	def setConfig(confname, confstr):
		confjson = json.loads(confstr)
		conn = DBConnection.getConnection();
		conn.excute("UPDATE config SET conf = %s WHERE confname = %s", [confstr, confname])
		cache.loc_delete('config:' + confname)
		
	
	