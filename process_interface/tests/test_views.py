from base64 import decodestring as b64decodestring
from os import urandom
from random import randint

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from process_interface.models import Analysis, Vintage

class ViewLoginLogout ( TestCase ):

	@classmethod
	def setUpClass ( cls ):
		from django.contrib.auth.models import User

		User.objects.create_user(
		  username='test_user',
		  password='SomethingSecure',
		  email='some@email'
		)
		cls.user = User.objects.get(email='some@email')


	@classmethod
	def tearDownClass ( cls ):
		cls.user.delete()


	def test_bad_logins_fail ( self ):
		c = Client()

		# some fuzz testing
		# 257 is one byte longer than 256.  Just testing a potential off-by-one
		# error, or length-issues.
		for i in range(10):
			len_username = randint( 1, 257 ) # 1 and 257 are possible results
			len_password = randint( 1, 257 ) # 1 and 257 are possible results
			u = urandom( len_username )
			p = urandom( len_password )
			if (u, p) == ('test_user', 'SomethingSecure'):
				# this is tested below, and should /not/ fail.
				continue

			login_url    = reverse('process_interface:login')
			interact_url = reverse('process_interface:view')
			res = c.post(login_url, {'username': u, 'password': p})

			cookie = b64decodestring( res.cookies['ServerState'].coded_value )

			# Ensure test-runner does not think we're logged in
			self.assertEqual( len(c.session.items()), 0 )

			# Do we get the expected SEE OTHER interaction?
			self.assertEqual( res.status_code, 303 )
			self.assertEqual( res.reason_phrase, u'SEE OTHER' )
			self.assertEqual( res.content, '' )
			self.assertTrue( res.has_header('Location'), True )
			self.assertTrue( res.get('Location').endswith( interact_url ))

			# Did server appropriately leave us as unauthenticated?
			self.assertEqual( cookie, '{"username": null}' )

			# Ensure that the response we get is for unauthenticated users
			res = c.get( res.get('Location') )

			cookie = b64decodestring( res.cookies['ServerState'].coded_value )

			self.assertEqual( len(c.session.items()), 0 )
			self.assertEqual( res.status_code, 200 )
			self.assertEqual( res.reason_phrase, u'OK' )
			self.assertEqual( cookie, '{"username": null}' )
			self.assertNotIn( " id='LogoutLink' ", res.content )
			self.assertIn( " id='LoginForm' ", res.content )


	def test_successful_login_returns_username_in_cookie ( self ):
		c = Client()
		u, p = 'test_user', 'SomethingSecure'

		login_url = reverse('process_interface:login')
		res = c.post(login_url, {'username': u, 'password': p})

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		# Ensure test-runner thinks we're authenticated
		self.assertNotEqual( len(c.session.items()), 0 )

		# First, do we get the expected SEE OTHER interaction?
		self.assertEqual( res.status_code, 303 )
		self.assertEqual( res.reason_phrase, u'SEE OTHER' )
		self.assertEqual( res.content, '' )
		self.assertTrue( res.has_header('Location'), True )
		self.assertTrue( res.get('Location').endswith('/interact/') )

		# Did server tell us that we successfully authenticated?
		self.assertEqual( cookie, '{"username": "test_user"}' )

		# Ensure that the response we get is for unauthenticated users
		res = c.get( res.get('Location') )

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		self.assertEqual( res.status_code, 200 )
		self.assertEqual( res.reason_phrase, u'OK' )
		self.assertEqual( cookie, '{"username": "test_user"}' )
		self.assertIn( " id='LogoutLink' ", res.content )
		self.assertNotIn( " id='LoginForm' ", res.content )


	def test_logout ( self ):
		"""
		Ensure that the test client knows of logout status, and that server
		returns a null value for the username.
		"""
		c = Client()
		u, p = 'test_user', 'SomethingSecure'

		login_url = reverse('process_interface:login')
		res = c.post(login_url, {'username': u, 'password': p})

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		# First, ensure we've logged in properly
		self.assertNotEqual( len(c.session.items()), 0 )
		self.assertEqual( cookie, '{"username": "test_user"}' )

		logout_url = reverse('process_interface:logout')
		res = c.get( logout_url )

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		self.assertEqual( len(c.session.items()), 0 )
		self.assertEqual( cookie, '{"username": null}' )




class ViewAnalysisTest ( TestCase ):

	@classmethod
	def setUpClass ( cls ):
		from django.contrib.auth.models import User

		User.objects.create_user(
		  username='test_user',
		  password='SomethingSecure',
		  email='some@email'
		)
		cls.user = User.objects.get(email='some@email')


	@classmethod
	def tearDownClass ( cls ):
		cls.user.delete()


	def setUp ( self ):
		self.client = Client()
		up = {'username': 'test_user', 'password': 'SomethingSecure'}
		res = self.client.post(reverse('process_interface:login'), up)

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

		self.assertEqual( res.status_code, 303 )
		self.assertEqual( res.reason_phrase, u'SEE OTHER' )
		self.assertEqual( cookie, '{"username": "test_user"}' )


	def tearDown ( self ):
		self.client.get('/logout/')
		del self.client


	def test_anonymous_user_cannot_create_analyses ( self ):
		c = self.client

		# First become an anonymous user
		res = c.get( reverse('process_interface:logout') )
		url = reverse('process_interface:analysis_create')

		analysis_create_url = reverse('process_interface:analysis_create')
		post_data = {}

		# Fuzz testing: should *always* get 401 (UNAUTHORIZED) in return
		for i in range(10):
			post_data.update(
			  name        = urandom( randint(1, 32769) ), # bounds on field length
			  description = urandom( randint(1, 32769) ), # just some large number
			  period_0    = urandom( randint(1, 32769) ), # just some large number
			  global_discount_rate = urandom( randint(1, 32769) ),
			  vintages    = urandom( randint(1, 32769) ), # just some large number
			)
			res = c.post( analysis_create_url, post_data )
			self.assertEqual( res.reason_phrase, 'UNAUTHORIZED')


	def test_create_analysis ( self ):
		"""
		Tests that user can create analyses.
		"""

		a = Analysis.objects.create(
		  user        = self.user,
		  name        = 'Some Analysis Name',
		  description = 'Some analysis description',
		  period_0    = 1,
		  global_discount_rate = 0.01,
		)


