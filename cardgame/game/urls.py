#coding:utf-8
#!/usr/bin/env python


from django.conf.urls import patterns, url
import game.views.main

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index')
    url(r'index', game.views.main.index),
    url(r'info', game.views.main.info),
    url(r'config', game.views.main.config),
    url(r'api', game.views.main.api)
)