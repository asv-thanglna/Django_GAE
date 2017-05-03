from django.views.generic import TemplateView
from google.appengine.api import users

from guestbook.models import Greeting, DEFAULT_GUESTBOOK_NAME

class IndexView(TemplateView):
	template_name = 'guestbook/main_page.html'
	context_object_name = 'greetings'

	def get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name')
		if not guestbook_name or guestbook_name == '':
			guestbook_name = DEFAULT_GUESTBOOK_NAME
		return guestbook_name

	def get_context_data(self, **kwargs):
		guestbook_name = self.get_guestbook_name()
		urlsafe = self.request.GET.get('urlsafe', '')
		context = super(IndexView, self).get_context_data(**kwargs)
		context['guestbook_list'], context['urlsafe'], context['more'] = \
			Greeting.get_greeting_by_page(guestbook_name, urlsafe)
		context['guestbook_name'] = guestbook_name

		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		if users.get_current_user():
			url = users.create_logout_url(request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(request.get_full_path())
			url_linktext = 'Login'

		context['url'] = url
		context['url_linktext'] = url_linktext
		return self.render_to_response(context)
