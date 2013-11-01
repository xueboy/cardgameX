#coding:utf-8
#!/usr/bin/env python

from gclib.cache import cache
from gclib.json import json


class cacheable:
	
	def __init__(self):
		self.cacheid = 0
		self.cache_key = ''
	
	@classmethod
	def makeMKey(cls, cacheid):
		return ':'.join([cls.__module__, cls.__name__, 'objcache', str(cacheid)])
		
	def getMKey(self):
		return makeMKey(self.__class__, self.cacheid)
		
	@classmethod	
	def get(cls, cacheid):
		"""
		get object from cache if not exist return object without laod call.
		"""
		key = cls.makeMKey(cacheid)
		datastr = cache.mc_getValue(key);
		obj = cls()
		obj.cacheid = cacheid		
		obj.cache_key = key
		if datastr:
			data = json.loads(datastr)
			obj.load(cacheid, data)
		return obj
		
	def delete(self):
		if self.has_key('cache_key'):
			cache.mc_delete(self['cache_key'])
		
	def save(self):
		if not self.cache_key:
			self.cache_key = getMKey();
		data = self.getData()
		datastr = json.dumps(data)
		cache.mc_setValue(self.cache_key, datastr)
		
	def getData(self):
		return {}	
	
	def load(self, cacheid, data):
		self.cacheid = cacheid
		return 0