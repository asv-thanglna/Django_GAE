# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from guestbook.api import jsonresponse
from guestbook.models import Greeting, greeting_to_obj, greeting_to_dict


class GreetingList(jsonresponse.JSONResponseMixin, TemplateView):

	def get_context_data(self, **kwargs):
		urlsafe = self.request.GET.get('urlsafe', '')
		guestbook_name = kwargs['guestbook_name']
		greetings, next_urlsafe, more = Greeting.get_greeting_by_page(guestbook_name, urlsafe)
		context = {}
		context['guestbook_name'] = guestbook_name
		context['greetings'] = greeting_to_dict(greetings, guestbook_name)
		context['next_cursor'] = next_urlsafe
		context['total_items'] = len(greetings)
		return context

	def render_to_response(self, context, **response_kwargs):
		return self.render_to_json_response(context, **response_kwargs)


class GreetingDetail(jsonresponse.JSONResponseMixin, TemplateView):

	def get_context_data(self, **kwargs):
		guestbook_name = kwargs['guestbook_name']
		greeting_id = kwargs['greeting_id']
		greeting = Greeting.get_greeting(int(greeting_id), guestbook_name)
		context = {}
		if greeting:
			context = greeting_to_obj(greeting, guestbook_name)
			context['guestbook_name'] = guestbook_name
		return context

	def render_to_response(self, context, **response_kwargs):
		return self.render_to_json_response(context, **response_kwargs)
