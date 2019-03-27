# -*- coding: utf-8 -*-

from django import forms


class GreetingDetailForm(forms.Form):

	greeting_id = forms.IntegerField()
	guestbook_name = forms.CharField()
	greeting_name = forms.CharField(max_length=100)
	content = forms.CharField(max_length=1000, required=False)
