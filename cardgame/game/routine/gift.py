#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json

class gift:
	
	@staticmethod
	def sendGift(sendRoleid, receiveRoleid):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/network_gift/', None, {'send_roleid':sendRoleid, 'receive_roleid': receiveRoleid}))