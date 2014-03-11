#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.json import json
from gclib.utility import randint
from cardgame.settings import ARENE_SERVER
from game.models.user import user
from game.routine.arena import arena
from game.utility.config import config


def show_ladder(request):
	"""
	显示竞技场天梯
	"""
	usr = request.user
	return arena.show(usr)

def stand_ladder(request):
	"""
	加入天梯
	"""
	usr = request.user
	return arena.stand_ladder(usr)

def show_all(request):
	"""
	显示所有排名
	"""
	return arena.show_all()

def challenge(request):
	"""
	挑战玩家
	"""
	usr = request.user
	defenceRoleid = request.GET['defence_roleid']
	return arena.challenge(usr, defenceRoleid)

def defeate(request):
	"""
	击败玩家
	"""
	usr = request.user
	return arena.defeate(usr)

def convert(request):
	"""
	兑换奖励
	"""
	mediumCount = request.GET['medium_count']
	mediumCount = int(mediumCount)
	usr = request.user

	return arena.convert(usr, mediumCount)

def score(request):
	"""
	积分
	"""
	usr = request.user	
	return arena.score(usr.roleid)

def rank_award(request):
	"""
	排名奖励
	"""
	usr = request.user
	rank = request.GET['rank_award']
	#rank = int(rank)
	return arena.rank_award(usr, rank)