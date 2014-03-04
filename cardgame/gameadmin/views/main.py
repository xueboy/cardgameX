#coding:utf-8
#!/usr/bin/env python

from django.shortcuts import render
from gclib.DBConnection import DBConnection
from django.http import HttpResponse
from gclib.json import json
from gclib.config import config
from excel_import import excel_import

def index(request):
	return render(request, 'index.html', {})

def dungeon(request):
	return generalConfigRequestProcess(request, 'dungeon')		
				
def level(request):
	return generalConfigRequestProcess(request, 'level')				
				
def monster(request):
	return generalConfigRequestProcess(request, 'monster')			
				
def game(request):
	return generalConfigRequestProcess(request, 'game')

def skill(request):
	return generalConfigRequestProcess(request, 'skill')

def skill_effect(request):
	return generalConfigRequestProcess(request, 'skill_effect')
	
def skill_level(request):
	return generalConfigRequestProcess(request, 'skill_level')
	
def pet(request):
	return generalConfigRequestProcess(request, 'pet')
	
def pet_level(request):
	return generalConfigRequestProcess(request, 'pet_level')
	
def prompt(request):
	return generalConfigRequestProcess(request, 'prompt')

def garcha(request):
	return generalConfigRequestProcess(request, 'garcha')	
	
def equipment(request):
	return generalConfigRequestProcess(request, 'equipment')

def strength_probability(request):
	return generalConfigRequestProcess(request, 'strength_probability')

def strength_price(request):
	return generalConfigRequestProcess(request, 'strength_price')

def luckycat_bless(request):
	return generalConfigRequestProcess(request, 'luckycat_bless')

def luckycat_fortune(request):
	return generalConfigRequestProcess(request, 'luckycat_fortune')
	
def luckycat_profit(request):
	return generalConfigRequestProcess(request, 'luckycat_profit')
	
def luck(request):
	return generalConfigRequestProcess(request, 'luck')
	
def language(request):
	return generalConfigRequestProcess(request, 'language')
	
def stone(request):
	return generalConfigRequestProcess(request, 'stone')
	
def stone_probability(request):
	return generalConfigRequestProcess(request, 'stone_probability')
	
def stone_level(request):
	return generalConfigRequestProcess(request, 'stone_level')
	
def trp_price(request):
	return generalConfigRequestProcess(request, 'trp_price')

def trp_probability(request):
	return generalConfigRequestProcess(request, 'trp_probability')

def trp(request):
	return generalConfigRequestProcess(request, 'trp')
	
def educate(request):
	return generalConfigRequestProcess(request, 'educate')
	
def educate_grade(request):
	return generalConfigRequestProcess(request, 'educate_grade')
	
def almanac_combination(request):
	return generalConfigRequestProcess(request, 'almanac_combination')
	
def reborn(request):
	return generalConfigRequestProcess(request, 'reborn')
	
def ladder_score(request):
	return generalConfigRequestProcess(request, 'ladder_score')
	
def arena_loot(request):
	return generalConfigRequestProcess(request, 'arena_loot')
	
def name(request):
	return generalConfigRequestProcess(request, 'name')
	
def drop(request):
	return generalConfigRequestProcess(request, 'drop')
	
def dialog(request):
	return generalConfigRequestProcess(request, 'dialog')
	
def drama(request):
	return generalConfigRequestProcess(request, 'drama')
	
def quest(request):
	return generalConfigRequestProcess(request, 'quest')
	
def item(request):
	return generalConfigRequestProcess(request, 'item')
	
def signin(request):
	return generalConfigRequestProcess(request, 'signin')
	
def levelup(request):
	return generalConfigRequestProcess(request, 'levelup')
	
def open_award(request):
	return generalConfigRequestProcess(request, 'open_award')
	
def tower_monster(request):
	return generalConfigRequestProcess(request, 'tower_monster')
	
def tower_markup(request):
	return generalConfigRequestProcess(request, 'tower_markup')

def tower_award(request):
	return generalConfigRequestProcess(request, 'tower_award')
	
def medal(request):
	return generalConfigRequestProcess(request, 'medal')
	
def medal_loot(request):
	return generalConfigRequestProcess(request, 'medal_loot')
	
def medal_level(request):
	return generalConfigRequestProcess(request, 'medal_level')

def mall_price(request):
	return generalConfigRequestProcess(request, 'mall_price')
	
def practice_property(request):
	return generalConfigRequestProcess(request, 'practice_property')
	
def practice_level(request):
	return generalConfigRequestProcess(request, 'practice_level')
	
def slotmachine(request):
	return generalConfigRequestProcess(request, 'slotmachine')
	
def vip(request):
	return generalConfigRequestProcess(request, 'vip')
	
def potential(request):
	return generalConfigRequestProcess(request, 'potential')
	
def potential_price(request):
	return generalConfigRequestProcess(request, 'potential_price')
	
def email(request):
	return generalConfigRequestProcess(request, 'email')
	
def gift(request):
	return generalConfigRequestProcess(request, 'gift')
	
