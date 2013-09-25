from django.core.cache import cache, get_cache

class gccache:

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