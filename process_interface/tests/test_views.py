from base64 import decodestring as b64decodestring

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
		from random import randint
		from os import urandom

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

			# First, do we get the expected SEE OTHER interaction?
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

			self.assertEqual( res.status_code, 200 )
			self.assertEqual( res.reason_phrase, u'OK' )
			self.assertEqual( cookie, '{"username": null}' )
			self.assertNotIn( res.content, " id='LogoutLink' " )
			self.assertIn( res.content, " id='LoginForm' " )


	def test_successful_login_returns_username_in_cookie ( self ):
		c = Client()
		u, p = 'test_user', 'SomethingSecure'

		login_url = reverse('process_interface:login')
		res = c.post(login_url, {'username': u, 'password': p})

		cookie = b64decodestring( res.cookies['ServerState'].coded_value )

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


	def test_create_update_delete_analysis ( self ):
		"""
		Tests that analyses can be created.
		"""

		a = Analysis.objects.create(
		  user        = self.user,
		  name        = 'Some Analysis Name',
		  description = 'Some analysis description',
		  period_0    = 1,
		  global_discount_rate = 0.01,
		)


