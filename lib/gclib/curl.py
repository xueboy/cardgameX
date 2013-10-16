#coding:utf-8
#!/usr/bin/env python


import pycurl
import StringIO

class curl:
	
	def __init__(self):
		pass
		
		
	@staticmethod
	def url(url):
		curl = pycurl.Curl()
		curl.setopt(pycurl.URL, url)
		ret = StringIO.StringIO()		
		curl.setopt(pycurl.WRITEFUNCTION, ret.write)		
		curl.perform()
		return ret.getvalue()
