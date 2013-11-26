#coding:utf-8
#!/usr/bin/env python


from django.conf.urls import patterns, url
import game.views.main

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index')
    url(r'^index$', game.views.main.index),
    url(r'^info$', game.views.main.info),    
    url(r'^get_config$', game.views.main.get_config),
    url(r'^new_account$', game.views.main.new_account),
    url(r'^set_nickname$', game.views.main.set_nickname),
    url(r'^exit$', game.views.main.exit),
    url(r'^test$', game.views.main.test),
    url(r'^api/(\w+)/(\w+)/$', game.views.main.api)
)