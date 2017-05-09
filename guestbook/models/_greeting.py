# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
import logging

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	'''Constructs a Datastore key for a Guestbook entity with guestbook_name.'''
	return ndb.Key('Guestbook', guestbook_name)


def greeting_to_obj(obj, guestbook_name):
		author = ''
		if obj.author is not None:
			author = obj.author.email()
		updated_by = ''
		if obj.updated_by is not None:
			updated_by = obj.updated_by.email()
		updated_date = ''
		if obj.updated_date is not None:
			updated_date = obj.updated_date.strftime('%Y-%m-%d %H:%M:%S')

		return {
			'id': obj.get_id(),
			'author': author,
			'content': obj.content,
			'date': obj.date.strftime('%Y-%m-%d %H:%M:%S'),
			'updated_by': updated_by,
			'updated_date': updated_date,
			'url': '/api/v1/' + guestbook_name + '/' + str(obj.get_id()) + '/'
		}


def greeting_to_dict(args, guestbook_name):
	results = []
	for arg in args:
		results.append(greeting_to_obj(arg, guestbook_name))
	return results


class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	updated_date = ndb.DateTimeProperty(auto_now=True)
	updated_by = ndb.UserProperty()

	@classmethod
	def get_greeting_by_page(self, guestbook_name, urlsafe=''):
		nums_of_page = 5
		cursor = Cursor(urlsafe=urlsafe)
		datas, next_cursor, more = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(
			-Greeting.date).fetch_page(nums_of_page, start_cursor=cursor)
		next_urlsafe = ''
		if next_cursor is not None:
			next_urlsafe = next_cursor.urlsafe()
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

	def update(self):
		self.put()
