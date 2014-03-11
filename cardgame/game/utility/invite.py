#coding:utf-8
#!/usr/bin/env python

class invite:
	
	base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+26)] + [ chr(x) for x in range(ord('a'),ord('a')+26)]
	
	@staticmethod
	def generateCode(accountid):
		"""
		生成邀请码
		"""
		code_base = 916132832 - accountid    
		text_code = invite.dec2ary62(code_base)
		final_code = []
		for i in range(len(text_code)):
			c = ord(text_code[i])
			c = c - i - 1
			if c < ord('a') and c > ord('Z'):
				c = c - 6
			elif c < ord('A') and c > ord('9'):
				c = c - 7
			elif c < ord('0'):
				c = ord('z') + 1 - (ord('0') - c)
			final_code.append(chr(c))			
		return ''.join(final_code)
    
	@staticmethod
	def reverseCode(inviteCode): 
		"""
		解释邀请码
		"""
		orgineCode = []
		for i in range(len(inviteCode)):
			c = ord(inviteCode[i])
			c = c + (i + 1)
			if c < ord('a') and c > ord('Z'):
				c = c + 6
			elif c < ord('A') and c > ord('9'):
				c = c + 7
			elif c > ord('z'):
				c = (ord('0') - 1) +  (c - ord('z'))
			orgineCode.append(chr(c))     
		accountid = 916132832 - invite.ary622dec(orgineCode)
		return accountid
    
	@staticmethod
	def dec2ary62(string_num):
		"""
		编码
		"""
		num = int(string_num)
		mid = []
		while True:
			if num == 0:
				break
			num, rem = divmod(num, 62)
			mid.append(invite.base[rem])
		return ''.join([str(x) for x in mid[::-1]])

	@staticmethod
	def ary622dec(string_num):
		"""
		解码
		"""		
		val = 0
		for i in range(len(string_num)):
			num = invite.base.index(string_num[i])
			val = num * pow(62, len(string_num) - i - 1) + val
		return val
