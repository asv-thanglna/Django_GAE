# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json


class JSONResponseMixin(object):

	response_class = HttpResponse

	def render_to_json_response(self, context, **response_kwargs):
		response_kwargs['content_type'] = 'application/json; charset=utf-8'
		return self.response_class(self.convert_context_to_json(context), **response_kwargs)

	def convert_context_to_json(self, context):
		return json.dumps(context)
