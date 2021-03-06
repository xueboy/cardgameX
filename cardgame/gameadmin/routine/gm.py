﻿#coding:utf-8
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
		data['petChip'] = inv.card_chip
		data['stoneConf'] = config.getConfig('stone')
		data['stoneList'] = inv.stone
		data['equipmentConf'] = config.getConfig('equipment')
		data['equipmentList'] = inv.equipment
		data['equipmentChip'] = inv.equipment_chip
		data['skillConf'] = config.getConfig('skill')
		data['skillList'] = inv.skill
		data['skillChip'] = inv.skill_chip
		data['itemConf'] = config.getConfig('item')
		data['itemList'] = inv.item
		data['login_count'] = usr.signin['login_count']
		data['medalConf'] = config.getConfig('medal')
		data['medalDict'] = inv.medal
		data['emailConf'] = config.getConfig('email')
		
		
		return data
		