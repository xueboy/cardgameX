#coding:utf-8
#!/usr/bin/env python


from django.conf.urls import patterns, url
import game.views.main

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index')
    url(r'^index$', game.views.main.index),
    url(r'^info$', game.views.main.info),
    url(r'^config$', game.views.main.config),
    url(r'^get_config$', game.views.main.get_config),
    url(r'^account_new$', game.views.main.account_new),
    url(r'^test$', game.views.main.test),
    url(r'^api/(\w+)/(\w+)/$', game.views.main.api)
)