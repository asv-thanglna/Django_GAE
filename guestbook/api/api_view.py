# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView
from guestbook.api import JsonResponse, form
from guestbook.models import Greeting
from google.appengine.api import datastore_errors
from google.appengine.datastore.datastore_query import Cursor
from django.http import HttpResponse


class GreetingService(JsonResponse.JSONResponseMixin, TemplateView):

	def get_context_data(self, **kwargs):
		try:
			cur = Cursor(urlsafe=self.request.GET.get('cursor', ''))
		except datastore_errors.BadQueryError:
			return HttpResponse(status=404)
		guestbook_name = kwargs['guestbook_name']
		limit = int(self.request.GET.get('limit', 5))
		greetings, next_urlsafe, more = Greeting.get_greeting_by_page(guestbook_name, limit, cur)
		context = {
			'guestbook_name': guestbook_name
		}
		results = []
		for greeting in greetings:
			results.append(greeting.to_resource_dict(guestbook_name=guestbook_name))
		context['greetings'] = results
		context['next_cursor'] = next_urlsafe
		context['total_items'] = len(greetings)
		return context


class GreetingDetail(JsonResponse.JSONResponseMixin, FormView):

	form_class = form.GreetingDetailForm

	def get(self, request, *args, **kwargs):
		guestbook_name = kwargs['guestbook_name']
		greeting_id = kwargs['greeting_id']
		greeting = Greeting.get_greeting(int(greeting_id), guestbook_name)
		context = {}
		if greeting:
			context = greeting.to_resource_dict(guestbook_name)
			context['guestbook_name'] = guestbook_name
		return self.render_to_response(context)
