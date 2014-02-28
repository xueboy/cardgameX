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
 url(r'^add_protect_time/$', 'arenarank.views.add_protect_time'),
 url(r'^network_gift/$', 'arenarank.views.network_gift'),
 url(r'^network_range', 'arenarank.views.network_range'),
 url(r'^infection_encounter', 'arenarank.views.infection_encounter'),
 url(r'^infection_beat', 'arenarank.views.infection_beat'),
 url(r'^infection_call_relief', 'arenarank.views.infection_call_relief'),
 url(r'^infection_get_battle', 'arenarank.views.infection_get_battle'),
 url(r'^infection_award', 'arenarank.views.infection_award'), 
 url(r'^infection_ladder', 'arenarank.views.infection_ladder'),
)