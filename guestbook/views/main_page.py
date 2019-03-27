# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from google.appengine.api import users

from guestbook.models import Greeting, DEFAULT_GUESTBOOK_NAME
from google.appengine.api import datastore_errors
from google.appengine.datastore.datastore_query import Cursor
from django.http import Http404

import logging
class IndexView(TemplateView):
	template_name = 'guestbook/main_page.html'
	context_object_name = 'greetings'

	def get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name')
		if not guestbook_name or guestbook_name == '':
			guestbook_name = DEFAULT_GUESTBOOK_NAME
		return guestbook_name

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		if users.get_current_user():
			url = users.create_logout_url(request.get_full_path())
			url_linktext = 'Logout'
			user_email = users.get_current_user().email()
		else:
			url = users.create_login_url(request.get_full_path())
			url_linktext = 'Login'
			user_email = ''
		context['user_email'] = user_email
		context['url'] = url
		context['url_linktext'] = url_linktext

		guestbook_name = self.get_guestbook_name()
		try:
			cur = Cursor(urlsafe=self.request.GET.get('cursor', ''))
		except datastore_errors.BadQueryError:
			return Http404

		limit = int(self.request.GET.get('limit', 5))
		context['guestbook_list'], context['next_cursor'], context['more'] = \
			Greeting.get_greeting_by_page(guestbook_name, limit, cur)
		context['guestbook_name'] = guestbook_name
		return self.render_to_response(context)
