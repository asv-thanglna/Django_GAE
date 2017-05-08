from django import forms


class SignForm(forms.Form):
	guestbook_name = forms.CharField(label='', widget=forms.HiddenInput)
	content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'rows': 5}),
		max_length=1000)


class UpdateForm(forms.Form):
	guestbook_id = forms.IntegerField(label='', widget=forms.HiddenInput)
	guestbook_name = forms.CharField(label='', widget=forms.HiddenInput)
	content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'rows': 5}),
		max_length=1000)
