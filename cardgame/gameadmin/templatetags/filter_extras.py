#coding:utf-8
#!/usr/bin/env python

from django import template

register = template.Library()

@register.filter(name = 'dict_get')
def dict_get(v, k):
	return v[k]
	
@register.filter(name = 'array_get')
def array_get(v, i):
	return v[int(i)]
	
@register.filter(name='dict_lookup')	
def dict_lookup(v, k1, k2):
	return v[k1][k2]
	
@register.filter(name='range')
def filter_range(v):
	return range(v)
