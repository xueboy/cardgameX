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
	usr = request.user
	return arena.show(usr)

def stand_ladder(request):
	usr = request.user
	return arena.stand_ladder(usr)

def show_all(request):
	return arena.show_all()

def challenge(request):
	usr = request.user
	defenceRoleid = request.GET['defence_roleid']
	return arena.challenge(usr, defenceRoleid)

def defeate(request):
	usr = request.user
	return arena.defeate(usr)

def convert(request):
	mediumCount = request.GET['medium_count']
	mediumCount = int(mediumCount)
	usr = request.user

	return arena.convert(usr, mediumCount)

def score(request):
	usr = request.user	
	return arena.score(usr.roleid)

def rank_award(request):
	usr = request.user
	rank = request.GET['rank_award']
	#rank = int(rank)
	return arena.rank_award(usr, rank)