#coding:utf-8
#!/usr/bin/env python

from django.shortcuts import render
from game.utility.config import config



class gm:
	@staticmethod
	def show_profile(acc, usr):
		data = {}
		openid = 0
		if acc:
			openid = acc.openid
		data['account_name'] = acc.username
		data['nickname'] = usr.name
		data['roleid'] = usr.roleid
		data['openid'] = openid
		data['level'] = usr.level
		data['exp'] = usr.exp
		data['gold'] = usr.gold
		data['gem'] = usr.gem
		data['stamina'] = usr.stamina
		data['trp'] = usr.trp
		
		inv = usr.getInventory()
		
		data['petConf'] = config.getConfig('pet')		
		data['petList'] = inv.card
		data['stoneConf'] = config.getConfig('stone')
		data['stoneList'] = inv.stone
		data['equipmentConf'] = config.getConfig('equipment')
		data['equipmentList'] = inv.equipment
		data['skillConf'] = config.getConfig('skill')
		data['skillList'] = inv.skill
		data['login_count'] = usr.signin['login_count']
		
		return data
		