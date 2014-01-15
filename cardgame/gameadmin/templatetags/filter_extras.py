#coding:utf-8
#!/usr/bin/env python

from django import template

register = template.Library()


@register.filter(name='dict_get')
def dict_get(v, k):
	return v[k]
	
	



