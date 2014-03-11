#coding:utf-8\
#!/usr/bin/env python

from game.models.almanac import almanac


def draw(request):
	"""
	领取奖励
	"""
	
	almawardid = request.GET['almawardid']	
	usr = request.user	
	alm = usr.getAlmanac()
	
	return alm.award(almawardid)