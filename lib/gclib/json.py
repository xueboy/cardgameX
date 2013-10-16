#coding:utf-8
#!/usr/bin/env python

class json():
	
	@staticmethod  
	def loads(s, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
		idx = 0
		lsidx = 0
		strTemp = ''
		newS = ''
		while idx != -1:
			idx = s.find('\n', lsidx, len(s) - 1)
			if idx == -1:
				strTemp = s[lsidx:]
			else:
				strTemp = s[lsidx:(idx + 1)]
			if len(strTemp) > 0 and strTemp[0] != '#':
				newS += strTemp
			lsidx = idx + 1		
		return getattr(__import__("json"), 'loads')(newS, encoding=encoding, cls=cls, object_hook=object_hook,parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook,**kw)
	
	@staticmethod 
	def dumps(obj, skipkeys=False, ensure_ascii=False, check_circular=True, allow_nan=True, cls=None, indent=None, separators=(',', ':'), encoding='utf-8', default=None, sort_keys=False, **kw):
		return getattr(__import__("json"), 'dumps')(obj, skipkeys, ensure_ascii, check_circular, allow_nan, cls, indent, separators, encoding, default, sort_keys, **kw)