def invite(request):
	return generalConfigRequestProcess(request, 'invite')
	
def infection_battle(request):
	return generalConfigRequestProcess(request, 'infection_battle')

def infection_prestige_price(request):
	return generalConfigRequestProcess(request, 'infection_prestige_price')
	
def infection_damage_award(request):
	return generalConfigRequestProcess(request, 'infection_damage_award')

def infection_prestige_award(request):
	return generalConfigRequestProcess(request, 'infection_prestige_award')
	
def infection_exploit_price(request):
	return generalConfigRequestProcess(request, 'infection_exploit_price')
	
def explore_award(request):
	return generalConfigRequestProcess(request, 'explore_award')
	
def generalConfigRequestProcess(request, confname):
	if request.method == 'POST':
		confstr = request.POST['config']
		try:
			config.setConfig(confname, confstr)		
			return render(request, 'index.html', {})
		except:
			return render(request, confname + '.html', {'config':confstr})
	else:
		confstr = config.getConfigStr(confname)		
		if confstr != None:			
			return render(request, confname + '.html', {'config': confstr})
		else:
			config.createConfig(confname)			
			return render(request, confname + '.html', {'config':''})

def monster_import(request):
	return excel_import.monster_import(request)	
	
def level_import(request):
	return excel_import.level_import(request)
	
def dungeon_import(request):
	return excel_import.dungeon_import(request)

def skill_import(request):
	return excel_import.skill_import(request)
	
def skill_effect_import(request):
	return excel_import.skill_effect_import(request)
	
def skill_level_import(request):
	return excel_import.skill_level_import(request)
	
def pet_import(request):
	return excel_import.pet_import(request)
	
def pet_level_import(request):
	return excel_import.pet_level_import(request)
	
def garcha_import(request):
	return excel_import.garcha_import(request)
	
def equipment_import(request):
	return excel_import.equipment_import(request)
	
def strength_price_import(request):
	return excel_import.strength_price_import(request)
	
def luckycat_bless_import(request):
	return excel_import.luckycat_bless_import(request)
	
def luckycat_profit_import(request):
	return excel_import.luckycat_profit_import(request)
	
def luck_import(request):
	return excel_import.luck_import(request)
	
def language_import(request):
	return excel_import.language_import(request)
	
def stone_import(request):
	return excel_import.stone_import(request)
	
def stone_probability_import(request):
	return excel_import.stone_probability_import(request)
	
def stone_level_import(request):
	return excel_import.stone_level_import(request)
	
def trp_import(request):
	return excel_import.trp_import(request)
	
def trp_price_import(request):
	return excel_import.trp_price_import(request)
	
def trp_probability_import(request):
	return excel_import.trp_probability_import(request)
	
def educate_import(request):
	return excel_import.educate_import(request)
	
def educate_grade_import(request):
	return excel_import.educate_grade_import(request)
	
def almanac_combination_import(request):
	return excel_import.almanac_combination_import(request)

def reborn_import(request):
	return excel_import.reborn_import(request)
	
def ladder_score_import(request):
	return excel_import.ladder_score_import(request)
	
def name_import(request):
	return excel_import.name_import(request)
	
def arena_loot_import(request):
	return excel_import.arena_loot_import(request)
	
def drop_import(request):
	return excel_import.drop_import(request)
	
def dialog_import(request):
	return excel_import.dialog_import(request)
	
def drama_import(request):
	return excel_import.drama_import(request)
	
def quest_import(request):
	return excel_import.quest_import(request)
	
def item_import(request):
	return excel_import.item_import(request)

def tower_monster_import(request):
	return excel_import.tower_monster_import(request)
	
def tower_markup_import(request):
	return excel_import.tower_markup_import(request)
	
def tower_award_import(request):
	return excel_import.tower_award_import(request)
	
def medal_import(request):
	return excel_import.medal_import(request)
	
def medal_loot_import(request):
	return excel_import.medal_loot_import(request)
	
def medal_level_import(request):
	return excel_import.medal_level_import(request)
	
def mall_price_import(request):
	return excel_import.mall_price_import(request)
	
def practice_level_import(request):
	return excel_import.practice_level_import(request)
	
def practice_property_import(request):
	return excel_import.practice_property_import(request)
	
def slotmachine_import(request):
	return excel_import.slotmachine_import(request)
	
def vip_import(request):
	return excel_import.vip_import(request)
	
def potential_price_import(request):
	return excel_import.potential_price_import(request)
	
def email_import(request):
	return excel_import.email_import(request)
	
def gift_import(request):
	return excel_import.gift_import(request)
	
def infection_battle_import(request):
	return excel_import.infection_battle_import(request)
	
def infection_prestige_price_import(request):
	return excel_import.infection_prestige_price_import(request)
	
def infection_damage_award_import(request):
	return excel_import.infection_damage_award_import(request)
	
def infection_prestige_award_import(request):
	return excel_import.infection_prestige_award_import(request)
	
def infection_exploit_price_import(request):
	return excel_import.infection_exploit_price_import(request)
	
def explore_award_import(request):
	return excel_import.explore_award_import(request)