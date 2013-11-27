#coding:utf-8
#!/usr/bin/env python

from django.conf.urls import patterns, url
import gameadmin.views.admin 
import gameadmin.views.main


urlpatterns = patterns('',
    #url(r'^$', views.index, name='index')    
    url(r'^login/$', gameadmin.views.admin.login),
    url(r'^tool/$', gameadmin.views.admin.tool),
    url(r'^dungeon/$', gameadmin.views.main.dungeon),
    url(r'^index/$', gameadmin.views.main.index),
    url(r'^level/$', gameadmin.views.main.level),
    url(r'^monster/$', gameadmin.views.main.monster),
    url(r'^monster_import/$', gameadmin.views.main.monster_import),
    url(r'^game/$', gameadmin.views.main.game),
    url(r'^skill/$', gameadmin.views.main.skill),
    url(r'^skill_import/$', gameadmin.views.main.skill_import),
    url(r'^skill_level/$', gameadmin.views.main.skill_level),
    url(r'^skill_level_import/$', gameadmin.views.main.skill_level_import),
    url(r'^level_import/$', gameadmin.views.main.level_import),
    url(r'^dungeon_import/$', gameadmin.views.main.dungeon_import),    
    url(r'^pet/$', gameadmin.views.main.pet),
    url(r'^pet_import/$', gameadmin.views.main.pet_import),
    url(r'^pet_level/$', gameadmin.views.main.pet_level),
    url(r'^pet_level_import/$', gameadmin.views.main.pet_level_import),
    url(r'^prompt/$', gameadmin.views.main.prompt),
    url(r'^garcha/$', gameadmin.views.main.garcha),
    url(r'^garcha_import/$', gameadmin.views.main.garcha_import),
    url(r'^equipment/$', gameadmin.views.main.equipment),
    url(r'^equipment_import/$', gameadmin.views.main.equipment_import),
    url(r'^strength_probability/$', gameadmin.views.main.strength_probability),
    url(r'^strength_price/$', gameadmin.views.main.strength_price),
    url(r'^strength_price_import/$', gameadmin.views.main.strength_price_import),
    url(r'^strength_price_import/$', gameadmin.views.main.strength_price_import),
    url(r'^luckycat_level/$', gameadmin.views.main.luckycat_level),
    url(r'^luckycat_level_import/$', gameadmin.views.main.luckycat_level_import),
    url(r'^luckycat_bless/$', gameadmin.views.main.luckycat_bless),
    url(r'^luckycat_bless_import/$', gameadmin.views.main.luckycat_bless_import),
    url(r'^luckycat_fortune/$', gameadmin.views.main.luckycat_fortune),
    url(r'^luck/$', gameadmin.views.main.luck),
    url(r'^luck_import/$', gameadmin.views.main.luck_import),
    url(r'^language/$', gameadmin.views.main.language),
    url(r'^language_import/$', gameadmin.views.main.language_import),
    url(r'^stone/$', gameadmin.views.main.stone),
    url(r'^stone_import/$', gameadmin.views.main.stone_import),
    url(r'^stone_probability/$', gameadmin.views.main.stone_probability),
    url(r'^stone_probability_import/$', gameadmin.views.main.stone_probability_import),
    url(r'^stone_level/$', gameadmin.views.main.stone_level),
    url(r'^stone_level_import/$', gameadmin.views.main.stone_level_import),
    url(r'^trp/$', gameadmin.views.main.trp),
    url(r'^trp_import/$', gameadmin.views.main.trp_import),
    url(r'^trp_price/$', gameadmin.views.main.trp_price),
    url(r'^trp_price_import/$', gameadmin.views.main.trp_price_import),
    url(r'^educate/$', gameadmin.views.main.educate),
    url(r'^educate_import/$', gameadmin.views.main.educate_import),
    url(r'^educate_grade/$', gameadmin.views.main.educate_grade),
    url(r'^educate_grade_import/$', gameadmin.views.main.educate_grade_import),
    url(r'^almanac_combination/$', gameadmin.views.main.almanac_combination),
    url(r'^almanac_combination_import/$', gameadmin.views.main.almanac_combination_import),
    
    
    
)