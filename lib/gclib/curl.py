#coding:utf-8
#!/usr/bin/env python


import pycurl
import StringIO
import urllib


		
def db(debug_type, debug_msg):
	myfile = open(r'd:/debug.log', 'a')             # open for output (creates)

	myfile.write( "debug(%d): %s" % (debug_type, debug_msg))        # write a line of text
	myfile.close()
	
class curl:
	
	def __init__(self):
		pass
	 		
	@staticmethod
	def url(url, postData = None, getData = None):		
		c = pycurl.Curl()		
		ret = StringIO.StringIO()		
		c.setopt(pycurl.WRITEFUNCTION, ret.write)
		c.setopt(pycurl.FOLLOWLOCATION, 1)
		#c.setopt(pycurl.VERBOSE, 1)
		#c.setopt(pycurl.DEBUGFUNCTION, db)
		if postData:
			c.setopt(pycurl.POST, 1)
			print urllib.urlencode(postData)
			c.setopt(pycurl.POSTFIELDS, urllib.urlencode(postData))
		if getData:
			url = url + '?' + urllib.urlencode(getData)
		c.setopt(pycurl.URL, url)
		c.perform()
		#c.close()
		return ret.getvalue()
