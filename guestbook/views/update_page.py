# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from google.appengine.api import users
from google.appengine.ext import ndb
from guestbook.models import Greeting
from guestbook.forms import UpdateForm
import logging


class UpdateView(FormView):
	template_name = 'guestbook/update_page.html'
	form_class = UpdateForm

	def get_initial(self):
		initial = super(UpdateView, self).get_initial()
		guestbook_name = self._get_guestbook_name()
		guestbook_id = self._get_guestbook_id()
		greeting = Greeting.get_greeting(guestbook_id, guestbook_name)
		initial['guestbook_id'] = guestbook_id
		initial['guestbook_name'] = guestbook_name
		initial['content'] = greeting.content
		return initial

	def _get_guestbook_id(self):
		guestbook_id = self.request.GET.get('guestbook_id', '')
		return int(guestbook_id)

	def _get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name')
		return guestbook_name

	def get_context_data(self, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = super(UpdateView, self).get_context_data(**kwargs)
		context['update_form'] = form
		context['guestbook_id'] = self._get_guestbook_id()
		context['guestbook_name'] = self._get_guestbook_name()
		return context

	def get_success_url(self):
		success_url = reverse_lazy('index')
		return '%s?guestbook_name=%s' % (success_url, self._get_guestbook_name())

	def form_valid(self, form, **kwargs):
		self.update_greeting(form)
		return super(UpdateView, self).form_valid(form, **kwargs)

	def update_greeting(self, form):
		user = users.get_current_user()
		greeting = Greeting.get_greeting(form.cleaned_data['guestbook_id'],
			form.cleaned_data['guestbook_name'])

		@ndb.transactional
		def txn():
			greeting.updated_by = user
			greeting.content = form.cleaned_data['content']
			greeting.update()

		if greeting:
			if users.is_current_user_admin():
				txn()
			else:
				if user and greeting.author == user:
					txn()
				else:
					logging.warning('not update greeting')
		return
