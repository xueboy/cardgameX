#coding:utf-8
#!/usr/bin/env python

from django.conf.urls import patterns, url
import gameadmin.views.admin 
import gameadmin.views.main


urlpatterns = patterns('',
    #url(r'^$', views.index, name='index')
    url(r'login', gameadmin.views.admin.login),
    url(r'dungeon', gameadmin.views.main.dungeon),
    url(r'index', gameadmin.views.main.index),
    
)