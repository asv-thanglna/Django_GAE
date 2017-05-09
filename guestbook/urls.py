# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from guestbook.views import IndexView, SignView, UpdateView, DeleteView
from guestbook.api import GreetingList, GreetingDetail

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(), name='index', ),
	url(r'^sign/$', SignView.as_view(), name='sign'),
	url(r'^update/$', UpdateView.as_view(), name='update'),
	url(r'^delete/(?P<guestbook_id>[0-9].*)/(?P<guestbook_name>.*)/$', DeleteView.as_view(), name='delete'),

	## greeting apis
	url(r'^api/v1/(?P<guestbook_name>.*)/greetings/$', GreetingList.as_view(),
		name='greeting_list'),
	url(r'^api/v1/(?P<guestbook_name>.*)/(?P<greeting_id>[0-9].*)/$', GreetingDetail.as_view(),
		name='greeting_detail'),
)
