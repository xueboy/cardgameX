#coding:utf-8
#!/usr/bin/env python

from gclib.curl import curl
from gclib.utility import randint
from cardgame.settings import ARENE_SERVER
from game.models.user import user

def show_ladder(request):	
	usr = request.user	
	return curl.url(ARENE_SERVER +  '/arena/show_ladder/', None, {'roleid':str(usr.roleid)})
		
def stand_ladder(request):
	usr = request.user
	return curl.url(ARENE_SERVER +  '/arena/stand_ladder/', None, {'roleid':str(usr.roleid)})
		
		
def challenge(request):
	usr = request.user
	defenceRoleid = request.GET['defence_roleid']
	defenceRole = user.get(defenceRoleid)
	
	usr.arena['challenge_roleid'] = defenceRole
	usr.save()
	
	return {'defence':defenceRole.getBattleData()}
		
def defeate(request):
	usr = request.user
	
	res = None
	if usr.arena.has_key('challenge_roleid'):
		res = curl.url(ARENE_SERVER +  '/arena/stand_ladder/', None, {'roleid':str(usr.roleid)})
		res = json.dumps(res)
		if not res.has_key('msg'):
			arenaLootConf = config.getConfig('arena_loot')
			arenaLootInfo = arenaLootConf[usr.level - 1]
			card = None			
			gold = 0
			skill = None
			rd = randint()
			rd = rd - gameConf['arena_loot_gold_probability']
			if rd <= 0:
				usr.gold = usr.gold + arenaLootInfo['glod']
			else:
				rd = rd - gameConf['arena_loot_pet_probability']
				if rd <= 0:
					inv = usr.getInventory()
					card =inv.addCard(arenaLootInfo['cardid'], arenaLootInfo['cardlevel'])
				else:
					inv = usr.getInventory()
					skl = inv.addSkill(arenaLootInfo['skillid'], arenaLootConf['skilllevel'])			
			
			data = {}
			if gold:
				data['gold'] = usr.gold
				usr.save()
			if card:
				data['add_card'] = card
				inv.save()
			if skl:
				data['add_skill'] = skl
				inv.save()
			return data
			
def convert(request):
	mediumCount = request.GET['medium_count']
	
	usr = request.user
	gameConf = config.getConfig('game')
	
	pointConsume = mediumCount * gameConf['arena_medium_price']
	
	res = curl.url(ARENE_SERVER +  '/arena/convert/', None, {'roleid':str(usr.roleid), 'score':pointConsume})
	res = json.dumps(res)
	
	if res.has_key('msg'):
		return res
		
	mediumId = gameConf['arena_dedium_id']
	inv = usr.getInventory()
	item = inf.addCountItem(mediumId, mediumCount)
	inv.save()
	if not item:
		return {'msg':'fail_add_item'}
	return {'add_item_array':item}
	