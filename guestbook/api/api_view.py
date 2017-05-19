# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView
from django.http import HttpResponse

from google.appengine.api import datastore_errors, users
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb


from guestbook.api import JsonResponse, form
from guestbook.models import Greeting as g
import json
import logging


class Greetings(JsonResponse.JSONResponseMixin, TemplateView):

	def get_context_data(self, **kwargs):
		try:
			cur = Cursor(urlsafe=self.request.GET.get('cursor', ''))
			limit = int(self.request.GET.get('limit', 5))
		except datastore_errors.BadQueryError, exp:
			logging.warning('error=' + exp.message)
			return HttpResponse(status=400)
		except ValueError, e:
			logging.warning('error=' + e.message)
			return HttpResponse(status=400)

		guestbook_name = kwargs['guestbook_name']
		if guestbook_name == '':
			return HttpResponse(status=400)

		greetings, next_urlsafe, more = g.get_greeting_by_page(guestbook_name, limit, cur)
		results = []
		for greeting in greetings:
			results.append(greeting.to_resource_dict(guestbook_name=guestbook_name))
		context = {
			'guestbook_name': guestbook_name,
			'greetings': results,
			'next_cursor': next_urlsafe,
			'total_items': len(results)
		}
		return context


class Greeting(JsonResponse.JSONResponseMixin, FormView):

	form_class = form.GreetingDetailForm

	def get_form(self, form_class):
		c = JsonResponse.snakify
		if isinstance(self.kwargs, dict):
			self.kwargs = {c(k): v for k, v in self.kwargs.items()}
		return self.form_class(self.kwargs)

	def get(self, request, *args, **kwargs):
		guestbook_name = kwargs['guestbook_name']
		greeting_id = kwargs['greeting_id']
		greeting = g.get_greeting(int(greeting_id), guestbook_name)
		if greeting:
			context = greeting.to_resource_dict(guestbook_name)
			context['guestbook_name'] = guestbook_name
			return self.render_to_response(context, status=200)
		return self.render_to_response({'status': 'error'}, status=404)

	def put(self, *args, **kwargs):
		body_unicode = self.request.body
		body = json.loads(body_unicode)
		kwargs.update(body)
		self.kwargs = kwargs
		return super(Greeting, self).put(*args, **kwargs)

	def form_valid(self, form):
		greeting = g.get_greeting(int(form.cleaned_data['greeting_id']),
			form.cleaned_data['guestbook_name'])

		user = users.get_current_user()

		@ndb.transactional
		def txn():
			greeting.updated_by = user
			greeting.content = form.cleaned_data['content']
			greeting.greeting_name = form.cleaned_data['greeting_name']
			greeting.update()

		if greeting:
			if user and (users.is_current_user_admin() or user == greeting.author):
				txn()
				context = {'msg': 'ok'}
				return self.render_to_response(context, status=200)
			return self.render_to_response({'msg': 'error'}, status=401)
		return self.render_to_response({'msg': 'error'}, status=404)

	def form_invalid(self, form):
		return self.render_to_response({'msg': 'error'}, status=400)

	def delete(self, request, *args, **kwargs):
		try:
			guestbook_name = kwargs['guestbook_name']
			greeting_id = int(kwargs['greeting_id'])
			greeting = g.get_greeting(greeting_id, guestbook_name)
		except BaseException, e:
			logging.warning(e.message)
			return self.render_to_response({'msg': 'error'}, status=400)

		@ndb.transactional
		def txn():
			greeting.key.delete()

		if greeting:
			user = users.get_current_user()
			if users.is_current_user_admin() or (user and greeting.author == user):
				txn()
				return self.render_to_response({'msg': 'ok'}, status=200)
			return self.render_to_response({'msg': 'error'}, status=401)
		return self.render_to_response({'msg': 'error'}, status=404)
