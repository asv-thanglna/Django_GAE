from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from google.appengine.api import users

from guestbook.models import Greeting
from guestbook.forms import SignForm
from guestbook.services import add_queue_send_mail


class SignView(FormView):
	template_name = 'guestbook/sign_page.html'
	form_class = SignForm
	success_url = reverse_lazy('index')

	def sign_book(self, guestbook_name, content):
		if guestbook_name != '':
			user = users.get_current_user()
			greeting = Greeting.insert_greeting(guestbook_name, user, content)
			add_queue_send_mail(user, guestbook_name, greeting.content)

	def get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name', '')
		return guestbook_name

	def get_initial(self):
		initial = super(SignView, self).get_initial()
		initial['guestbook_name'] = self.get_guestbook_name()
		return initial

	def get_context_data(self, **kwargs):
		guestbook_name = self.get_guestbook_name()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = super(SignView, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['sign_form'] = form
		return context

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form, **kwargs):
		self.sign_book(form.cleaned_data['guestbook_name'], form.cleaned_data['content'])
		return super(SignView, self).form_valid(form, **kwargs)

	def get_success_url(self):
		url = reverse_lazy('index')
		return '%s?guestbook_name=%s' % (url, self.get_guestbook_name())
