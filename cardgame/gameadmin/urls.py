#coding:utf-8
#!/usr/bin/env python

from django.conf.urls import patterns, url
import gameadmin.views.admin 
import gameadmin.views.main
import gameadmin.views.tool


urlpatterns = patterns('',
    #url(r'^$', views.index, name='index')    
    url(r'^login/$', gameadmin.views.admin.login),
    url(r'^arena_tool/$', gameadmin.views.admin.arena_tool),
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
    url(r'^skill_effect/$', gameadmin.views.main.skill_effect),
    url(r'^skill_effect_import/$', gameadmin.views.main.skill_effect_import),
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
    url(r'^trp_probability/$', gameadmin.views.main.trp_probability),
    url(r'^trp_probability_import/$', gameadmin.views.main.trp_probability_import),
    url(r'^educate/$', gameadmin.views.main.educate),
    url(r'^educate_import/$', gameadmin.views.main.educate_import),
    url(r'^educate_grade/$', gameadmin.views.main.educate_grade),
    url(r'^educate_grade_import/$', gameadmin.views.main.educate_grade_import),
    url(r'^almanac_combination/$', gameadmin.views.main.almanac_combination),
    url(r'^almanac_combination_import/$', gameadmin.views.main.almanac_combination_import),
    url(r'^reborn/$', gameadmin.views.main.reborn),
    url(r'^reborn_import/$', gameadmin.views.main.reborn_import),
    url(r'^ladder_score/$', gameadmin.views.main.ladder_score),
    url(r'^ladder_score_import/$', gameadmin.views.main.ladder_score_import),
    url(r'^arena_loot/$', gameadmin.views.main.arena_loot),
    url(r'^arena_loot_import/$', gameadmin.views.main.arena_loot_import),    
    url(r'^drop/$', gameadmin.views.main.drop),
    url(r'^drop_import/$', gameadmin.views.main.drop_import),
    url(r'^name/$', gameadmin.views.main.name),
    url(r'^name_import/$', gameadmin.views.main.name_import),
    url(r'^dialog/$', gameadmin.views.main.dialog),
    url(r'^dialog_import/$', gameadmin.views.main.dialog_import),
    url(r'^drama/$', gameadmin.views.main.drama),
    url(r'^drama_import/$', gameadmin.views.main.drama_import),
    url(r'^quest/$', gameadmin.views.main.quest),
    url(r'^quest_import/$', gameadmin.views.main.quest_import),
    url(r'^item/$', gameadmin.views.main.item),
    url(r'^item_import/$', gameadmin.views.main.item_import),
    url(r'^tool_create_player/$', gameadmin.views.tool.tool_create_player),
    url(r'^tool_ladder_remove/$', gameadmin.views.tool.tool_ladder_remove),
    url(r'^gm_tool/$', gameadmin.views.tool.gm_tool),
    url(r'^gm_tool_profile_find/$', gameadmin.views.tool.gm_tool_profile_find),
    url(r'^gm_tool_set_profile/$', gameadmin.views.tool.gm_tool_set_profile),
    url(r'^gm_tool_set_card/$', gameadmin.views.tool.gm_tool_set_pet),
    url(r'^gm_tool_set_stone/$', gameadmin.views.tool.gm_tool_set_stone),
    url(r'^gm_tool_set_equipment/$', gameadmin.views.tool.gm_tool_set_equipment),
    url(r'^gm_tool_set_skill/$', gameadmin.views.tool.gm_tool_set_skill),
    url(r'^gm_tool_set_item/$', gameadmin.views.tool.gm_tool_set_item),
    url(r'^signin/$', gameadmin.views.main.signin),
    url(r'^levelup/$', gameadmin.views.main.levelup),
    url(r'^open_award/$', gameadmin.views.main.open_award),
    url(r'^tower_monster/$', gameadmin.views.main.tower_monster),
    url(r'^tower_monster_import/$', gameadmin.views.main.tower_monster_import),
    url(r'^tower_markup/$', gameadmin.views.main.tower_markup),
    url(r'^tower_markup_import/$', gameadmin.views.main.tower_markup_import),
    url(r'^tower_award/$', gameadmin.views.main.tower_award),
    url(r'^tower_award_import/$', gameadmin.views.main.tower_award_import),
    
    
    
)