﻿#coding:utf-8
#!/usr/bin/env python

from gclib.json import json
from game.routine.pet import pet
from game.models.inventory import inventory
from game.routine.garcha import garcha as garchaR
from game.routine.potential import potential
def set_team(request):
	"""
	设置队伍
	"""
	usr = request.user
	inv = usr.getInventory()
	cardid1 = request.GET['card_id1']
	cardid2 = request.GET['card_id2']
	cardid3 = request.GET['card_id3']
	cardid4 = request.GET['card_id4']
	cardid5 = request.GET['card_id5']
	cardid6 = request.GET['card_id6']
	
	deq = []
	dst = []
	dsk = []
	
	msg = inv.setTeam(cardid1, cardid2, cardid3, cardid4, cardid5, cardid6, deq, dst, dsk)
	if msg:
		return msg
	data = {}
	data['team'] = inv.team
#	data['slot'] = inv.getSlots()
#	data['st_slot'] = inv.getStSlots()
#	data['sk_slot'] = inv.getSkSlots()
#	if deq:
#		data['add_equipment_array'] = deq
#	if dst:
#		data['add_stone_array'] = dst
#	if dsk:
#		data['add_skill_array'] = dsk
	return data

	
def level_up(request):
	"""
	升级
	"""
	usr = request.user
	
	sourceCard1 = ''
	sourceCard2 = ''
	sourceCard3 = ''
	sourceCard4 = ''
	sourceCard5 = ''
	sourceCard6 = ''	
	
	destCard = request.GET['dest_card']
	sourceCard1 = request.GET['source_card1']
	if request.GET.has_key('source_card2'):
		sourceCard2 = request.GET['source_card2']	
	if request.GET.has_key('source_card3'):
		sourceCard3 = request.GET['source_card3']	
	if request.GET.has_key('source_card4'):
		sourceCard4 = request.GET['source_card4']		
	if request.GET.has_key('source_card5'):
		sourceCard5 = request.GET['source_card5']	
	if request.GET.has_key('source_card6'):
		sourceCard6 = request.GET['source_card6']	
	
	sourceCardId = []
	if sourceCard1 != '':
		sourceCardId.append(sourceCard1)
	if sourceCard2 != '':
		sourceCardId.append(sourceCard2)
	if sourceCard3 != '':
		sourceCardId.append(sourceCard3)
	if sourceCard4 != '':
		sourceCardId.append(sourceCard4)
	if sourceCard5 != '':
		sourceCardId.append(sourceCard5)
	if sourceCard6 != '':
		sourceCardId.append(sourceCard6)		
		
	return pet.levelup(usr, destCard, sourceCardId)
	
		
def garcha(request):
	"""
	求将
	"""
	usr = request.user
	
	garchaAmount = request.GET['amount']
	if garchaAmount == '1':
		garchaAmount = 10
	elif garchaAmount == '2':
		garchaAmount = 100
	elif garchaAmount == '3':
		garchaAmount = 10000
	else:
		return {'msg':'parameter_bad'}
	res = garchaR.garcha_once(usr, garchaAmount)	
	return res
	
def training(request):
	"""
	培养
	"""
 	usr = request.user
 	
 	id = request.GET['id']
 	traininglevel = int(request.GET['training_level'])
 	
 	return pet.training(usr, id, traininglevel) 	
 	
def sell(request):
	"""
	卖出
	"""
	usr = request.user
	id = request.GET['id']
	return pet.sell(usr, id)
	
def training_confirm(request):
	"""
	培养确认
	"""
	usr = request.user	
	return pet.trainConfirm(usr)
	
def decompose(request):
	"""
	分解
	"""
	usr = request.user
	cardids = []
	
	cardids.append(request.GET['card_id1'])
	if request.GET.has_key('card_id2'):
		cardids.append(request.GET['card_id2'])
	if request.GET.has_key('card_id3'):
		cardids.append(request.GET['card_id3'])
	if request.GET.has_key('card_id4'):
		cardids.append(request.GET['card_id4'])
	if request.GET.has_key('card_id5'):
		cardids.append(request.GET['card_id5'])
	if request.GET.has_key('card_id6'):
		cardids.append(request.GET['card_id6'])
	if request.GET.has_key('card_id7'):
		cardids.append(request.GET['card_id7'])
	if request.GET.has_key('card_id8'):
		cardids.append(request.GET['card_id8'])
	if request.GET.has_key('card_id9'):
		cardids.append(request.GET['card_id9'])
	if request.GET.has_key('card_id10'):
		cardids.append(request.GET['card_id10'])
	return pet.decompose(usr, cardids)

def reborn(request):
	"""
	转生
	"""
	usr = request.user
	cardid = request.GET['card']	
	return pet.reborn(usr, cardid)
	
def assembly(request):	
	"""
	组装碎片
	"""
	usr = request.user	
	card_id = request.GET['cardid']	
	return pet.assembly(usr, card_id)
	
def fire_potential(request):
	"""
	替能激发
	"""
	usr = request.user
	id = request.GET['card']
	useGem = (request.GET['is_use_gem'] == 'yes')
	return potential.fire(usr, id, useGem)