# -*- coding: utf-8 -*-

from django import forms


class GreetingDetailForm(forms.Form):

	guestbook_id = forms.IntegerField()
	guestbook_name = forms.CharField()
	content = forms.CharField(max_length=1000)