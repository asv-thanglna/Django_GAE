from django.conf.urls.defaults import *
from guestbook.views import IndexView, SignView, UpdateView

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(), name='index', ),
	url(r'^sign/$', SignView.as_view(), name='sign'),
	url(r'^update/$', UpdateView.as_view(), name='update'),
	url(r'^delete/$', SignView.as_view(), name='delete'),
)
