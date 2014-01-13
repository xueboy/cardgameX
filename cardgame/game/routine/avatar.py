#coding:utf-8
#!/usr/bin/env python

from cardgame.settings import STATIC_ROOT
import hashlib

class avatar:
	
	@staticmethod
	def getAvatarId(roleid):		
		file_title = "".join([unicode(roleid), ".avt"])
		file_name = "/".join([STATIC_ROOT, "avatar", file_title])	
		try:
			f = open(file_name, 'rb')
			avatar = f.read()
			f.close()	
			m = hashlib.md5(avatar)		
			return m.hexdigest()
		except:
			return ''
	
	@staticmethod		
	def setAvatar(roleid, body):				
		m = hashlib.md5(body)
		avatar_id = m.hexdigest()
	
		file_title = "".join([str(roleid), ".avt"])
		file_name = "/".join([STATIC_ROOT, "avatar", file_title])
		try:
			f = open(file_name, "wb")
			f.write(body)
			f.close()
		except:
			return ''		
		return avatar_id
	
	@staticmethod
	def getAvatar(roleid):
		
		file_title = "".join([roleid, ".avt"])
		file_name = "/".join([STATIC_ROOT, "avatar", file_title])
	
		try:
			f = open(file_name, 'rb')
			body = f.read()
			f.close()
		except:
			return None
		return body
