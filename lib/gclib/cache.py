from django.core.cache import cache, get_cache

class cache:

	@staticmethod
	def loc_setValue(key, val):
		"""
		set local memery cache.
		"""
		c = get_cache('in_memery')
		c.set(key, val)
	
	@staticmethod	
	def loc_getValue(key):
		"""
		get local memery cache.
		"""
		c = get_cache('in_memery')
		return c.get(key)

	@staticmethod	
	def loc_delete(key):
		"""
		delete local memery cache.
		"""
		c = get_cache('in_memery')
		c.delete(key)
		
	@staticmethod
	def mc_setValue(key, val):
		"""
		set defalut memcached.
		"""
		c = get_cache('default')
		c.set(key, val)
		
	@staticmethod
	def mc_getValue(key):
		"""
		get defalut memcached.
		"""
		c = get_cache('default')
		return c.get(key)
		
	@staticmethod
	def mc_delete(key, val):
		"""
		delete defalut memcached.
		"""		
		c = get_cache('default')
		c.delete(key, val)
		
	@staticmethod
	def mc_hasKey(key):
		"""
		check if key exist in defalut memcached
		"""		
		c = get_cache('default')
		return c.has_key(key)