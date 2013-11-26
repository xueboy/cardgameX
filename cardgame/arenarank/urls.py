#coding:utf-8
#!/usr/bin/env python


from django.conf.urls import patterns, url, include
import arenarank.views

urlpatterns = patterns('',
 url(r'^show_ladder/', 'arenarank.views.show_ladder'),
   
)