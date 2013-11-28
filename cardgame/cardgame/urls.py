#coding:utf-8
#!/usr/bin/env python

from django.conf.urls import patterns, include, url
import game.urls
import gameadmin.urls
import arenarank.urls

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cardgame.views.home', name='home'),
    # url(r'^cardgame/', include('cardgame.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^arena/', include('arenarank.urls')),
    url(r'^game/', include('game.urls')),
    url(r'^admin/', include('gameadmin.urls')),
    
)
