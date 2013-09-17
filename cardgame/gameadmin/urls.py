#coding:utf-8
#!/usr/bin/env python

from django.conf.urls import patterns, url
import gameadmin.views.admin 
import gameadmin.views.main


urlpatterns = patterns('',
    #url(r'^$', views.index, name='index')    
    url(r'^login/$', gameadmin.views.admin.login),
    url(r'^dungeon/$', gameadmin.views.main.dungeon),
    url(r'^index/$', gameadmin.views.main.index),
    url(r'^level/$', gameadmin.views.main.level),
    url(r'^monster/$', gameadmin.views.main.monster),
    url(r'^card/$', gameadmin.views.main.card),
    url(r'^game/$', gameadmin.views.main.game),
    url(r'^skill/$', gameadmin.views.main.skill),
    url(r'^level_import/$', gameadmin.views.main.level_import),
    url(r'^dungeon_import/$', gameadmin.views.main.dungeon_import),
    url(r'^skill_import/$', gameadmin.views.main.skill_import),
    url(r'^pet/$', gameadmin.views.main.pet),
    url(r'^pet_import/$', gameadmin.views.main.pet_import),
    url(r'^pet_level/$', gameadmin.views.main.pet_level),
    url(r'^pet_level_import/$', gameadmin.views.main.pet_level_import),
    url(r'^prompt/$', gameadmin.views.main.prompt),
    
    
)