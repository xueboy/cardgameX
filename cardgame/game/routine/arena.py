#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from cardgame.settings import ARENE_SERVER


class arena:
	@staticmethod
	def stand_ladder(usr):
		return json.loads(curl.url(ARENE_SERVER +  '/arena/stand_ladder/', None, {'roleid':str(usr.roleid)}))

	@staticmethod
	def show_all():
		return json.loads(curl.url(ARENE_SERVER +  '/arena/show_all/', None, {}))