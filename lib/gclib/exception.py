#coding:utf-8
#!/usr/bin/env python


class NotLogin(Exception):
	"""
	没有登陆
	"""
	pass
	
	
class NotHaveNickname(Exception):
	"""
	没有昵称
	"""
	pass
	
class NotImplemented(Exception):
	"""
	没有实现
	"""
	pass
	
class DuplicateNickname(Exception):
	"""
	重复名称
	"""
	pass