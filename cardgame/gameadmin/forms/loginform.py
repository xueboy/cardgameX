#coding:utf-8
#!/usr/bin/env python


from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 20)
	password = forms.CharField(widget=forms.PasswordInput, max_length = 20)
	
	def __init__(self, form):
		forms.Form.__init__(self, form)