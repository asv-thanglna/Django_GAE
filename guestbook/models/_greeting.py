# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	'''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
	return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_greeting_by_page(self, guestbook_name, urlsafe=''):
		nums_of_page = 5
		cursor = Cursor(urlsafe=urlsafe)
		datas, next_cursor, more = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(
			-Greeting.date).fetch_page(nums_of_page, start_cursor=cursor)
		next_urlsafe = ''
		if next_cursor is not None:
			next_urlsafe = next_cursor.urlsafe
		for data in datas:
			data.id = data.get_id()
		return datas, next_urlsafe, more

	@classmethod
	@ndb.transactional
	def insert_greeting(cls, guestbook_name, author=None, content=''):
		greeting = cls(parent=guestbook_key(guestbook_name))
		if author:
			greeting.author = author
		greeting.content = content
		greeting.put()
		return greeting

	@classmethod
	def get_greeting(cls, id, guestbook_name):
		greeting = cls.get_by_id(id, guestbook_key(guestbook_name))
		return greeting

	def get_id(self):
		return self.key.id()

	@ndb.transactional
	def update(self):
		self.put()
