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

def luckycat_level(request):
	return generalConfigRequestProcess(request, 'luckycat_level')
	
def luckycat_bless(request):
	return generalConfigRequestProcess(request, 'luckycat_bless')

def luckycat_fortune(request):
	return generalConfigRequestProcess(request, 'luckycat_fortune')
	
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
	
def luckycat_level_import(request):
	return excel_import.luckycat_level_import(request)
	
def luckycat_bless_import(request):
	return excel_import.luckycat_bless_import(request)
	
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