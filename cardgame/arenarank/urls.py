#coding:utf-8
#!/usr/bin/env python


from django.conf.urls import patterns, url, include
import arenarank.views

urlpatterns = patterns('',
 url(r'^show_ladder/', 'arenarank.views.show_ladder'),
 url(r'^stand_ladder/', 'arenarank.views.stand_ladder'),
 url(r'^show_all/', 'arenarank.views.show_all'),
   
)