#coding:utf-8
#!/usr/bin/env python


from django.conf.urls import patterns, url, include
import arenarank.views

urlpatterns = patterns('',
 url(r'^show_ladder/$', 'arenarank.views.show_ladder'),
 url(r'^stand_ladder/$', 'arenarank.views.stand_ladder'),
 url(r'^show_all/$', 'arenarank.views.show_all'),
 url(r'^remove/$', 'arenarank.views.remove'),
 url(r'^defeat/$', 'arenarank.views.defeat'),
 url(r'^convert/$', 'arenarank.views.convert'),
 url(r'^set_avatar_id/$', 'arenarank.views.set_avatar_id'),
 url(r'^score/$', 'arenarank.views.score'),
 url(r'^tower_stand/$', 'arenarank.views.tower_stand'),
 url(r'^tower_show/$','arenarank.views.tower_show'), 
 url(r'^grab_medal/$', 'arenarank.views.grab_medal'),
 #url(r'^lose_medal/$', 'arenarank.views.lose_medal'),
 url(r'^seek_holder/$', 'arenarank.views.seek_holder'),
 url(r'^medal_levelup/$', 'arenarank.views.medal_levelup'), 
 url(r'^new_medal/$', 'arenarank.views.new_medal'),
 url(r'^delete_medal/$', 'arenarank.views.delete_medal'),
 url(r'^award_score/$', 'arenarank.views.award_score'),
 url(r'^try_grab/$', 'arenarank.views.try_grab'),
 url(r'^add_protect_time/$', 'arenarank.views.add_protect_time')
)