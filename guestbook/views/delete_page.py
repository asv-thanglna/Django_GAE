# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from google.appengine.api import users
from google.appengine.ext import ndb
from guestbook.models import Greeting
from django.shortcuts import redirect
import logging


class DeleteView(TemplateView):

	def post(self, request, *args, **kwargs):
		guestbook_id = ''
		if 'guestbook_id' in kwargs:
			guestbook_id = kwargs['guestbook_id']
		guestbook_name = ''
		if 'guestbook_name' in kwargs:
			guestbook_name = kwargs['guestbook_name']
		if guestbook_id == '' or guestbook_name == '':
			logging.warn('error')
			return

		self.delete_greeting(int(guestbook_id), guestbook_name)
		return redirect('%s?guestbook_name=%s' % (reverse_lazy('index'), guestbook_name))

	def delete_greeting(self, guestbook_id, guestbook_name):
		user = users.get_current_user()
		greeting = Greeting.get_greeting(guestbook_id, guestbook_name)

		@ndb.transactional
		def txn():
			greeting.key.delete()

		if greeting:
			if users.is_current_user_admin():
				txn()
			else:
				if user and greeting.author == user:
					txn()
				else:
					logging.info('error')
		else:
			logging.warning('not delete greeting')
		return
